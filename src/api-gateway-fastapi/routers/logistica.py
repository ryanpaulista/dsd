from fastapi import APIRouter, HTTPException
import httpx
from config import URL_LOGISTICA
from schemas import FreteRequest

router = APIRouter(tags=["Logística"])

@router.post("/produtos/{id_produto}/frete")
async def calcular_frete(id_produto: int, dados: FreteRequest):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "cep": dados.cep,
                "peso": dados.peso
            }

            resp = await client.post(URL_LOGISTICA, json=payload)

            if resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Erro no cálculo de frete")
            
            return resp.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de Logística indisponível")
            