from unittest.mock import patch

import pytest

from bitbucket import BitBucket, BitBucketRepo


@pytest.fixture
def bitbucket():
    bitbucket = BitBucket(token="test")

    with patch.object(bitbucket, "request"):
        yield bitbucket


@pytest.fixture
def bitbucket_repo(bitbucket):
    return BitBucketRepo(bitbucket, "test-owner", "test-repo")
