from typing import Dict

class Vocabulary:
    PADDING = "[padding]"
    UNKNOWN = "[unknown]"

    def __init__(self, ignore_case=False, simple=False):
        self.token2idx: Dict[str, int] = {}
        self.idx2token: Dict[int, str] = {}
        self.sequence_queue = set()
        self.ignore_case = ignore_case
        self.simple = simple

    def add(self, sequence):
        self.sequence_queue |= {item.lower() if self.ignore_case else item for item in set(sequence)}

    def __len__(self):
        return len(self.token2idx)

    def build(self):
        if self.simple:
            queue = sorted(self.sequence_queue)
        else:
            queue = [self.PADDING, self.UNKNOWN] + sorted(self.sequence_queue)

        for token in queue:
            if token in self.token2idx:
                continue

            idx = len(self.token2idx)
            self.token2idx[token] = idx
            self.idx2token[idx] = token
    
    def token(self, idx: int) -> str:
        return self.idx2token[idx]

    def index(self, token: str) -> int:
        if self.ignore_case:
            token = token.lower()
        return self.token2idx[token] if token in self.token2idx else self.token2idx[Vocabulary.UNKNOWN]
    
    def info(self):
        return (self.ignore_case, self.simple, self.idx2token, self.token2idx)

    @staticmethod
    def load(info):
        ignore_case, simple, idx2token, token2idx = info
        v = Vocabulary(ignore_case=ignore_case, simple=simple)
        v.idx2token = idx2token
        v.token2idx = token2idx
        return v