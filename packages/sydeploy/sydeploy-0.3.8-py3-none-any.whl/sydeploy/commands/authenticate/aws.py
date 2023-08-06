import os.path
import sys
import shutil
from impose_cli.decorators import impose
from subprocess import run, check_call


@impose
def _settings():
    pass


def get_aws_account_id():
    account_id_exec = run(args="aws sts get-caller-identity --query 'Account' --output text",
                     shell=True, capture_output=True)
    errors = account_id_exec.stderr.decode("utf-8").strip()
    output = account_id_exec.stdout.decode("utf-8").strip()
    if errors != "":
        raise Exception(errors)
    else:
        return output


def get_codeartifact_authentication_token(region: str, domain: str, repo: str):
    account_id = get_aws_account_id()
    auth_token_exec = run(args=f"aws codeartifact get-authorization-token --domain {domain} "
                   f"--domain-owner {account_id} --region {region} --query  "
                   f"authorizationToken --output text", shell=True, capture_output=True)
    errors = auth_token_exec.stderr.decode("utf-8").strip()
    output = auth_token_exec.stdout.decode("utf-8").strip()
    if errors != "":
        raise Exception(errors)
    else:
        return output, account_id


def authenticate_codeartifact_for_pip(region: str, domain: str, repo: str):
    auth_token, account_id = get_codeartifact_authentication_token(region, domain, repo)
    new_index_url = f"https://aws:{auth_token}@{domain}-{account_id}.d.codeartifact.{region}.amazonaws.com/pypi/{repo}/simple/"
    pip = "pip" + str(sys.version[0])
    check_call([pip, "config", "set", f"global.extra-index-url", new_index_url])


def authenticate_codeartifact_for_twine(region: str, domain: str, repo: str):
    account_id = get_aws_account_id()
    # Reauthenticate the KMS for CodeArtifact
    twine_exec = run(args=f"aws codeartifact login --tool twine --domain {domain} "
             f"--domain-owner {account_id} --region {region} --repository {repo}", shell=True, capture_output=True)
    output = twine_exec.stdout.decode("utf-8").strip()
    errors = twine_exec.stderr.decode("utf-8").strip()
    if errors != "":
        raise Exception(errors)

    if os.path.exists(os.path.expanduser("~/.pypirc")):
        print("Writing to a temp file for CI/CD use.")
        if not os.path.exists("/tmp"):
            os.mkdir("/tmp")
        shutil.copy2(os.path.expanduser("~/.pypirc"), "/tmp/.pypirc")
    return output


def authenticate_ecr_for_repo(region: str):
    account_id = get_aws_account_id()
    ecr_login_exec = run(args=f"aws ecr get-login-password --region {region} "
                              f"| docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com", shell=True, capture_output=True)
    output = ecr_login_exec.stdout.decode("utf-8").strip()
    errors = ecr_login_exec.stderr.decode("utf-8").strip()
    if errors != "":
        raise Exception(errors)
    else:
        return output