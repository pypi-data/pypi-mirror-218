from pydantic import BaseModel


class KafkaEvent(BaseModel):

    tracing_id: str

    def to_str(self) -> str:
        pass
