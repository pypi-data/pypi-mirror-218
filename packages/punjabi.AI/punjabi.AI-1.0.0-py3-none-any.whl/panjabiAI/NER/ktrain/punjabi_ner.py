import sys
import os
sys.path.insert(0, os.getcwd())

from panjabiAI.utils import download_from_s3
from pathlib import Path
import ktrain
import tensorflow as tf

CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "ktrain_ner" / "cache"
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/NER/ktrain/ktrain_ner_model.zip", extract_archive=True)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        
        # Memory growth must be set before GPUs have been initialized
        print(e)
        

predictor = ktrain.load_predictor(str(CACHE_DIRECTORY / 'ner_model'))
model = ktrain.get_predictor(predictor.model, predictor.preproc)

def predict_ner(sentence):
    """predict ner for a given sentence

    Args:
        sentence (str): punjabi sentence for which NER is to be inferred

    Returns:
        str :tagged sentence
    """
    
    output = model.predict(sentence)
    return output
    



