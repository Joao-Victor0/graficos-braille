#!/usr/bin/env bash
set -o errexit

echo "Baixando o motor ffmpeg..."
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz

echo "Organizando os arquivos..."
mkdir -p bin
cp ffmpeg-*-static/ffmpeg bin/
cp ffmpeg-*-static/ffprobe bin/

echo "Limpando os arquivos temporários..."
rm -rf ffmpeg-release-amd64-static.tar.xz ffmpeg-*-static

echo "Instalando pacotes Python..."
pip install --upgrade pip
pip install -r requirements.txt