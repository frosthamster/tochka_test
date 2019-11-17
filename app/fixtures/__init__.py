import importlib
import inspect
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
FIXTURES_REGISTRY = {}


def install_fixture(name):
    try:
        importlib.import_module(f'.{name}', 'app.fixtures')
    except ImportError:
        pass

    fixture = FIXTURES_REGISTRY.get(name)
    if not fixture:
        raise ValueError(f'not found {name} fixture')

    logger.info(f'installing fixture {name}')
    fixture()


def fixture(f):
    caller_name = Path(inspect.stack()[1][0].f_code.co_filename).stem
    if caller_name in FIXTURES_REGISTRY:
        raise ValueError(f'{caller_name} fixture already exists')

    FIXTURES_REGISTRY[caller_name] = f
    return f
