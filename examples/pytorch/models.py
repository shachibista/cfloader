import torch.nn as nn
import torch.nn.functional as F

from torch.nn.utils.rnn import pack_sequence, pad_packed_sequence

class LSTMTagger(nn.Module):

    def __init__(self, embedding, hidden_dim, target_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.word_embeddings = embedding
        self.lstm = nn.LSTM(self.word_embeddings.embedding_dim, hidden_dim, batch_first=True)
        self.hidden2tag = nn.Linear(hidden_dim, target_size)

    def forward(self, sentence):
        packed_sentence = pack_sequence(sentence)
        padded_sentence, sentence_lengths = pad_packed_sequence(packed_sentence, batch_first=True)
        embeds = self.word_embeddings(padded_sentence)
        lstm_out, _ = self.lstm(embeds)
        tag_space = self.hidden2tag(lstm_out)
        tag_scores = F.log_softmax(tag_space, dim=2)
        return tag_scores.permute(0, 2, 1)