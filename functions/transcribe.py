import whisper
import os

model = whisper.load_model("base")

audio_file = os.path.join(os.path.dirname(__file__), '..', 'Audios', 'test.mp3')

result = model.transcribe(audio_file, language="de")

print(result["text"])