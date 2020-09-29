import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

class CoNLL2003Dataset(Dataset):
    samples: list = []

    def __init__(self, data_filename, token_vocab, tag_vocab, max_sequence_length=512):
        self.token_vocab = token_vocab
        self.tag_vocab = tag_vocab
        self.max_sequence_length = max_sequence_length

        with open(data_filename, "r") as data_file:
            lines = data_file.readlines()
        
        sents = []
        for line in lines:
            if CoNLL2003Dataset.separator(line):
                if len(sents) > 0:
                    self.samples.append(sents)

                sents = []

                continue
            
            token, pos, pos_bio, ent_bio = line.strip().split(" ")

            token_vocab.add([token])
            tag_vocab.add([ent_bio])

            sents.append((token, pos, pos_bio, ent_bio))

        token_vocab.build()
        tag_vocab.build()

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        sents = torch.tensor([self.token_vocab.index(line[0]) for line in sample])
        tags = torch.tensor([self.tag_vocab.index(line[-1]) for line in sample])

        return sents, tags

    @staticmethod
    def separator(line):
        return line.strip() == "" or line.startswith("-DOCSTART-")