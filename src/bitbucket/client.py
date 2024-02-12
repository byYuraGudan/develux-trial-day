import copy

import requests
from requests.auth import HTTPBasicAuth, CONTENT_TYPE_MULTI_PART
from requests import Response


class BitBucket:
    def __init__(self, token: str, url: str = "https://api.bitbucket.org/2.0"):
        self.url = url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}"}

    def request(self, method: str, path: str, headers=None, **kwargs) -> Response:
        url = self.url + path

        _headers = copy.deepcopy(self._headers)
        _headers.update(self._headers)
        _headers.update(headers or {})

        response = requests.request(method, url, headers=_headers, **kwargs)
        response.raise_for_status()
        return response

    def get(self, path: str, **kwargs) -> Response:
        return self.request(method="GET", path=path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.request(method="POST", path=path, **kwargs)

    def get_content_of_file(self, workflow: str, repository: str, branch: str, filename: str) -> dict:
        response = self.get(f"/repositories/{workflow}/{repository}/src/{branch}/{filename.lstrip('/')}")
        # TODO make supporting different type of content
        return response.json()

    def upload_file(
        self,
        workflow: str,
        repository: str,
        filename: str,
        content: any,
        branch_name: str,
        message: str,
        source_commit_id: str,
    ):
        data = {
            "message": message,
            "parents": [source_commit_id],
            "branch": branch_name,
        }
        files = {filename: (filename, content)}
        return self.post(f"/repositories/{workflow}/{repository}/src", data=data, files=files)

    def create_branch(self, workflow: str, repository: str, branch_name: str, target_branch: str = "master"):
        data = {"name": branch_name, "target": {"hash": target_branch}}
        response = self.post(f"/repositories/{workflow}/{repository}/refs/branches", json=data)
        return response.json()

    def create_pull_request(
        self,
        workflow: str,
        repository: str,
        title: str,
        description: str,
        source_branch: str,
        destination_branch: str
    ) -> dict:
        data = {
            "title": title,
            "description": description,
            "source": {
                "branch": {"name": source_branch}
            },
            "destination": {
                "branch": {
                    "name": destination_branch
                }
            }
        }
        response = self.post(f"/repositories/{workflow}/{repository}/pullrequests", json=data)
        return response.json()
