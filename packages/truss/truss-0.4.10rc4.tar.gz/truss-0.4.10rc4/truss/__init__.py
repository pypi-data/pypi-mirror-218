# flake8: noqa F401

from pathlib import Path

from single_source import get_version

__version__ = get_version(__name__, Path(__file__).parent.parent)


def version():
    return __version__


from truss.build import (
    create,
    create_from_mlflow_uri,
    from_directory,
    init,
    kill_all,
    load,
    mk_truss,
)
