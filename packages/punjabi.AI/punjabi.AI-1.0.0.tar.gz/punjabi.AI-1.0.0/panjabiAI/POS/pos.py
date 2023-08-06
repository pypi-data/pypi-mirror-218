import sys
import os
sys.path.insert(0, os.getcwd())

from panjabiAI.utils import download_from_s3
import torch.nn as nn
import torch
import pickle
import re
from pathlib import Path
CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "pos" / "cache"
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/POS/pos_model.zip", extract_archive=True)

class BiLSTMPOSTagger(nn.Module):
    def __init__(self, 
                 input_dim, 
                 embedding_dim, 
                 hidden_dim, 
                 output_dim, 
                 n_layers, 
                 bidirectional, 
                 dropout, 
                 pad_idx):
        
        super().__init__()
        
        self.embedding = nn.Embedding(input_dim, embedding_dim, padding_idx = pad_idx)
        
        self.lstm = nn.LSTM(embedding_dim, 
                            hidden_dim, 
                            num_layers = n_layers, 
                            bidirectional = bidirectional,
                            dropout = dropout if n_layers > 1 else 0)
        
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, text):
        
        #pass text through embedding layer
        embedded = self.dropout(self.embedding(text))
        
        #pass embeddings into LSTM
        outputs, (hidden, cell) = self.lstm(embedded)
        
        predictions = self.fc(self.dropout(outputs))
        return predictions

def clean_text(text):
    """clean the punjabi sentence, normalize the puntuation marks, 
    remove other lanaguage charatcers, multiple spaces..

    Args:
        text (str): input punjabi text
    Returns:
        str: cleaned punjabi text
    """
    text = re.sub("।", " | ", text)
    text = re.sub('\n+', '\n', text).strip()
    text = re.sub("\s?\n\s\n\s?", "\n", text)
    text = re.sub('\n+', '\n', text).strip()
    text = re.sub(r"https?://\S+", "<URL>", text)
    text = re.sub(r"\www\.\S+\.\S+", "<URL>", text)
    pattern = r'[%,\.;:\-\/\\\[\]\{\}\|(\)"\'\*?!#&\$€¥£₹~]'
    text = re.sub(pattern, ' \g<0> ', text)
    text = re.sub('[a-zA-z]', ' ', text)
    text = re.sub("\s?\n\s?", "\n", text)
    text = re.sub(" +", " ", text)
    text = re.sub('\n+', '\n', text)
    text = re.sub(", ,", ",", text)
    return text

def read_pkl(path):
    pkl_file = open(path, 'rb')
    vocab = pickle.load(pkl_file)
    pkl_file.close()
    return vocab

def init_model(vocab_path, tags_path, model_path):
    """load the model into memory

    Args:
        vocab_path (str): path to the vocab file
        tags_path (str): path to the pos tags file
        model_path (str): path to model

    Returns:
        model, vocab_, tags
    """
    vocab_ = read_pkl(vocab_path)
    tags = read_pkl(tags_path)
    INPUT_DIM = len(vocab_)
    EMBEDDING_DIM = 300
    HIDDEN_DIM = 128
    OUTPUT_DIM = len(tags)
    N_LAYERS = 2
    BIDIRECTIONAL = True
    DROPOUT = 0.25
    PAD_IDX = 1

    model = BiLSTMPOSTagger(INPUT_DIM, 
                            EMBEDDING_DIM, 
                            HIDDEN_DIM, 
                            OUTPUT_DIM, 
                            N_LAYERS, 
                            BIDIRECTIONAL, 
                            DROPOUT, 
                            PAD_IDX)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu') ))
    return model, vocab_, tags

def tag_sentence(model, sentence,vocab_, tags, device='cpu'):
    """use the loaded model to tag a punjabi sentence

    Args:
        model : pos model
        sentence (str): punjabi sentence
        vocab_ : vocabulary
        tags : pos tags
        device (str, optional): Defaults to 'cpu'.

    Returns:
        str: pos tagged sentence
    """
    try:
        
        output = ''
        model.eval()
        tokens = [token for token in sentence.split(' ')]
    
        if vocab_:
            tokens = [t for t in tokens]
            
        numericalized_tokens = [vocab_.stoi[t] for t in tokens]

        unks = [t for t, n in zip(tokens, numericalized_tokens) if n == 0]
        token_tensor = torch.LongTensor(numericalized_tokens)
        token_tensor = token_tensor.unsqueeze(-1).to(device)
        predictions = model(token_tensor)
        top_predictions = predictions.argmax(-1)
        predicted_tags = [tags.itos[t.item()] for t in top_predictions]
        
        for token, pred_tag in zip(tokens, predicted_tags):
            output += token + '//' + pred_tag + ' '
        
        return output.strip()
    except Exception as e:
        print(e)
        return ""


model_path = CACHE_DIRECTORY / 'model' / 'pos_punjabi_bilstm.zip'
vocab_path = CACHE_DIRECTORY / 'model' / 'vocab.pkl'
tags_path = CACHE_DIRECTORY / 'model' / 'tags.pkl'
pos_model, pos_vocab_, pos_tags = init_model(vocab_path, tags_path, model_path)

