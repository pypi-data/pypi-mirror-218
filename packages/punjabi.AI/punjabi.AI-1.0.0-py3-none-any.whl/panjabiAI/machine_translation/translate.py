import sys
import os
sys.path.insert(0, os.getcwd())

from onmt.translate.translator import build_translator
from panjabiAI.utils import download_from_s3
from nltk.tokenize import word_tokenize
from argparse import Namespace
import sentencepiece as spm
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")
CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = (CACHE_ROOT / "machine_translation/cache")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/eng2pun_step_65000.pt")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/pun2eng_step_165000.pt")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/pan_subword.model")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/pan_subword.vocab")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/eng_subword.model")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_translation/eng_subword.vocab")

path = CACHE_DIRECTORY / 'eng2pun_step_65000.pt'
opt = Namespace(alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', data_type='text', dump_beam='', int8= False, fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', max_length=100, max_sent_length=None, min_length=0, models=[path], n_best=1, output=str(CACHE_ROOT / "machine_translation/output"), phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, random_sampling_topp= 1, ratio=-0.0, replace_unk=False, ban_unk_token= False, with_score= False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt_prefix= False, tgt=None, verbose=False)
eng2pun_translator = build_translator(opt, report_score=False)

path = CACHE_DIRECTORY / 'pun2eng_step_165000.pt'
opt = Namespace(alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', data_type='text', dump_beam='', int8= False, fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', max_length=100, max_sent_length=None, min_length=0, models=[path], n_best=1, output=str(CACHE_ROOT / "machine_translation/output"), phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, random_sampling_topp= 1, ratio=-0.0, replace_unk=False, ban_unk_token= False, with_score= False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt_prefix= False, tgt=None, verbose=False)
pun2eng_translator = build_translator(opt, report_score=False)


punjabi_sentencepiece_tokenizer = spm.SentencePieceProcessor(str(CACHE_DIRECTORY / 'pan_subword.model'))
english_sentencepiece_tokenizer = spm.SentencePieceProcessor(str(CACHE_DIRECTORY / 'eng_subword.model'))

def preprocess(sentence):
    sentence = sentence.lower()
    sentence = " ".join(word_tokenize(sentence))
    return sentence

def translate_eng2pun(sentence):
    """translates the english text to punjabi

    Args:
        sentence (str): input english text

    Returns:
        str: translated punjabi text_
    """
    sentence = preprocess(sentence)
    sentence = " ".join(english_sentencepiece_tokenizer.encode_as_pieces(sentence))
    output = eng2pun_translator.translate([sentence], batch_size=1)
    TranslatedText = output[1][0][0]
    TranslatedText_decoded = punjabi_sentencepiece_tokenizer.decode(TranslatedText.split(' '))
    return TranslatedText_decoded

def translate_pun2eng(sentence):
    """translates the punjabi text to english

    Args:
        sentence (str): input punjabi text

    Returns:
        str: translated english text_
    """
    sentence = preprocess(sentence)
    sentence = " ".join(punjabi_sentencepiece_tokenizer.encode_as_pieces(sentence))
    output = pun2eng_translator.translate([sentence], batch_size=1)
    TranslatedText = output[1][0][0]
    TranslatedText_decoded = english_sentencepiece_tokenizer.decode(TranslatedText.split(' '))
    TranslatedText_decoded_postprocessed = postprocessing(TranslatedText_decoded)
    return TranslatedText_decoded_postprocessed

def postprocessing(sentence):
    """post process the translated english text. 
       this included capitolizing the locations, organizations etc

    Args:
        sentence (str): translated english text

    Returns:
        str: processed text
    """
    updated_sentence = sentence
    sent_obj = nlp(sentence)
    for i, word in enumerate(sent_obj.ents):
        
        if i == 0:
            if word.label_ == 'GPE' and len(word.text) <= 4:
                updated_sentence = updated_sentence.replace(word.text, word.text.upper(), 1)
            
            elif word.label_ == 'ORG' and len(word.text) <= 5:
                updated_sentence = updated_sentence.replace(word.text, word.text.upper(), 1)
        else:            
            if word.label_ == 'GPE' and len(word.text) < 4:
                updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.upper())

            elif word.label_ == 'ORG' and len(word.text) <= 5:
                updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.upper())

            elif word.label_ in ['DATE', 'ORDINAL', 'TIME', 'CARDINAL', 'QUANTITY']:
                pass
            else:
                for term in word.text.split():
                    updated_sentence = updated_sentence.replace( " " + term, " " + term.capitalize())
            
    sent_obj = nlp(updated_sentence)  
    for i, word in enumerate(sent_obj):
        if i == 0 and word.text.islower():
            updated_sentence = updated_sentence.replace(word.text, word.text.capitalize(), 1)
            
        elif word.pos_ in ['PROPN', 'NUM'] and  word.text.islower():
            updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.capitalize())            
    
    return updated_sentence

if __name__ == "__main__":
    sentence = "ਗੈਂਗਸਟਰ ਲਾਰੈਂਸ ਬਿਸ਼ਨੋਈ ਨੂੰ ਪਟਿਆਲਾ ਹਾਊਸ ਕੋਰਟ 'ਚ ਪੇਸ਼ ਕੀਤਾ"
    translated_english_text = translate_pun2eng(sentence)
    print(translated_english_text)

    sentence = "Computer crime encompasses a broad range of activities, including computer fraud, financial crimes, scams, cybersex trafficking, and ad fraud."
    translated_punjabi_text = translate_eng2pun(sentence)
    print(translated_punjabi_text)