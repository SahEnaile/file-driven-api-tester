# Usa uma imagem oficial e leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script de automação para dentro do container
COPY runner.py .

# Cria as pastas padrão caso não existam
RUN mkdir -p payloads_entrada respostas_saida

# Comando padrão ao rodar o container
CMD ["python", "runner.py"]