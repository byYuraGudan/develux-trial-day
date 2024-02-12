import json
from pathlib import Path
from unittest.mock import patch

import pytest

from bitbucket import BitBucketRepo
from package_updater import PackageUpdater


@pytest.fixture
def package_json():
    package_json_path = Path("data/package.json")
    assert package_json_path.exists(), "Package json does not exist"

    return json.loads(package_json_path.read_text())


@pytest.fixture
def package_name() -> str:
    return "package"


@pytest.fixture
def package_version() -> str:
    return "1.2.3"


@pytest.fixture
def package_updater(
    bitbucket_repo: BitBucketRepo,
    package_json: dict,
    package_name: str,
    package_version: str
) -> PackageUpdater:
    package_updater = PackageUpdater(bitbucket_repo)
    # mock package name in package json
    package_json["dependencies"][package_name] = package_version
    package_updater.package_json = package_json
    return package_updater


@pytest.mark.parametrize("new_package_version, expected_package_version, updated", [
    ("1.0.1", "1.2.3", False),
    ("1.2.3", "1.2.3", False),
    ("2.0.1", "2.0.1", True),
])
def test_check_and_update_dependencies(
    package_updater: PackageUpdater,
    package_name: str,
    new_package_version: str,
    expected_package_version: str,
    updated: bool
):
    dependencies_updated = package_updater._check_and_update_package_version(package_name, new_package_version)

    assert dependencies_updated == updated
    assert package_updater.package_json["dependencies"][package_name] == expected_package_version


def test_update_package(package_updater: PackageUpdater, package_name: str, package_version: str):
    with patch.object(package_updater, "bitbucket_repo") as mock_bitbucket_repo:
        package_updater.update_package(package_name, "9.9.9")

        mock_bitbucket_repo.create_branch.assert_called_once()
        mock_bitbucket_repo.upload_file.assert_called_once()
        mock_bitbucket_repo.create_pull_request.assert_called_once()
