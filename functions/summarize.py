import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sentencepiece

def correct_text(text):
    # API-Anfrage an LanguageTool
    response = requests.post(
        'https://api.languagetool.org/v2/check',
        data={'text': text, 'language': 'de'}
    )

    # Antwort von der API
    data = response.json()

    # Korrigierter Text initialisieren
    corrected_text = text

    # Die gefundenen Fehler durchgehen und Korrekturen anwenden
    try:
        for match in data['matches']:
            start = match['offset']
            end = start + match['length']
            replacement = match['replacements'][0]['value']  # Die erste vorgeschlagene Korrektur verwenden
            corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
        
        # print("Korrigierter Text:", corrected_text)
        return corrected_text
    except:
        return text

def summarize_text(text):
    tokenizer = AutoTokenizer.from_pretrained("ml6team/mt5-small-german-finetune-mlsum")
    model = AutoModelForSeq2SeqLM.from_pretrained("ml6team/mt5-small-german-finetune-mlsum")
    
    inputs = tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'],
        max_length=150,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # print("Zusammenfassung:", summary)
    return summary

def summarize_text_gensim(text):
    summary = summarize(text, ratio=0.2)
    print("Zusammenfassung: ", summary)

text = "Das ist einfach ein bisschen das Google Vortrags, man kann festhalten, Google ist aber die beste Firma der Welt. Zunächst haben sie verschiedene Strategien vorgestellt, damit sie nachhaltig werden. Sie betreiben schon jetzt alle ihre Rechtenzentren, der Google Cloud mit grüner Energie. Jetzt hier ist es aber wirklich alle ihre Dienstleistungen, also auch die Eingriff, rund um die Ohr mit grüner Energie zu versorgen. Anklatschaften, die ist zu 69 Prozent der Zeit bei 80 Prozent zu über 85 Prozent der Zeit. Aber da ist natürlich, geht natürlich noch mehr. Vielleicht stellen Sie, oder sammeln Sie viele Daten über Google Maps, die Sie jetzt komponenzu verfügung stellen, kostenlos. Die damit, wenn es zum Beispiel die Zulabelbauung besser sehen können, Pantlerverkehr und so weiter. Und da in der Daten auf dieser Masse der Daten ergreifen können, als vorreiter dazu ist Hamburg zu nennen. Weitere Kuhn konnten Sie in einem mir nicht genannt werden, weil es auch halt für Schifkumen ist schwierig, dann darauf Aktionen drauf zu machen. Aber der Google ist einfach nicht cool. Also wurden noch ein paar weitere Sachen, zum Beispiel Google Earth Engine für So-Lebenutzer. Die Schnittwaffe von der Unternehmung benutzt das Waldfälle, wenn er fährt. Und das ist alles Pays-Reault, also es ist extrem gut skaliert. Es kaltiert sich jetzt meist auf den Google nicht, aber damit kann halt in der Zukunft viel erreicht werden. Also viel Fortschrift erreicht werden. Und das ist eben halt sehr gut."

# summarize_text(text)