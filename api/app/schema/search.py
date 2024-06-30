from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict
from pydantic.fields import Field
from typing import List, Optional

class queryMetadata(BaseModel):
    query: str
    query_order: int
    max_results: int
    api_key: str
    archive_id: Optional[int] = Field(default=None)
    namespace_id: Optional[str] = Field(default=None)
    index_id: Optional[str] = Field(default=None)
    use_cache: Optional[bool] = Field(default=True)

    class Config:
        from_attributes = True


class ResultSchema(BaseModel):
    result_id: Optional[int] = Field(default=None)
    index: int
    relevance_score: Optional[float] = Field(default=None)
    url_id: Optional[int] = Field(default=None)
    url: str
    title: str
    text_id: Optional[int] = Field(default=None)
    text: str
    query_order: int
    api_key: str
    query_id: Optional[int] = Field(default=None)

class ResponseSchema(BaseModel):
    results: List[ResultSchema] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return "\n".join([str(result) for result in self.results])
