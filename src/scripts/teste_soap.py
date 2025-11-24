import requests

# URL do seu Gateway SOAP
url = "http://localhost:8000/soap"

# O Envelope SOAP que define a requisição.
# Estamos pedindo o ID 1, que existe tanto na API Python quanto na Node.
payload = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tcc="tcc.soap.gateway">
   <soapenv:Header/>
   <soapenv:Body>
      <tcc:consultar_pedido>
         <tcc:pedido_id>1</tcc:pedido_id>
      </tcc:consultar_pedido>
   </soapenv:Body>
</soapenv:Envelope>
"""

headers = {
    'Content-Type': 'text/xml'
}

print(f"📡 Enviando requisição para {url}...")

try:
    response = requests.post(url, data=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print("\n--- RESPOSTA XML RECEBIDA ---")
    print(response.text)
    print("-----------------------------\n")

    # Validação rápida do resultado
    if response.status_code == 200:
        texto = response.text
        check_python = "Notebook Gamer" in texto
        check_node = "EM_TRANSITO" in texto
        
        if check_python and check_node:
            print("✅ SUCESSO TOTAL!")
            print("   - O Gateway buscou 'Notebook Gamer' na API Python (Porta 8001)")
            print("   - O Gateway buscou status 'EM_TRANSITO' na API Node.js (Porta 8002)")
        else:
            print("⚠️ AVISO: O Gateway respondeu, mas faltaram dados.")
            print(f"   - Achou dados do Python? {'Sim' if check_python else 'Não'}")
            print(f"   - Achou dados do Node? {'Sim' if check_node else 'Não'}")

except requests.exceptions.ConnectionError:
    print("❌ ERRO DE CONEXÃO: O Gateway na porta 8000 parece estar desligado.")