from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Text, Union

DESCRIPTOR: _descriptor.FileDescriptor
TASK_STATUS_COMPLETE: TaskStatus
TASK_STATUS_ERROR: TaskStatus
TASK_STATUS_EXPIRED: TaskStatus
TASK_STATUS_IN_PROGRESS: TaskStatus
TASK_STATUS_PENDING: TaskStatus
TASK_STATUS_QUEUED: TaskStatus
TASK_STATUS_UNSPECIFIED: TaskStatus

class CreatePortfolioTaskRequest(_message.Message):
    __slots__ = ["layer_ids", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    LAYER_IDS_FIELD_NUMBER: ClassVar[int]
    METADATA_FIELD_NUMBER: ClassVar[int]
    layer_ids: _containers.RepeatedScalarFieldContainer[str]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, layer_ids: Optional[Iterable[str]] = ..., metadata: Optional[Mapping[str, str]] = ...) -> None: ...

class CreatePortfolioTaskResponse(_message.Message):
    __slots__ = ["task_id", "upload_url"]
    TASK_ID_FIELD_NUMBER: ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: ClassVar[int]
    task_id: str
    upload_url: str
    def __init__(self, task_id: Optional[str] = ..., upload_url: Optional[str] = ...) -> None: ...

class PortfolioQuotaInfoResponse(_message.Message):
    __slots__ = ["remaining", "used"]
    REMAINING_FIELD_NUMBER: ClassVar[int]
    USED_FIELD_NUMBER: ClassVar[int]
    remaining: int
    used: int
    def __init__(self, used: Optional[int] = ..., remaining: Optional[int] = ...) -> None: ...

class PortfolioStatusRequest(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: ClassVar[int]
    task_id: str
    def __init__(self, task_id: Optional[str] = ...) -> None: ...

class PortfolioStatusResponse(_message.Message):
    __slots__ = ["download_url", "errors", "task_status"]
    DOWNLOAD_URL_FIELD_NUMBER: ClassVar[int]
    ERRORS_FIELD_NUMBER: ClassVar[int]
    TASK_STATUS_FIELD_NUMBER: ClassVar[int]
    download_url: str
    errors: _containers.RepeatedScalarFieldContainer[str]
    task_status: TaskStatus
    def __init__(self, task_status: Optional[Union[TaskStatus, str]] = ..., download_url: Optional[str] = ..., errors: Optional[Iterable[str]] = ...) -> None: ...

class TaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
