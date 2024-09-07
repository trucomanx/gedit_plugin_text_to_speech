#!/usr/bin/python3

from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

def ajustar_velocidade(audio_path, fator):
    # Carregar o arquivo de áudio
    audio = AudioSegment.from_file(audio_path)
    
    # Ajustar a velocidade sem alterar o pitch
    audio_modificado = audio.speedup(playback_speed=fator)
    
    # Salvar o áudio modificado em um arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file.close()
    audio_modificado.export(temp_file.name, format="wav")
    
    # Reproduzir o áudio modificado
    with open(temp_file.name, 'rb') as f:
        play(AudioSegment.from_wav(f))
    
    # Remover o arquivo temporário
    os.remove(temp_file.name)


