# Usa uma imagem oficial do Python 3.10 (onde o Spyne funciona)
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema necessárias para compilar lxml (se precisar)
RUN apt-get update && apt-get install -y gcc libxml2-dev libxslt-dev

# Copia o requirements e instala
# (Vou garantir que instalamos as versões certas direto aqui para não depender do arquivo)
RUN pip install spyne lxml werkzeug==2.0.3

# Copia o código fonte para dentro do container
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o servidor
CMD ["python", "main.py"]