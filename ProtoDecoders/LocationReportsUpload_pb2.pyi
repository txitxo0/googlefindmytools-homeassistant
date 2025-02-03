from ProtoDecoders import Common_pb2 as _Common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationReportsUpload(_message.Message):
    __slots__ = ("reports", "clientMetadata", "random1", "random2")
    REPORTS_FIELD_NUMBER: _ClassVar[int]
    CLIENTMETADATA_FIELD_NUMBER: _ClassVar[int]
    RANDOM1_FIELD_NUMBER: _ClassVar[int]
    RANDOM2_FIELD_NUMBER: _ClassVar[int]
    reports: _containers.RepeatedCompositeFieldContainer[Report]
    clientMetadata: ClientMetadata
    random1: int
    random2: int
    def __init__(self, reports: _Optional[_Iterable[_Union[Report, _Mapping]]] = ..., clientMetadata: _Optional[_Union[ClientMetadata, _Mapping]] = ..., random1: _Optional[int] = ..., random2: _Optional[int] = ...) -> None: ...

class Report(_message.Message):
    __slots__ = ("advertisement", "time", "location")
    ADVERTISEMENT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    advertisement: Advertisement
    time: _Common_pb2.Time
    location: _Common_pb2.LocationReport
    def __init__(self, advertisement: _Optional[_Union[Advertisement, _Mapping]] = ..., time: _Optional[_Union[_Common_pb2.Time, _Mapping]] = ..., location: _Optional[_Union[_Common_pb2.LocationReport, _Mapping]] = ...) -> None: ...

class Advertisement(_message.Message):
    __slots__ = ("identifier", "unwantedTrackingModeEnabled")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    UNWANTEDTRACKINGMODEENABLED_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    unwantedTrackingModeEnabled: int
    def __init__(self, identifier: _Optional[_Union[Identifier, _Mapping]] = ..., unwantedTrackingModeEnabled: _Optional[int] = ...) -> None: ...

class Identifier(_message.Message):
    __slots__ = ("truncatedEid", "canonicDeviceId")
    TRUNCATEDEID_FIELD_NUMBER: _ClassVar[int]
    CANONICDEVICEID_FIELD_NUMBER: _ClassVar[int]
    truncatedEid: bytes
    canonicDeviceId: bytes
    def __init__(self, truncatedEid: _Optional[bytes] = ..., canonicDeviceId: _Optional[bytes] = ...) -> None: ...

class ClientMetadata(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: ClientVersionInformation
    def __init__(self, version: _Optional[_Union[ClientVersionInformation, _Mapping]] = ...) -> None: ...

class ClientVersionInformation(_message.Message):
    __slots__ = ("playServicesVersion",)
    PLAYSERVICESVERSION_FIELD_NUMBER: _ClassVar[int]
    playServicesVersion: str
    def __init__(self, playServicesVersion: _Optional[str] = ...) -> None: ...
