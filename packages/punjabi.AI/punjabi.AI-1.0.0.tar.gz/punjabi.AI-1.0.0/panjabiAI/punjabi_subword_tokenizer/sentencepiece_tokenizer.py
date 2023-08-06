import sys
import os
sys.path.insert(0, os.getcwd())

import sentencepiece as spm
from panjabiAI.utils import download_from_s3
from pathlib import Path
CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "tokenizer" / "cache"
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/pan_subword.vocab")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/pan_subword.model")

punjabi_sentencepiece_tokenizer = spm.SentencePieceProcessor(str(CACHE_DIRECTORY / 'pan_subword.model'))

if __name__ == "__main__":
    sentence = "ਗੈਂਗਸਟਰ ਲਾਰੈਂਸ ਬਿਸ਼ਨੋਈ ਨੂੰ ਪਟਿਆਲਾ ਹਾਊਸ ਕੋਰਟ 'ਚ ਪੇਸ਼ ਕੀਤਾ"
    sentence = " ".join(punjabi_sentencepiece_tokenizer.encode_as_pieces(sentence))
    print(sentence)
