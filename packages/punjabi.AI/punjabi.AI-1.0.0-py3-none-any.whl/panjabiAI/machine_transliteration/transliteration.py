import sys
import os
sys.path.insert(0, os.getcwd())

from panjabiAI.utils import download_from_s3
import torch.nn as nn
import numpy as np
import torch
import random
from pathlib import Path

CACHE_ROOT = Path(Path.home() / ".panjabi.AI")
CACHE_DIRECTORY = CACHE_ROOT / "transliteration/cache"

download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_transliteration/eng2pun_translit_model.pth")
download_from_s3(CACHE_DIRECTORY, url_="https://sabudh-linguafranca-models.s3.ap-south-1.amazonaws.com/models/machine_transliteration/pun2eng_translit_model.pth")
dir = CACHE_DIRECTORY
enc2dec_hid = True
device = 'cuda' if torch.cuda.is_available() else 'cpu'
indoarab_num = [chr(alpha) for alpha in range(48, 58)]
english_lower_script = [chr(alpha) for alpha in range(97, 123)]

gurmukhi_script = ['ੈ','ੱ','ਬ','ਫ','ਂ','ਡ','ੇ','ਨ','ਆ','ਖ','ਢ','ਘ','ਾ','ਅ','ਸ','ਯ','ਲ','ਥ','ੜ','ੋ','ਦ',
                    'ਮ','ਖ਼','ਲ਼','ਠ','਼','ੀ','ਤ','ਈ','ਹ','ਪ','ਊ','ਟ','ਕ','੍','ਝ','ਭ','ਸ਼','ਣ','ਐ','ਿ','ੰ',
                    'ਫ਼','ਧ','ਉ','ਇ','ੁ','ੲ','ਔ','ਵ','ਗ਼','ਓ','ੌ','ਜ','ਚ','ਏ','ਰ','ਜ਼','ਛ','ੂ','ਗ', chr(0x200c)
                    , chr(0x200d)]

matras = ['ੈ','ੱ','ਂ','ੇ','ਾ','ੋ','਼','ੀ','੍','ਿ','ੰ','ੁ','ੌ','ੂ']
class Encoder(nn.Module):
    '''
    Simple RNN based encoder network
    '''
    def __init__(self, input_dim, embed_dim, hidden_dim ,
                       rnn_type = 'gru', layers = 1,
                       bidirectional =False,
                       dropout = 0, device = "gpu"):
        super(Encoder, self).__init__()

        self.input_dim = input_dim #src_vocab_sz
        self.enc_embed_dim = embed_dim
        self.enc_hidden_dim = hidden_dim
        self.enc_rnn_type = rnn_type
        self.enc_layers = layers
        self.enc_directions = 2 if bidirectional else 1
        self.device = device

        self.embedding = nn.Embedding(self.input_dim, self.enc_embed_dim)

        if self.enc_rnn_type == "gru":
            self.enc_rnn = nn.GRU(input_size= self.enc_embed_dim,
                          hidden_size= self.enc_hidden_dim,
                          num_layers= self.enc_layers,
                          bidirectional= bidirectional)
        elif self.enc_rnn_type == "lstm":
            self.enc_rnn = nn.LSTM(input_size= self.enc_embed_dim,
                          hidden_size= self.enc_hidden_dim,
                          num_layers= self.enc_layers,
                          bidirectional= bidirectional)
        else:
            raise Exception("unknown RNN type mentioned")

    def forward(self, x, x_sz, hidden = None):
        '''
        x_sz: (batch_size, 1) -  Unpadded sequence lengths used for pack_pad

        Return:
            output: (batch_size, max_length, hidden_dim)
            hidden: (n_layer*num_directions, batch_size, hidden_dim) | if LSTM tuple -(h_n, c_n)

        '''
        batch_sz = x.shape[0]
        # x: batch_size, max_length, enc_embed_dim
        x = self.embedding(x)

        ## pack the padded data
        # x: max_length, batch_size, enc_embed_dim -> for pack_pad
        x = x.permute(1,0,2)
        x = nn.utils.rnn.pack_padded_sequence(x, x_sz, enforce_sorted=False) # unpad

        # output: packed_size, batch_size, enc_embed_dim --> hidden from all timesteps
        # hidden: n_layer**num_directions, batch_size, hidden_dim | if LSTM (h_n, c_n)
        output, hidden = self.enc_rnn(x)

        ## pad the sequence to the max length in the batch
        # output: max_length, batch_size, enc_emb_dim*directions)
        output, _ = nn.utils.rnn.pad_packed_sequence(output)

        # output: batch_size, max_length, hidden_dim
        output = output.permute(1,0,2)

        return output, hidden


