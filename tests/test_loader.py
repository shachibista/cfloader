import json

import pytest

from mloader.loader import Loader
from tests.models import *

@pytest.fixture
def model_config():
    return {
        "model": {
            "model_name": "Test"
        },
        "epochs": 10
    }

def test_loader_can_be_instantiated(model_config):
    loader = Loader(model_config)

    assert loader.config == model_config

def test_loader_can_retrieve_values_with_simple_keys(model_config):
    loader = Loader(model_config)

    assert loader.load("epochs") == 10

def test_loader_can_retrieve_values_with_compound_keys(model_config):
    loader = Loader(model_config)

    assert loader.load("model") == model_config["model"]
    assert loader.load("model.model_name") == "Test"

def test_loader_can_instantiate_class_as_string():
    loader = Loader({
        "model": "DummyModelWithoutParams"
    })

    model = loader.load("model", as_class=True, package="tests.models")
    
    assert isinstance(model, DummyModelWithoutParams)

def test_loader_can_instantiate_class_as_dict():
    loader = Loader({
        "model": {
            "model_name": "DummyModelWithoutParams"
        }
    })

    model = loader.load("model", as_class=True, package="tests.models")
    
    assert isinstance(model, DummyModelWithoutParams)

def test_loader_can_instantiate_class_with_params():
    loader = Loader({
        "model": {
            "model_name": "DummyModelWithParams",
            "epochs": 10,
            "batch_size": 60
        }
    })

    model: DummyModelWithParams = loader.load("model", as_class=True, package="tests.models")
    
    assert isinstance(model, DummyModelWithParams)
    assert model.epochs == 10
    assert model.batch_size == 60