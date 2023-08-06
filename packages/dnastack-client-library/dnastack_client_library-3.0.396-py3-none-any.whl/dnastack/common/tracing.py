import random
import time
from abc import ABC
from contextlib import contextmanager
from logging import Logger
from typing import Dict, Optional, List, Any

from py_zipkin import Tracer
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span

from dnastack.common.logger import get_logger_for, TraceableLogger
from dnastack.feature_flags import in_global_debug_mode


def _generate_random_64bit_string() -> str:
    """Returns a 64 bit UTF-8 encoded string. In the interests of simplicity,
    this is always cast to a `str` instead of (in py2 land) a unicode string.
    Certain clients (I'm looking at you, Twisted) don't enjoy unicode headers.

    This code is copied from https://github.com/Yelp/py_zipkin/blob/master/py_zipkin/util.py.

    :returns: random 16-character string
    """
    return f"{random.getrandbits(64):016x}"


def _generate_random_128bit_string() -> str:
    """Returns a 128 bit UTF-8 encoded string. Follows the same conventions
    as generate_random_64bit_string().

    The upper 32 bits are the current time in epoch seconds, and the
    lower 96 bits are random. This allows for AWS X-Ray `interop
    <https://github.com/openzipkin/zipkin/issues/1754>`_

    This code is copied from https://github.com/Yelp/py_zipkin/blob/master/py_zipkin/util.py.

    :returns: 32-character hex string
    """
    t = int(time.time())
    lower_96 = random.getrandbits(96)
    return f"{(t << 96) | lower_96:032x}"


# FIXME Remove this.
class TraceContext:
    """ Deprecated
    """

    def __init__(self):
        self._tracer: Optional[Tracer] = None

    @staticmethod
    def _silent_transport_handler():
        pass

    @contextmanager
    def new_span(self, service_name: str, span_name: str) -> None:
        """ Create a new span """
        if self._tracer is None:
            span = zipkin_span(service_name=service_name,
                               span_name=span_name,
                               transport_handler=self._silent_transport_handler,
                               sample_rate=0)

            self._tracer = span.get_tracer()
        else:
            span = zipkin_span(service_name=service_name,
                               span_name=span_name,
                               _tracer=self._tracer)
        span.start()
        try:
            yield span
        except BaseException as e:
            span.stop(type(e), e, None)  # The last argument is the traceback.
            raise e
        span.stop()

    @contextmanager
    def new_span_from(self, ref: object, span_name: str):
        with self.new_span(service_name=type(ref).__name__, span_name=span_name):
            yield

    def create_http_headers(self) -> Dict[str, str]:
        return create_http_headers_for_new_span(tracer=self._tracer)


class SpanInterface(ABC):
    def __init__(self):
        self.__active: bool = True

        local_logger_name = f'Span(origin={self.origin})' if self.origin else 'Span'

        self._logger = TraceableLogger.make(local_logger_name,
                                            trace_id=self.trace_id,
                                            span_id=self.span_id)
        self._logger.debug('Begin')

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def origin(self) -> str:
        raise NotImplementedError()

    @property
    def parent(self):
        raise NotImplementedError()

    @property
    def trace_id(self) -> str:
        raise NotImplementedError()

    @property
    def span_id(self) -> str:
        raise NotImplementedError()

    def __enter__(self):
        assert self.__active is not False, 'This span has already been deactivated.'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_http_headers(self) -> Dict[str, str]:
        return {
            k: v
            for k, v in {
                'X-B3-TraceId': self.trace_id,
                'X-B3-ParentSpanId': self.parent.span_id if self.parent else None,
                'X-B3-SpanId': self.span_id,
                'X-B3-Sampled': '0',
            }.items()
            if v is not None
        }

    def create_span_logger(self, parent_logger: TraceableLogger) -> TraceableLogger:
        return parent_logger.fork(trace_id=self.trace_id, span_id=self.span_id)

    def close(self):
        self.__active = False
        self._logger.debug('End')

        if in_global_debug_mode and not self.parent:
            self.print_tree(use_logger=True)

    def print_tree(self, print_root: bool = True, depth: int = 0, indent: int = 2, use_logger: bool = False):
        printer = (self._logger.debug if use_logger else print)

        if print_root:
            printer(f'* {self}')

        next_depth = depth + 1

        for child_span in self.__children:
            printer((' ' * (next_depth * indent)) + f'* {child_span}')
            child_span.print_tree(print_root=False, depth=next_depth, use_logger=use_logger)

    def __str__(self):
        return f'Span(trace_id={self.trace_id}, ' \
               f'span_id={self.span_id}, ' \
               f'parent_span_id={self.parent.span_id if self.parent else None}, ' \
               f'origin={self.origin})'


class Span(SpanInterface):
    def __init__(self, trace_id: Optional[str] = None, span_id: Optional[str] = None,
                 parent: Optional[SpanInterface] = None, origin: Any = None):
        self.__parent = parent
        self.__trace_id = (
                              parent.trace_id
                              if self.__parent is not None
                              else trace_id
                          ) or _generate_random_128bit_string()
        self.__span_id = span_id or _generate_random_64bit_string()
        self.__children: List[Span] = []

        # noinspection PyUnresolvedReferences
        self._origin = (
            self.__parent._origin
            if self.__parent
            else (
                origin
                if isinstance(origin, str)
                else f'{type(origin).__module__}.{type(origin).__name__}'
            )
        ) if origin else None

        super().__init__()

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def origin(self) -> str:
        return self._origin

    @property
    def parent(self):
        return self.__parent

    @property
    def trace_id(self) -> str:
        return self.__trace_id

    @property
    def span_id(self) -> str:
        return self.__span_id

    def new_span(self) -> SpanInterface:
        child_span = Span(self.trace_id, parent=self)
        self.__children.append(child_span)
        return child_span