class Decoder(nn.Module):
    '''
    Used as decoder stage
    '''
    def __init__(self, output_dim, embed_dim, hidden_dim,
                       rnn_type = 'gru', layers = 1,
                       use_attention = True,
                       enc_outstate_dim = None, # enc_directions * enc_hidden_dim
                       dropout = 0, device = "gpu"):
        super(Decoder, self).__init__()

        self.output_dim = output_dim #tgt_vocab_sz
        self.dec_hidden_dim = hidden_dim
        self.dec_embed_dim = embed_dim
        self.dec_rnn_type = rnn_type
        self.dec_layers = layers
        self.use_attention = use_attention
        self.device = device
        if self.use_attention:
            self.enc_outstate_dim = enc_outstate_dim if enc_outstate_dim else hidden_dim
        else:
            self.enc_outstate_dim = 0


        self.embedding = nn.Embedding(self.output_dim, self.dec_embed_dim)

        if self.dec_rnn_type == 'gru':
            self.dec_rnn = nn.GRU(input_size= self.dec_embed_dim + self.enc_outstate_dim, # to concat attention_output
                          hidden_size= self.dec_hidden_dim, # previous Hidden
                          num_layers= self.dec_layers,
                          batch_first = True )
        elif self.dec_rnn_type == "lstm":
            self.dec_rnn = nn.LSTM(input_size= self.dec_embed_dim + self.enc_outstate_dim, # to concat attention_output
                          hidden_size= self.dec_hidden_dim, # previous Hidden
                          num_layers= self.dec_layers,
                          batch_first = True )
        else:
            raise Exception("unknown RNN type mentioned")

        self.fc = nn.Sequential(
            nn.Linear(self.dec_hidden_dim, self.dec_embed_dim), nn.LeakyReLU(),
            # nn.Linear(self.dec_embed_dim, self.dec_embed_dim), nn.LeakyReLU(), # removing to reduce size
            nn.Linear(self.dec_embed_dim, self.output_dim),
            )

        ##----- Attention ----------
        if self.use_attention:
            self.W1 = nn.Linear( self.enc_outstate_dim, self.dec_hidden_dim)
            self.W2 = nn.Linear( self.dec_hidden_dim, self.dec_hidden_dim)
            self.V = nn.Linear( self.dec_hidden_dim, 1)

    def attention(self, x, hidden, enc_output):
        '''
        x: (batch_size, 1, dec_embed_dim) -> after Embedding
        enc_output: batch_size, max_length, enc_hidden_dim *num_directions
        hidden: n_layers, batch_size, hidden_size | if LSTM (h_n, c_n)
        '''

        ## perform addition to calculate the score

        # hidden_with_time_axis: batch_size, 1, hidden_dim
        ## hidden_with_time_axis = hidden.permute(1, 0, 2) ## replaced with below 2lines
        hidden_with_time_axis = torch.sum(hidden, axis=0)

        hidden_with_time_axis = hidden_with_time_axis.unsqueeze(1)

        # score: batch_size, max_length, hidden_dim
        score = torch.tanh(self.W1(enc_output) + self.W2(hidden_with_time_axis))

        # attention_weights: batch_size, max_length, 1
        # we get 1 at the last axis because we are applying score to self.V
        attention_weights = torch.softmax(self.V(score), dim=1)

        # context_vector shape after sum == (batch_size, hidden_dim)
        context_vector = attention_weights * enc_output
        context_vector = torch.sum(context_vector, dim=1)
        # context_vector: batch_size, 1, hidden_dim
        context_vector = context_vector.unsqueeze(1)

        # attend_out (batch_size, 1, dec_embed_dim + hidden_size)
        attend_out = torch.cat((context_vector, x), -1)

        return attend_out, attention_weights

    def forward(self, x, hidden, enc_output):
        '''
        x: (batch_size, 1)
        enc_output: batch_size, max_length, dec_embed_dim
        hidden: n_layer, batch_size, hidden_size | lstm: (h_n, c_n)
        '''
        if (hidden is None) and (self.use_attention is False):
            raise Exception( "No use of a decoder with No attention and No Hidden")

        batch_sz = x.shape[0]

        if hidden is None:
            # hidden: n_layers, batch_size, hidden_dim
            hid_for_att = torch.zeros((self.dec_layers, batch_sz,
                                    self.dec_hidden_dim )).to(self.device)
        elif self.dec_rnn_type == 'lstm':
            hid_for_att = hidden[0] # h_n
        else:
            hid_for_att = hidden

        # x (batch_size, 1, dec_embed_dim) -> after embedding
        x = self.embedding(x)

        if self.use_attention:
            # x (batch_size, 1, dec_embed_dim + hidden_size) -> after attention
            # aw: (batch_size, max_length, 1)
            x, aw = self.attention( x, hid_for_att, enc_output)
        else:
            x, aw = x, 0

        # passing the concatenated vector to the GRU
        # output: (batch_size, n_layers, hidden_size)
        # hidden: n_layers, batch_size, hidden_size | if LSTM (h_n, c_n)
        output, hidden = self.dec_rnn(x, hidden) if hidden is not None else self.dec_rnn(x)

        # output :shp: (batch_size * 1, hidden_size)
        output =  output.view(-1, output.size(2))

        # output :shp: (batch_size * 1, output_dim)
        output = self.fc(output)

        return output, hidden, aw



