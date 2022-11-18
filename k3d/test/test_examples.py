import sys
from pathlib import Path

import pytest
from pytest_notebook.nb_regression import NBRegressionFixture
from pytest_notebook.plugin import gather_config_options


EXAMPLES_DIR = Path(__file__).resolve().parent.parent.absolute()
_exclude_files = []
EXCLUDE = [EXAMPLES_DIR / t for t in _exclude_files]
EXAMPLES = [t for t in EXAMPLES_DIR.glob('*.ipynb') if t not in EXCLUDE]


class NBLaxFixture(NBRegressionFixture):
    """Same functionality as base class, but result comparison for regressions is skipped"""

    def check(self, path):
        return super().check(path=path, raise_errors=False)


@pytest.fixture(scope="function")
def nb_lax(pytestconfig):
    kwargs, other_args = gather_config_options(pytestconfig)
    return NBLaxFixture(**kwargs)


@pytest.mark.parametrize("filename", EXAMPLES, ids=[t.name for t in EXAMPLES])
def test_check(filename, nb_lax):
    nb_lax.check(filename)


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))

