class DummyModelWithoutParams:
    def __init__(self):
        pass

class DummyModelWithParams:
    def __init__(self, epochs, batch_size):
        self.epochs = epochs
        self.batch_size = batch_size