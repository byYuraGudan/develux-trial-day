import os

import pytest

from bitbucket import BitBucket


@pytest.fixture
def workflow():
    # TODO move to pytest.ini
    return "yuriihudan"


@pytest.fixture
def repository():
    # TODO move to pytest.ini
    return "npm-package"


@pytest.fixture
def token():
    # TODO move to pytest.ini
    return os.environ.get("BITBUCKET_TOKEN")


@pytest.fixture
def bitbucket(token):
    return BitBucket(token=token)
