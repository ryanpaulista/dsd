# Brainz E-Shop — Integração REST + SOAP com API Gateway (HATEOAS)

**Resumo**  
Este projeto demonstra uma arquitetura híbrida onde **serviços REST** (Django + Express), um **serviço SOAP** (Spyne/Python) e um **API Gateway** (FastAPI) trabalham juntos. Há também um **cliente web** em Vue que consome o Gateway. O Gateway implementa **HATEOAS** e disponibiliza documentação via Swagger (FastAPI).

---

## ✅ Tecnologias usadas
- **API Gateway**: FastAPI (Python) — `src/api-gateway-fastapi`
- **Catálogo (REST)**: Django + Django REST Framework — `src/api-catalogo-django`
- **API Logística (consumidor SOAP / REST)**: Node.js + Express — `src/api-logistica-express`
- **Serviço SOAP (Frete)**: Spyne (Python) — `src/soap-frete-service`
- **RabbitMQ**
- **Cliente Web**: Vue 3 + Vite — `src/loja-vue`

---

## Arquitetura (visão rápida)
```
      ┌──────────────────────┐
      │  Front-End (Vue.js)  │
      └──────────▲───────────┘
                 │ HTTP (JSON)
                 │ WebSocket (Eventos)
                 │
      ┌──────────▼───────────┐
      │ API Gateway (FastAPI)│ ◄─── Orquestrador
      └────┬─────┬─────┬─────┘
           │     │     │
   REST    │     │     │ AMQP (Mensageria)
┌──────────▼─┐   │   ┌─▼──────────┐
│ API Django │   │   │  RabbitMQ  │ ◄─── Fila de Pedidos
│ (Catálogo) │   │   │            │ ◄─── Fila de Notificações
└────────────┘   │   └────────────┘
                 │
           ┌─────▼───────┐      SOAP      ┌─────────────┐
           │   API Node  │ ◄────────────► │   API SOAP  │
           │ (Logística) │      (XML)     │   (Frete)   │
           └─────────────┘                └─────────────┘
```

Processo Web (Server): Responde requisições HTTP (GET/POST). É o python manage.py runserver.

Processo Worker (Trabalhador): Fica rodando scripts de fundo, ouvindo filas. É o python manage.py run_consumer.


### Principais portas/endpoints (padrões no projeto)
- **Gateway (FastAPI)**: `http://localhost:8080/`
  - Swagger UI: `http://localhost:8080/docs`
- **Catálogo (Django REST)**: `http://127.0.0.1:8001/api/produtos` (ex.: `GET /api/produtos`)
- **SOAP Frete (Spyne)**: WSDL em `http://127.0.0.1:8000/?wsdl`
  - Serviço expõe método: `calcular_frete(cep: string, peso: float)` → retorna `FreteResponse`
- **API Logística (Express)**: `http://localhost:3000/cotacao-frete` (endpoint que consome o SOAP e retorna JSON)
- **Cliente Vue (Vite)**: `http://localhost:5173` (padrão Vite)
- **RabbitMQ**: `http://localhost:15672/`

---

## HATEOAS no Gateway

O Gateway adiciona links HATEOAS à resposta de produtos. Exemplo de resposta de /produtos (retornada pelo Gateway):
```bash
{
  "id": 1,
  "nome": "Camiseta Exemplo",
  "descricao": "...",
  "preco": 79.90,
  "peso": 0.3,
  "imagem_url": "http://...",
  "links": [
    { "href": "/produtos/1", "rel": "self", "method": "GET" },
    { "href": "/produtos", "rel": "listar", "method": "GET" },
    { "href": "/produtos/1", "rel": "atualizar", "method": "PUT" }
  ]
}
```

## Serviço SOAP — WSDL e principais tags

O Spyne publica um WSDL automaticamente. A URL padrão no projeto é http://127.0.0.1:8000/?wsdl.
Principais elementos que aparecerão no WSDL (exemplo simplificado):

```html
<definitions name="FreteService" targetNamespace="http://example.com/">
  <types>
    <!-- complexTypes: FreteResponse (valor, peso, prazo, obs) -->
  </types>

  <message name="calcular_freteRequest">
    <part name="cep" type="xsd:string"/>
    <part name="peso" type="xsd:float"/>
  </message>

  <message name="calcular_freteResponse">
    <part name="calcular_freteResult" element="tns:FreteResponse"/>
  </message>

  <portType name="FreteServicePortType">
    <operation name="calcular_frete">
      <input message="tns:calcular_freteRequest"/>
      <output message="tns:calcular_freteResponse"/>
    </operation>
  </portType>

  <binding name="FreteServiceBinding" type="tns:FreteServicePortType">
    <!-- binding SOAP11 -->
  </binding>

  <service name="FreteService">
    <port name="FretePort" binding="tns:FreteServiceBinding">
      <soap:address location="http://127.0.0.1:8000/"/>
    </port>
  </service>
</definitions>
```
