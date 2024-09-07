#!/usr/bin/python3

import gi
gi.require_version('Gio', '2.0')
gi.require_version('Gedit', '3.0')

from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

def ajustar_velocidade(audio_path, fator):
    # Carregar o arquivo de áudio
    audio = AudioSegment.from_file(audio_path)
    
    # Ajustar a velocidade (fator > 1 acelera, fator < 1 desacelera)
    audio_modificado = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * fator)
    })
    audio_modificado = audio_modificado.set_frame_rate(audio.frame_rate)
    
    # Salvar o áudio modificado em um arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file.close()
    audio_modificado.export(temp_file.name, format="wav")
    
    # Reproduzir o áudio modificado
    with open(temp_file.name, 'rb') as f:
        play(AudioSegment.from_wav(f))
    
    # Remover o arquivo temporário
    os.remove(temp_file.name)

# Exemplo de uso
#arquivo_audio = "caminho/para/seu/audio.mp3"
#ajustar_velocidade(arquivo_audio, fator=1.5)  # Acelera o áudio em 50%

