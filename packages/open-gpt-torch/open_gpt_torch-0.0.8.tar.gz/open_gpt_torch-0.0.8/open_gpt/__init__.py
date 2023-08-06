import logging as _logging
import os as _os
import sys

_logging.captureWarnings(True)


# import importlib.metadata if available, otherwise importlib_metadata
if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

import jina as _jina

# hide jina user survey
_os.environ['JINA_HIDE_SURVEY'] = '1'


try:
    __jina_version__ = _jina.__version__
except AttributeError as e:
    raise RuntimeError(
        '`jina` dependency is not installed correctly, please reinstall with `pip install -U --force-reinstall jina`'
    )


def get_version() -> str:
    """Return the module version number specified in pyproject.toml.
    :return: The version number.
    """
    return importlib_metadata.version(__package__ + '_torch')


__version__ = get_version()

__resources_path__ = _os.path.join(_os.path.dirname(__file__), 'resources')

_os.environ['NO_VERSION_CHECK'] = '1'

from inference_client import Client

from .factory import create_model
