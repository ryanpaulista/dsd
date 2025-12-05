from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import catalogo, logistica

app = FastAPI(
    title="Brainz E-Shop Gateway",
    description="Gateway central com HATEOAS.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalogo.router)
app.include_router(logistica.router)

@app.get("/", tags=["Status"])
async def root():
    return {"status": "Gateway Online", "docs": "/docs"}