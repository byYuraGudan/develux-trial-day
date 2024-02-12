from bitbucket.client import BitBucket


class BitBucketRepo:

    def __init__(self, bitbucket: BitBucket, repo_owner: str, repo_slug: str, base_branch: str = "master"):
        self.bitbucket = bitbucket
        self.repo_owner = repo_owner
        self.repo_slug = repo_slug
        self.base_branch = base_branch

    def get_content_of_file(self, filename: str) -> dict:
        return self.bitbucket.get_content_of_file(
            workflow=self.repo_owner,
            repository=self.repo_slug,
            branch=self.base_branch,
            filename=filename
        )

    def create_branch(self, branch_name: str) -> dict:
        return self.bitbucket.create_branch(self.repo_owner, self.repo_slug, branch_name, self.base_branch)

    def upload_file(self, filename: str, content: any, branch_name: str, message: str, source_commit_id: str):
        return self.bitbucket.upload_file(
            workflow=self.repo_owner,
            repository=self.repo_slug,
            filename=filename,
            content=content,
            branch_name=branch_name,
            message=message,
            source_commit_id=source_commit_id
        )

    def create_pull_request(self, title: str, description: str, source_branch: str) -> dict:
        return self.bitbucket.create_pull_request(
            workflow=self.repo_owner,
            repository=self.repo_slug,
            title=title,
            description=description,
            source_branch=source_branch,
            destination_branch=self.base_branch
        )
