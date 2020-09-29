import os
import sys
import mloader
import pickle

from pathlib import Path

import torch
from torch.utils.data import DataLoader
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence

from examples.pytorch.utils import download
from examples.pytorch.dataset import CoNLL2003Dataset
from examples.pytorch.vocabulary import Vocabulary
from tqdm import tqdm, trange

module_dir = os.path.dirname(__file__)

def simple_collator(batch):
    sorted_batch = sorted(batch, key=lambda x: len(x[0]), reverse=True)

    collated = (
        [sample[0] for sample in sorted_batch],
        [sample[1] for sample in sorted_batch]
    )

    return collated

def cmd_train(args):
    model_file = Path(args.model or f"{module_dir}/config.json")
    loader = mloader.open(model_file)

    training_vocabulary = Vocabulary(ignore_case=True)
    tag_vocabulary = Vocabulary(ignore_case=True, simple=True)
    training_dataset = CoNLL2003Dataset("train.txt", training_vocabulary, tag_vocabulary)
    training_loader = DataLoader(training_dataset, batch_size=10, collate_fn=simple_collator)

    epochs = loader.load("epochs")
    lr = loader.load("optimizer.lr")

    model = loader.load("model", as_class=True, package=".models")
    loss_function = torch.nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        for batch in tqdm(training_loader):
            x_train, y_train = batch
            
            model.zero_grad()

            tag_scores = model(x_train)
            target_scores = pad_sequence(y_train, batch_first=True)

            loss = loss_function(tag_scores, target_scores)
            loss.backward()
            optimizer.step()

    with open(f"{model_file.stem}.pickle", "wb") as model_file:
        pickle.dump({
            "config": loader.config,
            "model": model.state_dict(),
            "token_vocabulary": training_vocabulary.info(),
            "tag_vocabulary": tag_vocabulary.info()
        }, model_file)

def cmd_test(args):
    if not os.path.exists(args.model):
        print("model has not been trained yet")
        sys.exit()
    
    with open(args.model, "rb") as model_file:
        saved_model = pickle.load(model_file)
    
    token_vocabulary = Vocabulary.load(saved_model["token_vocabulary"])
    tag_vocabulary = Vocabulary.load(saved_model["tag_vocabulary"])

    loader = mloader.open(saved_model["config"])
    model = loader.load("model", as_class=True, package=".models")
    model.load_state_dict(saved_model["model"])
    model.eval()

    tokens = args.sent.split(" ")
    model_input = torch.tensor([[token_vocabulary.index(token) for token in tokens]])
    
    outputs = model(model_input)

    print([tag_vocabulary.token(c.item()) for c in torch.argmax(outputs, dim=1).squeeze()])

if __name__ == "__main__":
    download("https://github.com/davidsbatista/NER-datasets/blob/master/CONLL2003/train.txt?raw=true", cache=True)

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_train = subparsers.add_parser("train")
    parser_train.add_argument("model", nargs='?')
    parser_train.set_defaults(func=cmd_train)

    parser_test = subparsers.add_parser("test")
    parser_test.add_argument("model")
    parser_test.add_argument("sent")
    parser_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    args.func(args)