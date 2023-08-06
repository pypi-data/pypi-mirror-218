from enum import Enum
from typing import Dict, Optional, Any, List

from pydantic import BaseModel, Field


class WorkflowDescriptor(BaseModel):
    workflow_name: str
    input_schema: Dict
    output_schema: Dict
    wdl_version: str
    errors: Optional[Any] = None


class WorkflowVersion(BaseModel):
    workflowId: Optional[str] = None
    id: str
    externalId: Optional[str] = None
    versionName: str
    workflowName: str
    createdAt: Optional[str] = None
    lastUpdatedAt: Optional[str] = None
    descriptorType: str
    authors: Optional[List[str]] = Field(default_factory=list)
    description: Optional[str] = None
    deleted: Optional[bool] = None
    etag: Optional[str] = None


class Workflow(BaseModel):
    internalId: str
    source: str
    name: str
    description: Optional[str] = None
    lastUpdatedAt: Optional[str] = None
    latestVersion: str
    authors: Optional[List[str]] = Field(default_factory=list)
    versions: Optional[List[WorkflowVersion]] = Field(default_factory=list)
    deleted: Optional[bool] = None
    etag: Optional[str] = None


class WorkflowFileType(str, Enum):
    primary = "PRIMARY_DESCRIPTOR"
    secondary = "DESCRIPTOR"
    test_file = "TEST_FILE"
    other = "OTHER"

class WorkflowSource(str,Enum):
    dockstore = "DOCKSTORE"
    custom = "CUSTOM"

class WorkflowFile(BaseModel):
    path: str
    file_type: WorkflowFileType
    content: Optional[str] = Field(default_factory=list)
    file_url: Optional[str] = Field(default_factory=list)


class WorkflowCreate(BaseModel):
    name: Optional[str] = Field(default_factory=list)
    description: Optional[str] = Field(default_factory=list)
    versionName: Optional[str] = Field(default_factory=list)
    files: List[WorkflowFile]


class WorkflowVersionCreate(BaseModel):
    versionName: str
    descriptions: Optional[str] = None
    files: List[WorkflowFile]


class WorkflowListResult(BaseModel):
    workflows: List[Workflow]


class WorkflowVersionListResult(BaseModel):
    versions: List[WorkflowVersion]

