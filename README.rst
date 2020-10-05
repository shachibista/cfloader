==========================
Model Configuration Loader
==========================


.. image:: https://img.shields.io/pypi/v/cfloader
        :target: https://pypi.python.org/pypi/cfloader

.. image:: https://img.shields.io/travis/shachibista/cfloader.svg
        :target: https://travis-ci.com/shachibista/cfloader

.. image:: https://readthedocs.org/projects/cfloader/badge/?version=latest
        :target: https://cfloader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Loads and instantiates python classes from a configuration file.


* Free software: MIT license
* Documentation: https://cfloader.readthedocs.io.


Features
--------

* Auto class instantiation from json configuration
* Read configuration from archives
* Load dependencies between classes
* Load configuration parameter as class or as object

Installation
------------

::

    pip install cfloader

Usage
-----

Create a configuration file with parameters:

.. code-block:: json

    {
        "model": {
            "model_name": "SomeClass",
            "param_1": 20
        },
        "epochs": 10
    }

Now you can load the configuration parameters, either as primitive dicts or as a class:

.. code-block:: python

    import cfloader

    class SomeClass:
        def __init__(self, param_1):
            self.param_1 = param_1

    loader = cfloader.open("config.json")
    num_epochs = loader.load("epochs") # = int(10)
    model_param_1 = loader.load("model.param_1") # = int(20)
    model_configuration = loader.load("model") # = {"model_name": "SomeClass", "param_1": 20}
    model_class = loader.load("model", as_class=True) # = <SomeClass object (param_1 = 20)>

For a more extensive example, see ``examples/pytorch/example_pytorch.py``. 

.. note::
    If you want to run the example, run it as a python module: ``python -m examples.pytorch.example_pytorch --help``

    You may need to install pytorch ``pip install torch torchvision tqdm``

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
