# Panjabi.AI
Panjabi.AI is a Python based NLP Toolkit for Punjabi language.


## Main Features

Here are a few things that this package can do:
1. Perform Sentencepiece Tokenization.
2. Provide a word2vec model to vectorize punjabi text.
3. Perform Named Entity Recognition on a sentence. Recognizing [20+ Labels](https://docs.google.com/spreadsheets/d/1U8xqkEG3SND36lH5Cc6HHqhieG6NuQN0E5F0wD5zQTo/edit?usp=sharing).
4. Find the Parts of Speech for a text. [PoS Labels](https://docs.google.com/spreadsheets/d/1U8xqkEG3SND36lH5Cc6HHqhieG6NuQN0E5F0wD5zQTo/edit#gid=2182013)
5. Translate Punjabi sentence to English and vice versa.
6. Transliterate Punjabi sentence to English and vice versa.
7. News Classification using the news summary. [Labels](https://docs.google.com/spreadsheets/d/1U8xqkEG3SND36lH5Cc6HHqhieG6NuQN0E5F0wD5zQTo/edit#gid=1734162254)

## Getting Started 

The source code can be found at https://gitlab.com/sabudh/lingua-franca/lingua-franca/

Install the Package

```
pip install punjabi.AI
```
Dependencies

```
pip install ktrain==0.31.10
pip install tensorflow==2.10.0
pip install allennlp-models==2.10.0
pip install allennlp==2.10.0
pip install torch==1.11.0
pip install torchtext==0.5.0
pip install nltk==3.7
pip install opennmt-py==2.3.0
pip install keras==2.12.0
pip install gensim==4.2.0
pip install wget

```
## Sample Run for SentencePiece Tokenizer

```
from panjabiAI.punjabi_subword_tokenizer.sentencepiece_tokenizer import punjabi_sentencepiece_tokenizer

sentence = "ਚੰਡੀਗੜ੍ਹ : ਮਾਈ ਭਾਗੋ ਆਰਮਡ ਫੋਰਸਿਜ਼ ਪ੍ਰੈਪਰੇਟਰੀ ਇੰਸਟੀਚਿਊਟ (ਏ.ਐਫ.ਪੀ.ਆਈ.) ਫਾਰ ਗਰਲਜ਼, ਐਸ.ਏ.ਐਸ. ਨਗਰ (ਮੋਹਾਲੀ) ਦੀਆਂ ਦੋ ਮਹਿਲਾ ਕੈਡਿਟਾਂ ਚੇਨੱਈ ਸਥਿਤ ਆਫੀਸਰਜ਼ ਟਰੇਨਿੰਗ ਅਕੈਡਮੀ ਵਿੱਚ ਪ੍ਰੀ-ਕਮਿਸ਼ਨ ਟਰੇਨਿੰਗ ਲਈ ਚੁਣੀਆਂ ਗਈਆਂ ਹਨ।"
sentence = punjabi_sentencepiece_tokenizer.encode_as_pieces(sentence)
print(sentence)


```

Output
```
['▁ਚੰਡੀਗੜ੍ਹ', '▁:', '▁ਮਾਈ', '▁ਭਾਗੋ', '▁ਆਰਮਡ', '▁ਫੋਰਸਿਜ਼', '▁ਪ੍ਰ', 'ੈਪ', 'ਰੇਟਰੀ', '▁ਇੰਸਟੀਚਿਊਟ', '▁(', 'ਏ', '.', 'ਐਫ', '.', 'ਪੀ', '.', 'ਆਈ', '.)', '▁ਫਾਰ', '▁ਗਰਲਜ਼', ',', '▁ਐਸ', '.', 'ਏ', '.', 'ਐਸ', '.', '▁ਨਗਰ', '▁(', 'ਮੋਹਾਲੀ', ')', '▁ਦੀਆਂ', '▁ਦੋ', '▁ਮਹਿਲਾ', '▁ਕੈਡਿਟਾਂ', '▁ਚੇਨੱਈ', '▁ਸਥਿਤ', '▁ਆਫੀ', 'ਸਰਜ਼', '▁ਟਰੇਨਿੰਗ', '▁ਅਕੈਡਮੀ', '▁ਵਿੱਚ', '▁ਪ੍ਰੀ', '-', 'ਕਮਿਸ਼ਨ', '▁ਟਰੇਨਿੰਗ', '▁ਲਈ', '▁ਚੁਣੀਆਂ', '▁ਗਈਆਂ', '▁ਹਨ', '।']
```

## Punjabi Word2Vec

### find most similar words

```
from panjabiAI.word_vector.punjabi_word2vec import punjabi_word2vec_model

most_similar = punjabi_word2vec_model.most_similar('ਰਾਣੀ')
print(most_similar)
```

Output

```
[('ਕੁਮਾਰੀ', 0.8087022304534912),
 ('ਦੇਵੀ', 0.7671301364898682),
 ('ਰਾਨੀ', 0.5875258445739746),
 ('ਬਾਲਾ', 0.5828306078910828),
 ('ਕੌਰ', 0.5682294368743896),
 ('ਰਜਨੀ', 0.560609757900238),
 ('ਮੈਡਮ', 0.5501168966293335),
 ('ਸੁਮਨ', 0.5374152660369873),
 ('ਰਾਜਰਾਣੀ', 0.5237485766410828),
 ('ਕਾਜਲ', 0.5222685933113098)]
```
### find similarity between words

```
from panjabiAI.word_vector.punjabi_word2vec import punjabi_word2vec_model
from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity([punjabi_word2vec_model['ਨਾਸ਼ਪਾਤੀ']], [punjabi_word2vec_model['ਸੇਬ']])
```

Output

```
array([[0.74444485]], dtype=float32)
```

## Sample Run for NER

### Using Ktrain Model

```
from panjabiAI.NER.ktrain import punjabi_ner

sentence = 'ਕੈਪਟਨ ਨੂੰ ਪੰਜਾਬ ਦਾ ਮੁੱਖ ਦੱਸਦੇ ਇਨ੍ਹਾਂ ਪੋਸਟਰਾਂ ਨੂੰ ਵੱਡੇ ਪੱਧਰ ਉਤੇ ਹਟਾਉਣ ਲਈ ਕਾਰਵਾਈ ਕੀਤੀ ਜਾ ਰਹੀ ਹੈ।'
predictions = punjabi_ner.model.predict(sentence)
print("Original sentence: ", sentence)
print("Output: ", predictions)
```

Output
```
Original sentence:  ਕੈਪਟਨ ਨੂੰ ਪੰਜਾਬ ਦਾ ਮੁੱਖ ਦੱਸਦੇ ਇਨ੍ਹਾਂ ਪੋਸਟਰਾਂ ਨੂੰ ਵੱਡੇ ਪੱਧਰ ਉਤੇ ਹਟਾਉਣ ਲਈ ਕਾਰਵਾਈ ਕੀਤੀ ਜਾ ਰਹੀ ਹੈ।
Output  [('ਕੈਪਟਨ', 'B-person'), ('ਨ', 'I-person'), ('ੂ', 'I-person'), ('ੰ', 'O'), ('ਪੰਜਾਬ', 'B-location'), ('ਦ', 'O'), ('ਾ', 'O'), ('ਮੁੱਖ', 'O'), ('ਦੱਸਦ', 'O'), ('ੇ', 'O'), ('ਇਨ੍ਹ', 'O'), ('ਾ', 'O'), ('ਂ', 'O'), ('ਪੋਸਟਰ', 'O'), ('ਾ', 'O'), ('ਂ', 'O'), ('ਨ', 'O'), ('ੂ', 'O'), ('ੰ', 'O'), ('ਵੱਡ', 'O'), ('ੇ', 'O'), ('ਪੱਧਰ', 'O'), ('ਉਤ', 'O'), ('ੇ', 'O'), ('ਹਟਾਉਣ', 'O'), ('ਲਈ', 'O'), ('ਕਾਰਵਾਈ', 'O'), ('ਕੀਤ', 'O'), ('ੀ', 'O'), ('ਜ', 'O'), ('ਾ', 'O'), ('ਰਹ', 'O'), ('ੀ', 'O'), ('ਹ', 'O'), ('ੈ', 'O'), ('।', 'O')]
```

### Using AllenNLP model

```
from panjabiAI.NER.allennlp.punjabi_ner import get_ner
sentence =  "ਪਾਕਿਸਤਾਨ ਨੇ ਕਰਤਾਰਪੁਰ ਲਾਂਘੇ ਦੀ ਉਸਾਰੀ ਪੂਰੀ ਕਰਨ ਲਈ ਵਿਦੇਸ਼ਾਂ 'ਚ ਵੱਸਦੇ ਸਿੱਖਾਂ ਤੋਂ ਮੰਗੀ ਮਦਦ"
predictions = get_ner(sentence)
print("Original sentence: ", sentence)
print("Output: ", predictions)
```

Output
```
Original sentence:  ਪਾਕਿਸਤਾਨ ਨੇ ਕਰਤਾਰਪੁਰ ਲਾਂਘੇ ਦੀ ਉਸਾਰੀ ਪੂਰੀ ਕਰਨ ਲਈ ਵਿਦੇਸ਼ਾਂ 'ਚ ਵੱਸਦੇ ਸਿੱਖਾਂ ਤੋਂ ਮੰਗੀ ਮਦਦ
Output  ਪਾਕਿਸਤਾਨ\U-location ਨੇ\O ਕਰਤਾਰਪੁਰ\U-location ਲਾਂਘੇ\O ਦੀ\O ਉਸਾਰੀ\O ਪੂਰੀ\O ਕਰਨ\O ਲਈ\O ਵਿਦੇਸ਼ਾਂ\O '\O ਚ\O ਵੱਸਦੇ\O ਸਿੱਖਾਂ\O ਤੋਂ\O ਮੰਗੀ\O ਮਦਦ\O 
```

## Sample Run for PoS

```
from panjabiAI.POS.pos import pos_model, pos_vocab_, pos_tags
from panjabiAI.POS import pos

sentence = "ਕੇਂਦਰੀ ਦਿੱਲੀ ਵਿੱਚ ਆਂਧਰਾ ਭਵਨ ਦੇ ਬਾਹਰ ਗਿਟਾਰ ਰਾਓ ਆਪਣੇ ਸਾਜ ਲੈ ਕੇ ਬੈਠਾ ਹੈ ਅਤੇ ਲੋਕਾਂ ਨੂੰ ਸੰਗੀਤ ਦੀ ਸਿੱਖਿਆ ਦੇ ਰਿਹਾ ਹੈ |"
predictions = pos.tag_sentence(pos_model, sentence, pos_vocab_, pos_tags)
print("Original sentence: ", sentence)
print("Output: ", predictions)
```

Output

```
Original sentence:  ਕੇਂਦਰੀ ਦਿੱਲੀ ਵਿੱਚ ਆਂਧਰਾ ਭਵਨ ਦੇ ਬਾਹਰ ਗਿਟਾਰ ਰਾਓ ਆਪਣੇ ਸਾਜ ਲੈ ਕੇ ਬੈਠਾ ਹੈ ਅਤੇ ਲੋਕਾਂ ਨੂੰ ਸੰਗੀਤ ਦੀ ਸਿੱਖਿਆ ਦੇ ਰਿਹਾ ਹੈ |
Output:  ਕੇਂਦਰੀ//N_NNP ਦਿੱਲੀ//N_NNP ਵਿੱਚ//PSP ਆਂਧਰਾ//N_NNP ਭਵਨ//N_NNP ਦੇ//PSP ਬਾਹਰ//RB ਗਿਟਾਰ//N_NNP ਰਾਓ//N_NNP ਆਪਣੇ//PR_PRF ਸਾਜ//N_NN ਲੈ//V_VM ਕੇ//V_VM_VNF ਬੈਠਾ//V_VM_VF ਹੈ//V_VAUX ਅਤੇ//CC_CCD ਲੋਕਾਂ//N_NN ਨੂੰ//PSP ਸੰਗੀਤ//N_NN ਦੀ//PSP ਸਿੱਖਿਆ//N_NN ਦੇ//PSP ਰਿਹਾ//N_NNP ਹੈ//V_VAUX |//RD_PUNC
```

## Sample Run for Machine Transliteration

### Punjabi to English transliteration
```
from panjabiAI.machine_transliteration import transliteration

word = "ਲੋਕਾਂ"
transliterated_word = transliteration.give_transliterations([word], 'pun', 'eng')
print(transliterated_word)
```

Output
```
{'ਲੋਕਾਂ': ['locaan']}
```

### English to Punjabi transliteration
```
word = "foundation"
transliterated_word = transliteration.give_transliterations([word], 'eng', 'pun')
print(transliterated_word)
```

Output
```
{'foundation': ['ਫਾਊਂਡੇਸ਼ਨ']}
```

## Sample Run for Machine Translation

### English to Punjabi
```
from panjabiAI.machine_translation.translate import translate_eng2pun

sentence = "Computer crime encompasses a broad range of activities, including computer fraud, financial crimes, scams, cybersex trafficking, and ad fraud."
translated_punjabi_text = translate_eng2pun(sentence)
print(translated_punjabi_text)
```

Output
```
ਕੰਪਿਊਟਰ ਅਪਰਾਧ ਵਿੱਚ ਕੰਪਿਊਟਰ ਧੋਖਾਧੜੀ , ਵਿੱਤੀ ਅਪਰਾਧ , ਘੁਟਾਲੇ , ਸਾਈਬਰਸੈਕਸ ਤਸਕਰੀ , ਅਤੇ ਵਿਗਿਆਪਨ ਧੋਖਾਧੜੀ ਸਮੇਤ ਗਤੀਵਿਧੀਆਂ ਦੀ ਇੱਕ ਵਿਸ਼ਾਲ ਸ਼੍ਰੇਣੀ ਸ਼ਾਮਲ ਹੈ।
```


### Punjabi to English
```
from panjabiAI.machine_translation.translate import translate_pun2eng

sentence = "ਗੈਂਗਸਟਰ ਲਾਰੈਂਸ ਬਿਸ਼ਨੋਈ ਨੂੰ ਪਟਿਆਲਾ ਹਾਊਸ ਕੋਰਟ 'ਚ ਪੇਸ਼ ਕੀਤਾ"
translated_english_text = translate_pun2eng(sentence)
print(translated_english_text)

```
Output
```
Gangster Lawrence Bishnoi produced in patiala House court
```

## Sample Run for News Classification

```
from panjabiAI.text_classification import news_classification

sentence = """ਮੌਜੂਦਾ ਸਮੇਂ ' ਚ ਮੋਟਾਪਾ ਸਭ ਤੋਂ ਵੱਡੀ ਸਮੱਸਿਆ ਬਣ ਗਿਆ ਹੈ । ਬੱਚੇ ਵੀ ਇਸ ਖ਼ਤਰੇ ਦਾ ਸਾਹਮਣਾ ਕਰ ਰਹੇ ਹਨ । ਯੂਨੀਵਰਸਿਟੀ ਆਫ ਕੋਲੰਬੀਆ ਦੇ ਵਿਗਿਆਨੀਆਂ ਨੇ ਬੱਚਿਆਂ ' ਚ ਮੋਟਾਪੇ ਦਾ ਖ਼ਤਰਾ ਵਧਾਉਣ ਵਾਲੇ ਜੀਨ ਦਾ ਪਤਾ ਲਗਾ ਲ"""
print(sentence)
predicted_class = news_classification.predict_label(sentence)
print(predicted_class)
```
Output
```
ਮੌਜੂਦਾ ਸਮੇਂ ' ਚ ਮੋਟਾਪਾ ਸਭ ਤੋਂ ਵੱਡੀ ਸਮੱਸਿਆ ਬਣ ਗਿਆ ਹੈ । ਬੱਚੇ ਵੀ ਇਸ ਖ਼ਤਰੇ ਦਾ ਸਾਹਮਣਾ ਕਰ ਰਹੇ ਹਨ । ਯੂਨੀਵਰਸਿਟੀ ਆਫ ਕੋਲੰਬੀਆ ਦੇ ਵਿਗਿਆਨੀਆਂ ਨੇ ਬੱਚਿਆਂ ' ਚ ਮੋਟਾਪੇ ਦਾ ਖ਼ਤਰਾ ਵਧਾਉਣ ਵਾਲੇ ਜੀਨ ਦਾ ਪਤਾ ਲਗਾ ਲ
('Lifestyle', 0.99904734)
```

### In case of any problem/suggestion please raise an issue in the git repo