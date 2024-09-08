import whisper
import os

# import warnings
# warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def transcribe(filename, folder='Audios'):
    model = whisper.load_model("base")

    audio_file = os.path.join(os.path.dirname(__file__), '..', folder, filename)

    result = model.transcribe(audio_file, language="de")

    return result["text"]