import json
import uuid

# This Library support semantic version
from nodesemver import lt

from bitbucket.repo import BitBucketRepo


class PackageUpdater:
    def __init__(self, bitbucket_repo: BitBucketRepo, package_json_path: str = "package.json"):
        # TODO use the atlassian BitBucket
        self.bitbucket_repo = bitbucket_repo
        self.package_json_path = package_json_path

        # TODO validate the package json
        self.package_json = self.bitbucket_repo.get_content_of_file(self.package_json_path)

    def _check_and_update_package_version(self, package_name: str, package_version: str) -> bool:
        # TODO check for no dependencies
        dependencies = self.package_json.get("dependencies", {})
        source_package_version = dependencies.get(package_name)

        if not source_package_version:
            print(f"Package `{package_name}` not found in dependencies")
            return False

        if lt(source_package_version, package_version, True):
            dependencies[package_name] = package_version
            print(f"Updating package {package_name} from {source_package_version} to {package_version}")
            return True
        else:
            print(f"Package {package_name} current version({source_package_version}) is greater than {package_version}")

        return False

    def update_package(self, package_name: str, package_version: str):
        # TODO validate package version
        updated = self._check_and_update_package_version(package_name, package_version)

        if not updated:
            return

        # TODO Handle if branch already exists and remove uuid
        # Uuid is used to avoid branch name duplication
        branch_name = f"update-{package_name}-to-{package_version}-{uuid.uuid4()}"
        branch_info = self.bitbucket_repo.create_branch(branch_name)
        branch_hash = branch_info["target"]["hash"]

        self.bitbucket_repo.upload_file(
            filename=self.package_json_path,
            content=json.dumps(self.package_json, indent=4),
            branch_name=branch_name,
            message=f"Update {package_name} to version {package_version}",
            source_commit_id=branch_hash
        )

        # TODO handle pull request already exists
        pull_request_info = self.bitbucket_repo.create_pull_request(
            title=f"Update {package_name} to version {package_version}",
            description=f"Update {package_name} to version {package_version}",
            source_branch=branch_name,
        )
        pull_request_link = pull_request_info["links"]["html"]["href"]
        print(f"Pull request link: {pull_request_link}")
