from pydantic import BaseModel, Field, conlist, ValidationError
from typing import Optional, List

EMBEDDING_DIM = 1536
Vector = conlist(float, min_length=EMBEDDING_DIM, max_length=EMBEDDING_DIM)

class Doc(BaseModel):
    doc_id: Optional[int] = Field(default=None) # primary key, automatically asigned
    api_key: str
    url: str
    title: str

    class Config:
        from_attributes = True

class Chunk(BaseModel):
    chunk_id: str # primary_key, needs to be explicxitly given
    api_key: str
    doc_id: str
    text: str
    embedding: List[float]

    class Config:
        from_attributes = True


class Image(BaseModel):
    image_id: Optional[int] = Field(default=None) # primary key, automatically asigned
    api_key: str
    url: str
    image: str
    embeddings: List[float]

    class Config:
        from_attributes = True


class Pixel(BaseModel):
    pixel_id: Optional[int] = Field(default=None) # primary key, automatically asigned
    api_key: str
    image_id: str
    embedding: List[float]

    class Config:
        from_attributes = True

class archiveMetadata(BaseModel):
    size: Optional[int] = Field(default=None)
    type_: str
    url_: Optional[str] = Field(default=None)
    text_: Optional[str] = Field(default=None)
    vec_modality: Optional[str] = Field(default=None)
    vec_dim: Optional[int] = Field(default=None)
    index_id: Optional[str] = Field(default=None)
    namespace_id: Optional[str] = Field(default=None)
    api_key: str

    class Config:
        from_attributes = True

class imageSchema(BaseModel):
    image_id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    image_url: str

    class Config:
        from_attributes = True
