#!/usr/bin/env bash
# Interrompe a execução caso ocorra algum erro
set -o errexit

# Atualiza os pacotes do Linux e instala o ffmpeg
apt-get update
apt-get install -y ffmpeg

# Instala as dependências do Python
pip install --upgrade pip
pip install -r requirements.txt