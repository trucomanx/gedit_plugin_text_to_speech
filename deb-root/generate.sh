#!/bin/bash

# Defina as variáveis que você deseja substituir
USER=$(whoami)  # Nome do usuário atual
GROUP=$(id -gn) # Nome do grupo principal do usuário atual
HOME_DIR=$HOME  # Diretório home do usuário
USERID=$(id -u $USER) # User ID
PROGRAM_PATH=$(which clipboard-tts-client) # Path of some program
PYTHON_NAME=$(python3 --version | awk '{print "python" $2}' | sed 's/\.[0-9]*$//') # PYthon name

mkdir -p gedit-plugin-text-to-speech/usr/share/gedit/plugins
mkdir -p gedit-plugin-text-to-speech/DEBIAN

# Caminho para o arquivo de serviço
TEMP_FILEPATH="gedit-plugin-text-to-speech/DEBIAN/control"

# Conteúdo do arquivo de serviço (substitua os placeholders)
STRING_CONTENT="[Desktop Entry]
Package: gedit-plugin-text-to-speech
Version: 0.1.0
Section: editors
Priority: optional
Architecture: all
Depends: gedit (>= 3.0), python3, python3-gi, gir1.2-gtk-3.0
Maintainer: Fernando Pujaico Rivera <fernando.pujaico.rivera@gmail.com>
Description: Text to speech plugin require https://github.com/trucomanx/text_to_speech_program .
"

# Cria o arquivo de serviço temporário e escreve o conteúdo nele
echo "$STRING_CONTENT" | tee $TEMP_FILEPATH > /dev/null

cp -r ../plugins/* gedit-plugin-text-to-speech/usr/share/gedit/plugins

