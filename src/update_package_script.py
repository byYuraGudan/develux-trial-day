import argparse

from bitbucket import BitBucket, BitBucketRepo
from package_updater import PackageUpdater


def parse_args(args=None):
    argument_parser = argparse.ArgumentParser(description="Package updater")
    argument_parser.add_argument("package_name", type=str, help="Package name")
    argument_parser.add_argument("package_version", type=str, help="Package version")
    argument_parser.add_argument("bitbucket_workspace", type=str, help="Bitbucket Workspace")
    argument_parser.add_argument("bitbucket_repository", type=str, help="Bitbucket Repository")
    argument_parser.add_argument("bitbucket_token", type=str, help="Bitbucket Access Token")
    return argument_parser.parse_args(args)


def main(args=None):
    parser = parse_args(args)

    # TODO handle invalid token
    bitbucket = BitBucket(token=parser.bitbucket_token)
    bitbucket_repo = BitBucketRepo(bitbucket, parser.bitbucket_workspace, parser.bitbucket_repository)

    package_updater = PackageUpdater(bitbucket_repo)
    package_updater.update_package(parser.package_name, parser.package_version)


if __name__ == '__main__':
    # For testing purpose, uncomment and give as a parameter to main function
    # args = ("package", "0.1.15", "yuriihudan", "npm-package", "<TOKEN>")
    main()
