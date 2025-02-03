from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEMANTIC: _ClassVar[Status]
    LAST_KNOWN: _ClassVar[Status]
    CROWDSOURCED: _ClassVar[Status]
    AGGREGATED: _ClassVar[Status]
SEMANTIC: Status
LAST_KNOWN: Status
CROWDSOURCED: Status
AGGREGATED: Status

class Time(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...

class LocationReport(_message.Message):
    __slots__ = ("semanticLocation", "geoLocation", "status")
    SEMANTICLOCATION_FIELD_NUMBER: _ClassVar[int]
    GEOLOCATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    semanticLocation: SemanticLocation
    geoLocation: GeoLocation
    status: Status
    def __init__(self, semanticLocation: _Optional[_Union[SemanticLocation, _Mapping]] = ..., geoLocation: _Optional[_Union[GeoLocation, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ...) -> None: ...

class SemanticLocation(_message.Message):
    __slots__ = ("locationName",)
    LOCATIONNAME_FIELD_NUMBER: _ClassVar[int]
    locationName: str
    def __init__(self, locationName: _Optional[str] = ...) -> None: ...

class GeoLocation(_message.Message):
    __slots__ = ("encryptedReport", "deviceTimeOffset", "accuracy")
    ENCRYPTEDREPORT_FIELD_NUMBER: _ClassVar[int]
    DEVICETIMEOFFSET_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    encryptedReport: EncryptedReport
    deviceTimeOffset: int
    accuracy: float
    def __init__(self, encryptedReport: _Optional[_Union[EncryptedReport, _Mapping]] = ..., deviceTimeOffset: _Optional[int] = ..., accuracy: _Optional[float] = ...) -> None: ...

class EncryptedReport(_message.Message):
    __slots__ = ("publicKeyRandom", "encryptedLocation", "isOwnReport")
    PUBLICKEYRANDOM_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDLOCATION_FIELD_NUMBER: _ClassVar[int]
    ISOWNREPORT_FIELD_NUMBER: _ClassVar[int]
    publicKeyRandom: bytes
    encryptedLocation: bytes
    isOwnReport: bool
    def __init__(self, publicKeyRandom: _Optional[bytes] = ..., encryptedLocation: _Optional[bytes] = ..., isOwnReport: bool = ...) -> None: ...

class GetEidInfoForE2eeDevicesRequest(_message.Message):
    __slots__ = ("ownerKeyVersion", "hasOwnerKeyVersion")
    OWNERKEYVERSION_FIELD_NUMBER: _ClassVar[int]
    HASOWNERKEYVERSION_FIELD_NUMBER: _ClassVar[int]
    ownerKeyVersion: int
    hasOwnerKeyVersion: bool
    def __init__(self, ownerKeyVersion: _Optional[int] = ..., hasOwnerKeyVersion: bool = ...) -> None: ...
