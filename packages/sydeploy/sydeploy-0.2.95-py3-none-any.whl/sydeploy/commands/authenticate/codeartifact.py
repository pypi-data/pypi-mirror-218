import sys
import os
from subprocess import run, check_call
from impose_cli.decorators import impose


def get_index_url():
    pip = "pip" + str(sys.version_info[0])
    return run(args=f"{pip} config get global.index-url", shell=True, capture_output=True).stdout.decode("utf-8").strip()


def set_index_url(body, extra: bool = False):
    pip = "pip" + str(sys.version_info[0])
    index_url = "extra-index-url" if extra else "index-url"
    check_call([pip, "config", "set", f"global.{index_url}", body])


@impose
def pip(domain: str = None, repo: str = None, region: str = None):
    if domain is None or repo is None:
        raise Exception("A domain and a repo must be defined for CodeArtifact.")
    region = "" if region is None else f"--region {region}"

    account_id = run(args="aws sts get-caller-identity --query 'Account' --output text",
                     shell=True, capture_output=True).stdout.decode("utf-8").strip()

    res = run(args=f"aws codeartifact get-authorization-token --domain {domain} "
                   f"--domain-owner {account_id} {region} --query "
                   f"authorizationToken --output text", shell=True, capture_output=True)
    res = res.stdout.decode("utf-8").strip()

    # By default, AWS CodeArtifact overrides the PIP config file
    # I assume that this is a bug, but for the meantime, the solution
    # is to take the remote host, save it temporarily,
    # let aws replace it, and then switch it
    new_index_url = f"https://{res}@{domain}-{account_id}.d.codeartifact.{region}.amazonaws.com/pypi/{repo}/simple/"
    set_index_url(new_index_url, extra=True)


@impose
def twine(domain: str = None, repo: str = None, region: str = None):
    if domain is None or repo is None or region is None:
        raise Exception("A domain, repository, and region must be defined for authentication with CodeArtifact.")
    account_id = run(args="aws sts get-caller-identity --query 'Account' --output text",
                     shell=True, capture_output=True).stdout.decode("utf-8").strip()
    # Reauthenticate the KMS for CodeArtifact
    run(args=f"aws codeartifact login --tool twine --domain {domain} "
             f"--domain-owner {account_id} --region {region} --repository {repo}", shell=True)
    print("The repository's KMS was refreshed.")