class Seq2Seq(nn.Module):
    '''
    Used to construct seq2seq architecture with encoder decoder objects
    '''
    def __init__(self, encoder, decoder, pass_enc2dec_hid=False, dropout = 0, device = "cpu"):
        super(Seq2Seq, self).__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        self.pass_enc2dec_hid = pass_enc2dec_hid

        if self.pass_enc2dec_hid:
            assert decoder.dec_hidden_dim == encoder.enc_hidden_dim, "Hidden Dimension of encoder and decoder must be same, or unset `pass_enc2dec_hid`"
        if decoder.use_attention:
            assert decoder.enc_outstate_dim == encoder.enc_directions*encoder.enc_hidden_dim,"Set `enc_out_dim` correctly in decoder"
        assert self.pass_enc2dec_hid or decoder.use_attention, "No use of a decoder with No attention and No Hidden from Encoder"


    def forward(self, src, tgt, src_sz, teacher_forcing_ratio = 0):
        '''
        src: (batch_size, sequence_len.padded)
        tgt: (batch_size, sequence_len.padded)
        src_sz: [batch_size, 1] -  Unpadded sequence lengths
        '''
        batch_size = tgt.shape[0]

        # enc_output: (batch_size, padded_seq_length, enc_hidden_dim*num_direction)
        # enc_hidden: (enc_layers*num_direction, batch_size, hidden_dim)
        enc_output, enc_hidden = self.encoder(src, src_sz)

        if self.pass_enc2dec_hid:
           # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            dec_hidden = enc_hidden
        else:
            # dec_hidden -> Will be initialized to zeros internally
            dec_hidden = None

        # pred_vecs: (batch_size, output_dim, sequence_sz) -> shape required for CELoss
        pred_vecs = torch.zeros(batch_size, self.decoder.output_dim, tgt.size(1)).to(self.device)

        # dec_input: (batch_size, 1)
        dec_input = tgt[:,0].unsqueeze(1) # initialize to start token
        pred_vecs[:,1,0] = 1 # Initialize to start tokens all batches
        for t in range(1, tgt.size(1)):
            # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            # dec_output: batch_size, output_dim
            # dec_input: (batch_size, 1)
            dec_output, dec_hidden, _ = self.decoder( dec_input,
                                               dec_hidden,
                                               enc_output,  )
            pred_vecs[:,:,t] = dec_output

            # # prediction: batch_size
            prediction = torch.argmax(dec_output, dim=1)

            # Teacher Forcing
            if random.random() < teacher_forcing_ratio:
                dec_input = tgt[:, t].unsqueeze(1)
            else:
                dec_input = prediction.unsqueeze(1)

        return pred_vecs #(batch_size, output_dim, sequence_sz)

    def inference(self, src, max_tgt_sz=50, debug = 0):
        '''
        single input only, No batch Inferencing
        src: (sequence_len)
        debug: if True will return attention weights also
        '''
        batch_size = 1
        start_tok = src[0]
        end_tok = src[-1]
        src_sz = torch.tensor([len(src)])
        src_ = src.unsqueeze(0)

        # enc_output: (batch_size, padded_seq_length, enc_hidden_dim*num_direction)
        # enc_hidden: (enc_layers*num_direction, batch_size, hidden_dim)
        enc_output, enc_hidden = self.encoder(src_, src_sz)

        if self.pass_enc2dec_hid:
            # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            dec_hidden = enc_hidden
        else:
            # dec_hidden -> Will be initialized to zeros internally
            dec_hidden = None

        # pred_arr: (sequence_sz, 1) -> shape required for CELoss
        pred_arr = torch.zeros(max_tgt_sz, 1).to(self.device)
        if debug: attend_weight_arr = torch.zeros(max_tgt_sz, len(src)).to(self.device)

        # dec_input: (batch_size, 1)
        dec_input = start_tok.view(1,1) # initialize to start token
        pred_arr[0] = start_tok.view(1,1) # initialize to start token
        for t in range(max_tgt_sz):
            # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            # dec_output: batch_size, output_dim
            # dec_input: (batch_size, 1)
            dec_output, dec_hidden, aw = self.decoder( dec_input,
                                               dec_hidden,
                                               enc_output,  )
            # prediction :shp: (1,1)
            prediction = torch.argmax(dec_output, dim=1)
            dec_input = prediction.unsqueeze(1)
            pred_arr[t] = prediction
            if debug: attend_weight_arr[t] = aw.squeeze(-1)

            if torch.eq(prediction, end_tok):
                break

        if debug: return pred_arr.squeeze(), attend_weight_arr
        # pred_arr :shp: (sequence_len)
        return pred_arr.squeeze().to(dtype=torch.long)


    def active_beam_inference(self, src, beam_width=3, max_tgt_sz=50):
        ''' Active beam Search based decoding
        src: (sequence_len)
        '''
        def _avg_score(p_tup):
            ''' Used for Sorting
            TODO: Dividing by length of sequence power alpha as hyperparam
            '''
            return p_tup[0]

        batch_size = 1
        start_tok = src[0]
        end_tok = src[-1]
        src_sz = torch.tensor([len(src)])
        src_ = src.unsqueeze(0)

        # enc_output: (batch_size, padded_seq_length, enc_hidden_dim*num_direction)
        # enc_hidden: (enc_layers*num_direction, batch_size, hidden_dim)
        enc_output, enc_hidden = self.encoder(src_, src_sz)

        if self.pass_enc2dec_hid:
            # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            init_dec_hidden = enc_hidden
        else:
            # dec_hidden -> Will be initialized to zeros internally
            init_dec_hidden = None

        # top_pred[][0] = Σ-log_softmax
        # top_pred[][1] = sequence torch.tensor shape: (1)
        # top_pred[][2] = dec_hidden
        top_pred_list = [ (0, start_tok.unsqueeze(0) , init_dec_hidden) ]

        for t in range(max_tgt_sz):
            cur_pred_list = []

            for p_tup in top_pred_list:
                if p_tup[1][-1] == end_tok:
                    cur_pred_list.append(p_tup)
                    continue

                # dec_hidden: dec_layers, 1, hidden_dim
                # dec_output: 1, output_dim
                dec_output, dec_hidden, _ = self.decoder( x = p_tup[1][-1].view(1,1), #dec_input: (1,1)
                                                    hidden = p_tup[2],
                                                    enc_output = enc_output, )

                ## π{prob} = Σ{log(prob)} -> to prevent diminishing
                # dec_output: (1, output_dim)
                dec_output = nn.functional.log_softmax(dec_output, dim=1)
                # pred_topk.values & pred_topk.indices: (1, beam_width)
                pred_topk = torch.topk(dec_output, k=beam_width, dim=1)

                for i in range(beam_width):
                    sig_logsmx_ = p_tup[0] + pred_topk.values[0][i]
                    # seq_tensor_ : (seq_len)
                    seq_tensor_ = torch.cat( (p_tup[1], pred_topk.indices[0][i].view(1)) )

                    cur_pred_list.append( (sig_logsmx_, seq_tensor_, dec_hidden) )

            cur_pred_list.sort(key = _avg_score, reverse =True) # Maximized order
            top_pred_list = cur_pred_list[:beam_width]

            # check if end_tok of all topk
            end_flags_ = [1 if t[1][-1] == end_tok else 0 for t in top_pred_list]
            if beam_width == sum( end_flags_ ): break

        pred_tnsr_list = [t[1] for t in top_pred_list ]

        return pred_tnsr_list

    def passive_beam_inference(self, src, beam_width = 7, max_tgt_sz=50):
        '''
        Passive Beam search based inference
        src: (sequence_len)
        '''
        def _avg_score(p_tup):
            ''' Used for Sorting
            TODO: Dividing by length of sequence power alpha as hyperparam
            '''
            return  p_tup[0]

        def _beam_search_topk(topk_obj, start_tok, beam_width):
            ''' search for sequence with maxim prob
            topk_obj[x]: .values & .indices shape:(1, beam_width)
            '''
            # top_pred_list[x]: tuple(prob, seq_tensor)
            top_pred_list = [ (0, start_tok.unsqueeze(0) ), ]

            for obj in topk_obj:
                new_lst_ = list()
                for itm in top_pred_list:
                    for i in range(beam_width):
                        sig_logsmx_ = itm[0] + obj.values[0][i]
                        seq_tensor_ = torch.cat( (itm[1] , obj.indices[0][i].view(1) ) )
                        new_lst_.append( (sig_logsmx_, seq_tensor_) )

                new_lst_.sort(key = _avg_score, reverse =True)
                top_pred_list = new_lst_[:beam_width]
            return top_pred_list

        batch_size = 1
        start_tok = src[0]
        end_tok = src[-1]
        src_sz = torch.tensor([len(src)])
        src_ = src.unsqueeze(0)

        enc_output, enc_hidden = self.encoder(src_, src_sz)

        if self.pass_enc2dec_hid:
            # dec_hidden: dec_layers, batch_size , dec_hidden_dim
            dec_hidden = enc_hidden
        else:
            # dec_hidden -> Will be initialized to zeros internally
            dec_hidden = None

        # dec_input: (1, 1)
        dec_input = start_tok.view(1,1) # initialize to start token


        topk_obj = []
        for t in range(max_tgt_sz):
            dec_output, dec_hidden, aw = self.decoder( dec_input,
                                               dec_hidden,
                                               enc_output,  )

            ## π{prob} = Σ{log(prob)} -> to prevent diminishing
            # dec_output: (1, output_dim)
            dec_output = nn.functional.log_softmax(dec_output, dim=1)
            # pred_topk.values & pred_topk.indices: (1, beam_width)
            pred_topk = torch.topk(dec_output, k=beam_width, dim=1)

            topk_obj.append(pred_topk)

            # dec_input: (1, 1)
            dec_input = pred_topk.indices[0][0].view(1,1)
            if torch.eq(dec_input, end_tok):
                break

        top_pred_list = _beam_search_topk(topk_obj, start_tok, beam_width)
        pred_tnsr_list = [t[1] for t in top_pred_list ]

        return pred_tnsr_list

