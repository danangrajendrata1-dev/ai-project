from langdetect import detect

def detect_language(text):

    try:
        lang = detect(text)

        if lang == "id":
            return "Bahasa Indonesia"

        elif lang == "en":
            return "English"

        return "Bahasa Indonesia"

    except:
        return "Bahasa Indonesia"