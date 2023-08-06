import sys
import os
sys.path.insert(0, os.getcwd())
from panjabiAI.utils import download_from_s3
from allennlp.predictors import Predictor

model_path = "https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/NER/allennlp/model.tar.gz"
predictor = Predictor.from_path(model_path)
def get_ner(sentence):
    """predict ner for a given sentence

    Args:
        sentence (str): punjabi sentence for which NER is to be inferred

    Returns:
        str :tagged sentence
    """
    
    results = predictor.predict(sentence=sentence)
    output = ""
    for word, tag in zip(results["words"], results["tags"]):
        output += word + '\\'
        output += tag + ' ' 
    return output

