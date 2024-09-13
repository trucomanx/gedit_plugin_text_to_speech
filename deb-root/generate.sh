#!/bin/bash

################################################################################
VERSION=$(grep "^Version=" ../plugins/text_to_speech.plugin | cut -d'=' -f2)
ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)

mkdir -p gedit-plugin-text-to-speech/usr/lib/$ARCH/gedit/plugins
mkdir -p gedit-plugin-text-to-speech/DEBIAN

# Caminho para o arquivo de serviço
TEMP_FILEPATH="gedit-plugin-text-to-speech/DEBIAN/control"

# Conteúdo do arquivo de serviço (substitua os placeholders)
STRING_CONTENT="Package: gedit-plugin-text-to-speech
Version: $VERSION
Section: editors
Priority: optional
Architecture: all
Depends: gedit (>= 3.0), python3, python3-gi, gir1.2-gtk-3.0
Maintainer: Fernando Pujaico Rivera <fernando.pujaico.rivera@gmail.com>
Description: Text to speech plugin require https://github.com/trucomanx/text_to_speech_program .
"

# Cria o arquivo de serviço temporário e escreve o conteúdo nele
echo "$STRING_CONTENT" | tee $TEMP_FILEPATH > /dev/null

cp -r ../plugins/* gedit-plugin-text-to-speech/usr/lib/$ARCH/gedit/plugins

dpkg-deb --build gedit-plugin-text-to-speech

mv gedit-plugin-text-to-speech.deb gedit-plugin-text-to-speech_${VERSION}.deb
