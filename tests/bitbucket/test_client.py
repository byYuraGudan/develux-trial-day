import json
import uuid

from bitbucket import BitBucket


def test_get_content_of_file(bitbucket: BitBucket, workflow: str, repository: str):
    file = bitbucket.get_content_of_file(workflow, repository, "master", "package.json")

    assert isinstance(file, dict)
    assert file["dependencies"]


def test_create_branch(bitbucket: BitBucket, workflow: str, repository: str):
    branch_name = f"test-branch-{uuid.uuid4()}"
    branch_info = bitbucket.create_branch(workflow, repository, branch_name=branch_name, target_branch="master")

    assert branch_info
    assert branch_info["name"] == branch_name


def test_upload_file(bitbucket: BitBucket, workflow: str, repository: str):
    filename = f"file-{uuid.uuid4()}"
    content = {"hello": "world"}

    file_info = bitbucket.upload_file(
        workflow,
        repository,
        filename,
        json.dumps(content),
        "master",
        "Testing upload file",
        "HEAD"
    )
    assert file_info

    remote_content = bitbucket.get_content_of_file(workflow, repository, "master", filename)
    assert content == remote_content


def test_create_pull_request(bitbucket: BitBucket, workflow: str, repository: str):
    # TODO test create pull request
    pass
