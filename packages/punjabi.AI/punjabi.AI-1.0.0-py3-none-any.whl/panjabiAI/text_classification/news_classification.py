import sys
import os
sys.path.insert(0, os.getcwd())

from panjabiAI.utils import download_from_s3
from keras.preprocessing.text import tokenizer_from_json
from keras.utils import pad_sequences
from tensorflow import keras
import numpy as np 
import json

from pathlib import Path
CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "classification" / "cache"
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/text_classification/tokenizer_v1.json")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/text_classification/text_classification_LSTM.zip", extract_archive=True)

tokenizer_path = CACHE_DIRECTORY / "tokenizer_v1.json"
model_path = CACHE_DIRECTORY / "text_classification_LSTM"
model = keras.models.load_model(model_path, compile=False)
model.compile()
labels = {1: 'Lifestyle', 0: 'Entertainment', 2: 'National', 3: 'Sports', 4: 'World'}

def load_tokenizer():
    """load the tokenizer from json

    Returns:
        punjabi tokenizer
    """
    with open(tokenizer_path) as f:
        data = json.load(f)
    tokenizer = tokenizer_from_json(data)
    return tokenizer

tokenizer =  load_tokenizer()

def predict_label(pb_text):
    """_summary_

    Args:
        tokenizer :punjabi tokenizer_
        pb_text (str): input text

    Returns:
        pred_label (str): pedicted label for the sentence
        prob (float): probability with which the label is predicted
    """
    x = tokenizer.texts_to_sequences([pb_text])
    x = pad_sequences(x, maxlen=94)
    pred = model.predict(x)
    idx = np.argmax(pred)
    pred_label = labels[idx]
    prob = pred[0][idx]
    return pred_label, prob


if __name__ == "__main__":
    
    # sentence = """ਪਿੰਡ ਮਜਾਲ ਵਿਖੇ ਗ੍ਰਿਫ਼ਤਾਰ ਕਰਨ ਆਈ ਪੁਲਿਸ ਦੇ ਡਰੋਂ ਇਕ ਵਿਅਕਤੀ ਨੇ ਸਿਰ ' ਚ ਗੋਲ਼ੀ ਮਾਰ ਕੇ ਖ਼ੁਦਕੁਸ਼ੀ ਕਰ ਲਈ । ਵਿਅਕਤੀ ਦੀ ਪਛਾਣ ਜਗਤਾਰ ਸਿੰਘ 45 ਸਾਲ ਵਾਸੀ ਪਿੰਡ ਮਜਾਲ ਦੇ ਤੌਰ ' ਤੇ ਹੋਈ ਹੈ । ਘਟਨਾ ਤੋਂ ਬਾਅਦ ਹੰਗਾ"""
    sentence = """ਮੌਜੂਦਾ ਸਮੇਂ ' ਚ ਮੋਟਾਪਾ ਸਭ ਤੋਂ ਵੱਡੀ ਸਮੱਸਿਆ ਬਣ ਗਿਆ ਹੈ । ਬੱਚੇ ਵੀ ਇਸ ਖ਼ਤਰੇ ਦਾ ਸਾਹਮਣਾ ਕਰ ਰਹੇ ਹਨ । ਯੂਨੀਵਰਸਿਟੀ ਆਫ ਕੋਲੰਬੀਆ ਦੇ ਵਿਗਿਆਨੀਆਂ ਨੇ ਬੱਚਿਆਂ ' ਚ ਮੋਟਾਪੇ ਦਾ ਖ਼ਤਰਾ ਵਧਾਉਣ ਵਾਲੇ ਜੀਨ ਦਾ ਪਤਾ ਲਗਾ ਲ"""
    print(sentence)
    print(predict_label(sentence))