from googletrans import Translator  # pip install googletrans==4.0.0rc1

tr = Translator()

def translate(text, source_language_code, target_language_code):
    return tr.translate(text, src=source_language_code or 'auto', dest=target_language_code).text