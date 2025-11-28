from fastapi import APIRouter, HTTPException
import httpx
from typing import List
from config import URL_CATALOGO, GATEWAY_URL
from schemas import ProdutoResponse, Link

router = APIRouter(tags=["Catálogo"])

@router.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{URL_CATALOGO}/")
            produtos_django = resp.json()
            print(produtos_django)

            produtos_enriquecidos = []
            for p in produtos_django:
                links = [
                    Link(href=f"{GATEWAY_URL}/produtos/{p['id']}", rel="self", method="GET"),
                    Link(href=f"{GATEWAY_URL}/produtos/{p['id']}/frete", rel="calcular_frete", method="POST")
                ]
                p_novo = {**p, "links": links}
                produtos_enriquecidos.append(p_novo)

            return produtos_enriquecidos
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de Catálogo indisponível")

@router.get("/produtos/{id_produto}", response_model=ProdutoResponse)
async def detalhe_produto(id_produto: int):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{URL_CATALOGO}/{id_produto}/")
            if resp.status_code == 404:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            
            if resp.status_code != 200:
                print(f"Erro no Django: {resp.status_code} - {resp.text}")
                raise HTTPException(status_code=502, detail="Erro interno no serviço de Catálogo")

            produto = resp.json()
            links = [
                Link(href=f"{GATEWAY_URL}/produtos/{id_produto}", rel="self", method="GET"),
                Link(href=f"{GATEWAY_URL}/produtos/{id_produto}/frete", rel="calcular_frete", method="POST"),
                Link(href=f"{GATEWAY_URL}/comprar", rel="comprar", method="POST")
            ]

            return {**produto, "links": links}
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de Catálogo indisponível")
        