def load_pretrained(model, weight_path, flexible = False):
    if not weight_path:
        return model

    pretrain_dict = torch.load(weight_path, map_location=torch.device('cpu'))
    model_dict = model.state_dict()
    if flexible:
        pretrain_dict = {k: v for k, v in pretrain_dict.items() if k in model_dict}
    #print("Pretrained layers:", pretrain_dict.keys())
    model_dict.update(pretrain_dict)
    model.load_state_dict(model_dict)

    return model
    

def inferencer(word, src, tgt, topk = 10):
    if src == "eng" and tgt == "pun":
        src_glyph = eng_glyph
        tgt_glyph = pun_glyph
        model = eng2pun_model

    elif src == "pun" and tgt == "eng":
        src_glyph = pun_glyph
        tgt_glyph = eng_glyph
        model = pun2eng_model

    else:
        raise Exception("Language not supported")

    in_vec = torch.from_numpy(src_glyph.word2xlitvec(word)).to(device)
    ## change to active or passive beam
    p_out_list = model.active_beam_inference(in_vec, beam_width = topk)
    p_result = [ tgt_glyph.xlitvec2word(out.cpu().numpy()) for out in p_out_list]
        # result = voc_sanitize.reposition(p_result) ## Uncomment for repositioning
    
    result = multiple_matras_cleaning(p_result)
   
    return result
    
                    
