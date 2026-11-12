import pyttsx3
import threading

def falar_texto(texto):
    """
    Recebe um texto e reproduz o áudio em segundo plano (background)
    para não travar a interface do Flet.
    """
    def executar_voz():
        engine = pyttsx3.init()
        
        # Configura a voz para Português
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'brazil' in voice.name.lower() or 'pt-br' in voice.languages or 'portuguese' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 170)
        
        print(f"Lendo em áudio: {texto}")
        engine.say(texto)
        engine.runAndWait()

    # Inicia a thread separada
    thread_voz = threading.Thread(target=executar_voz, daemon=True)
    thread_voz.start()