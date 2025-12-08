from pydantic import BaseModel
from typing import List

class Link(BaseModel):
    href: str
    rel: str
    method: str

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    peso: float
    estoque: int
    imagem_url: str
    links: List[Link]

class FreteRequest(BaseModel):
    cep: str
    peso: float

class CompraRequest(BaseModel):
    id_produto: int
    quantidade: int