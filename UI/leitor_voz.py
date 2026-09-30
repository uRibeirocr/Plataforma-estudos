import json
import pyttsx3
import os

def ler_perguntas():
    # 1. Inicializa o motor de texto para fala
    engine = pyttsx3.init()

    # 2. Configura a voz para Português
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'brazil' in voice.name.lower() or 'pt-br' in voice.languages or 'portuguese' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 170)

    # 3. Carrega o ficheiro JSON (ajustado para o seu projeto)
    # Garante que procura o 'questoes.json' na mesma pasta onde este script está (pasta UI)
    caminho_base = os.path.dirname(__file__)
    caminho_json = os.path.join(caminho_base, 'questoes.json')
    
    with open(caminho_json, 'r', encoding='utf-8') as ficheiro:
        dados = json.load(ficheiro)

    # 4. Itera sobre os objetos no JSON e lê a chave "pergunta"
    for item in dados:
        texto_pergunta = item.get("pergunta")
        
        if texto_pergunta:
            print(f"A ler: {texto_pergunta}")
            engine.say(texto_pergunta)
            engine.runAndWait()

# Permite testar o script correndo-o diretamente
if __name__ == "__main__":
    ler_perguntas()