class GlyphStrawboss():
    def __init__(self, lang_script = english_lower_script):
        """ list of letters in a language in unicode
        lang: List with unicodes
        """
        self.glyphs = lang_script

        self.char2idx = {}
        self.idx2char = {}
        self._create_index()

    def _create_index(self):

        self.char2idx['_'] = 0  #pad
        self.char2idx['$'] = 1  #start
        self.char2idx['#'] = 2  #end
        self.char2idx['*'] = 3  #Mask
        self.char2idx["'"] = 4  #apostrophe U+0027
        self.char2idx['%'] = 5  #unused
        self.char2idx['!'] = 6  #unused

        # letter to index mapping
        for idx, char in enumerate(self.glyphs):
            self.char2idx[char] = idx + 7 # +7 token initially

        # index to letter mapping
        for char, idx in self.char2idx.items():
            self.idx2char[idx] = char

    def size(self):
        return len(self.char2idx)


    def word2xlitvec(self, word):
        """ Converts given string of gyphs(word) to vector(numpy)
        Also adds tokens for start and end
        """
        try:
            vec = [self.char2idx['$']] #start token
            for i in list(word):
                vec.append(self.char2idx[i])
            vec.append(self.char2idx['#']) #end token

            vec = np.asarray(vec, dtype=np.int64)
            return vec

        except Exception as error:
            print("Error In word:", word, "Error Char not in Token:", error)
            raise ValueError(error)

    def xlitvec2word(self, vector):
        """ Converts vector(numpy) to string of glyphs(word)
        """
        char_list = []
        for i in vector:
            char_list.append(self.idx2char[i])

        word = "".join(char_list).replace('$','').replace('#','') # remove tokens
        word = word.replace("_", "").replace('*','') # remove tokens
        return word                                    
                    

