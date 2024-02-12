import pytest

from update_package_script import parse_args


def test_parse_args_no_arguments():
    with pytest.raises(SystemExit) as e:
        parse_args()

    assert e.value.code == 2


def test_parse_args():
    args = ("package", "0.0.1", "workspace", "repository", "token")
    parser = parse_args(args)

    assert parser.package_name == "package"
    assert parser.package_version == "0.0.1"
    assert parser.bitbucket_workspace == "workspace"
    assert parser.bitbucket_repository == "repository"
    assert parser.bitbucket_token == "token"
