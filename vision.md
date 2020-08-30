What we want:

- Easy model loading
- Simple configuration
- Swappable models
- Read config files from archives and load model

```python
import mloader

loader = mloader.open("config.json")

model = loader.load("model")
tokenizer = loader.load("tokenizer")

epochs = loader.load("epochs")

loader = mloader.open("archive.zip", config_file="config.json")
loader = mloader.open("archive.tar.gz")
loader = mloader.open("archive.tar.bz")
loader = mloader.open("http:///...../")
```