def define_model_architecture(src_lang, tgt_lang):

    if src_lang == 'eng' and tgt_lang == "pun":
        src_glyph = GlyphStrawboss(english_lower_script) 
        tgt_glyph = GlyphStrawboss(gurmukhi_script)
        model_path = dir / "eng2pun_translit_model.pth"
    elif src_lang == "pun" and tgt_lang == "eng":
        model_path = dir / "pun2eng_translit_model.pth"
        src_glyph = GlyphStrawboss(gurmukhi_script) 
        tgt_glyph = GlyphStrawboss(english_lower_script)
    else:
        raise Exception('Either Source or Target Language not supported')
    
    input_dim = src_glyph.size()
    output_dim = tgt_glyph.size()
    enc_emb_dim = 32
    dec_emb_dim = 64
    enc_hidden_dim = 256
    dec_hidden_dim = 256
    rnn_type = "gru"
    enc2dec_hid = True
    attention = True
    enc_layers = 6
    dec_layers = 12
    m_dropout = 0.0
    enc_bidirect = True
    enc_outstate_dim = enc_hidden_dim * (2 if enc_bidirect else 1)


    enc = Encoder(  input_dim= input_dim, embed_dim = enc_emb_dim,
                    hidden_dim= enc_hidden_dim,
                    rnn_type = rnn_type, layers= enc_layers,
                    dropout= m_dropout, device = device,
                    bidirectional= enc_bidirect)
    dec = Decoder(  output_dim= output_dim, embed_dim = dec_emb_dim,
                    hidden_dim= dec_hidden_dim,
                    rnn_type = rnn_type, layers= dec_layers,
                    dropout= m_dropout,
                    use_attention = attention,
                    enc_outstate_dim= enc_outstate_dim,
                    device = device,)

    model = Seq2Seq(enc, dec, pass_enc2dec_hid=enc2dec_hid,
                    device=device)
    model = model.to(device)
    model = load_pretrained(model,model_path)

    return model

pun2eng_model = define_model_architecture(src_lang="pun", tgt_lang= "eng")
eng2pun_model = define_model_architecture(src_lang="eng", tgt_lang="pun")
eng_glyph = GlyphStrawboss(english_lower_script) 
pun_glyph = GlyphStrawboss(gurmukhi_script)



def multiple_matras_cleaning(word_list):
    result = []
    for word in word_list:
        prev = ''
        cleaned_word = ''
        for char in word:
            if char == prev and char in matras:
                pass
            else:
                cleaned_word += char
            prev = char
        result.append(cleaned_word)
    return result

def give_transliterations(words, src, tgt):
    try:
        words = [word.lower() for word in words]
        out_dict = {}
        for word in words:
            try:
                out_dict[word] = inferencer(word, src, tgt, topk = 1)
            except ValueError as error:
                out_dict[word] = [word]

        for eng_word in out_dict:
            out_dict[eng_word] = list(set(out_dict[eng_word]))
        return out_dict
    except Exception as e:
        print(e)
        return ""


