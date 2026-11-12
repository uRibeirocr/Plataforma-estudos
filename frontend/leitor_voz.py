"""Leitor de perguntas em voz alta (opcional).

Depende de `pyttsx3` e de uma voz instalada no sistema. Se qualquer parte faltar, o app
continua funcionando normalmente, só sem áudio.
"""
import threading

try:  # pyttsx3 é opcional
    import pyttsx3
except Exception:  # pragma: no cover - depende do ambiente
    pyttsx3 = None

_trava = threading.Lock()


def disponivel() -> bool:
    return pyttsx3 is not None


def falar_texto(texto: str) -> None:
    """Lê `texto` em segundo plano, sem travar a interface. Silencioso se não houver voz."""
    if not texto or not disponivel():
        return

    def executar():
        with _trava:  # uma fala por vez
            try:
                engine = pyttsx3.init()
                for voz in engine.getProperty("voices"):
                    nome = (voz.name or "").lower()
                    idiomas = [str(i).lower() for i in (voz.languages or [])]
                    if "brazil" in nome or "portuguese" in nome or any("pt" in i for i in idiomas):
                        engine.setProperty("voice", voz.id)
                        break
                engine.setProperty("rate", 170)
                engine.say(texto)
                engine.runAndWait()
            except Exception as exc:  # sem driver de áudio, sem voz etc.
                print(f"[voz] indisponível: {exc}")

    threading.Thread(target=executar, daemon=True).start()
