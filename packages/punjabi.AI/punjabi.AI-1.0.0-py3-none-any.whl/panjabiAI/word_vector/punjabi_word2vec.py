import sys
import os
sys.path.insert(0, os.getcwd())

from gensim.models import KeyedVectors
from panjabiAI.utils import download_from_s3
from pathlib import Path
CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "word_vectors" / "cache"
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/word2vec/punjabi_word2vec.vec")

model_path = str(CACHE_DIRECTORY / "punjabi_word2vec.vec")

punjabi_word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=False)

if __name__ == "__main__":
    most_similar = punjabi_word2vec_model.most_similar('ਰਾਣੀ')
    print(most_similar)