import importlib
import inspect
from pathlib import Path


FIXTURES_REGISTRY = {}


def run_fixture(name):
    try:
        importlib.import_module(f'.{name}', 'app.fixtures')
    except ImportError:
        pass

    fixture = FIXTURES_REGISTRY.get(name)
    if not fixture:
        raise ValueError(f'not found {name} fixture')

    fixture()


def fixture(f):
    caller_name = Path(inspect.stack()[1][0].f_code.co_filename).stem
    if caller_name in FIXTURES_REGISTRY:
        raise ValueError(f'{caller_name} fixture already exists')

    FIXTURES_REGISTRY[caller_name] = f
    return f
