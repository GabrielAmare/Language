import os

__all__ = [
    'WEBSITE_PATH',
    'READER_FN',
    'GRAMMAR_FN',
    'MODELS_FN',
    'METHODS_FN',
    'ENGINE_FN',
]

# path to "Website/website"
WEBSITE_PATH = os.path.dirname(__file__).replace('\\', '/').rsplit('/', 1)[0]

READER_FN = "reader"
GRAMMAR_FN = "grammar"
MODELS_FN = "models"
METHODS_FN = "methods"
ENGINE_FN = "engine"


class LEX:
    """Lexicon class, contains all the keywords used."""
    READER = "reader"
    GRAMMAR = "grammar"
    MODELS = "models"
    IMPORTS = "imports"
    ENGINE = "engine"
