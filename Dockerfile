# Imagem
FROM python:3.10-alpine

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala dependências do sistema: ffmpeg, build tools
RUN apk add --no-cache ffmpeg build-base

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Comando para iniciar o app
CMD ["python", "app.py"]
