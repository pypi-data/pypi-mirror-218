from dataclasses import dataclass

from ..logger import log
from .payload import MessagePayload
from .utils import B642B, unpack_buffer_to_list, B2B64
from .enums import EventOperationID

@dataclass
class EventHeader:
    mod: int 
    appid: int 
    timestamp: int
    payload_size: int

    def to_dict(self) -> str:
        return {
            "mod": self.mod,
            "appid": self.appid,
            "timestamp": self.timestamp,
            "payload_size": self.payload_size
        }

    def to_array(self) -> list:
        return [
            self.mod, 
            self.appid,
            self.timestamp, 
            self.payload_size
        ]


@dataclass
class EventDataIn:
    datasource: int
    datatype: str
    buffer: bytes

    def to_dict(self) -> str:
        return {
            "datasource": self.datasource,
            "datatype": self.datatype,
            "buffer": unpack_buffer_to_list(self.buffer, self.datatype[0] == "<", 4, self.datatype[1])
        }

    def to_array(self) -> list:
        return [
            self.datasource,
            self.datatype,
            self.buffer
        ]


@dataclass
class EventException:
    error: int
    msg: str

    def to_dict(self) -> str:
        return {
            "error": self.error,
            "msg": self.msg
        }

    def to_array(self) -> list:
        return [
            self.error,
            self.msg
        ]


@dataclass
class EventCMDStatus:
    mod: int
    op: int
    status: int

    def to_dict(self) -> str:
        return {
            "mod": self.mod,
            "op": self.op,
            "status": self.status
        }

    def to_array(self) -> list:
        return [
            self.mod,
            self.op,
            self.status
        ]


@dataclass
class EventLog:
    level: int
    msg: str

    def to_dict(self) -> str:
        return {
            "level": self.level,
            "msg": self.msg
        }

    def to_array(self) -> list:
        return [
            self.level,
            self.msg
        ]


@dataclass
class EventAslResult:
    label_type: int
    confidence: float
    result: list

    def to_dict(self) -> str:
        return {
            "label_type": self.label_type,
            "confidence": self.confidence,
            "result": self.result
        }

    def to_array(self) -> list:
        return [
            self.label_type,
            self.confidence,
            self.result
        ]


@dataclass
class EventInferResult:
    ai_type:int
    label_type: int
    step: int
    result: list

    def to_dict(self) -> str:
        return {
            "ai_type": self.ai_type,
            "label_type": self.label_type,
            "step": self.step,
            "result": self.result
        }

    def to_array(self) -> list:
        return [
            self.ai_type,
            self.label_type,
            self.step,
            self.result
        ]


@dataclass
class EventSetMode:
    ai_mode: int
    ai_type: int
    data: list

    def to_dict(self) -> str:
        return {
            "ai_mode": self.ai_mode,
            "ai_type": self.ai_type,
            "data":self.data
        }
    
    def to_array(self) -> list:
        return [
            self.ai_mode,
            self.ai_type,
            self.data
        ]


@dataclass
class EventCorrection:
    position: int
    ai_type: int
    data: list

    def to_dict(self) -> str:
        return {
            "position": self.position,
            "ai_type": self.ai_type,
            "data":self.data
        }

    def to_array(self) -> list:
        return [
            self.position,
            self.ai_type,
            self.data
        ]
    

@dataclass
class EventTrigger:
    trigger_type: int
    trigger_value: int

    def to_dict(self) -> str:
        return {
            "trigger_type": self.trigger_type,
            "trigger_value": self.trigger_value,
        }
    
    def to_array(self) -> list:
        return [
            self.trigger_type,
            self.trigger_value
        ]
    

@dataclass
class EventCustom:
    data: bytearray

    def __init__(self, data) -> None:
        if(type(data) == str):
            data = B642B(data)
        self.data = bytearray(data)

    def to_dict(self) -> str:
        return { "data": B2B64(self.data) }

    def to_array(self) -> list:
        return [ self.data ]
    

OP_TO_EVENT_TYPES = {
    EventOperationID.EVT_EXT_EXCEPTION.value:     EventException,
    EventOperationID.EVT_EXT_DATA_IN.value:       EventDataIn,
    EventOperationID.EVT_EXT_CMD_STATUS.value:    EventCMDStatus,
    EventOperationID.EVT_EXT_LOG.value:           EventLog,
    EventOperationID.EVT_EXT_ASL_RESULT.value:    EventAslResult, 
    EventOperationID.EVT_EXT_VM_RESULT.value:     EventInferResult, 
    EventOperationID.EVT_EXT_SET_MODE.value:      EventSetMode,
    EventOperationID.EVT_EXT_CORRECTION.value:    EventCorrection,
    EventOperationID.EVT_EXT_TRIGGER.value:       EventTrigger,
    EventOperationID.EVT_EXT_CUSTOM_1.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_2.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_3.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_4.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_5.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_6.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_7.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_8.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_9.value:      EventCustom,
    EventOperationID.EVT_EXT_CUSTOM_10.value:     EventCustom
}


def GetEventClass(event_type_id: int):
    return OP_TO_EVENT_TYPES.get(event_type_id, None)

class EventMessagePayload(MessagePayload):
    @classmethod
    def from_array(cls, operation: int, raw_data: list) -> "MessagePayload":
        EventClass = GetEventClass(operation)
        if EventClass is None:
            log(f"Operation {operation} unknown", logger_level="ERROR")
            return

        payload = cls()
        payload.header = EventHeader(*raw_data[:4])
        payload.event = EventClass(*raw_data[4:])

        return payload

    @classmethod
    def from_json(cls, operation: int, raw_data: list) -> "MessagePayload":
        EventClass = GetEventClass(operation)
        if EventClass is None:
            log(f"Operation {operation} unknown", logger_level="ERROR")
            return
            
        payload = cls()
        payload.header = EventHeader(**raw_data["header"])
        payload.event = EventClass(**raw_data["data"])

        return payload

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "data": self.event.to_dict()
        }
