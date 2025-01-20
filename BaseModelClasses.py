from pydantic import BaseModel

class ProductCreate(BaseModel):
    code: int

class ProductAttributeCreate(BaseModel):
    product_id: int
    attribute: str
    value: str

class NameProductCreate(BaseModel):
    product_id: int
    language: str
    name_product: str