import os

from invoke import Exit, task
from dotenv.main import DotEnv


def _check_stack(stack):
    if stack is None:
        raise Exit("No stack name specified")

    stack_path = os.path.abspath(stack)
    if not os.path.isdir(stack_path):
        raise Exit(f"No stack directory named {stack}")

    return stack_path


def _check_dot_env(stack_path):
    stack_name = os.path.basename(stack_path)
    dot_env_example_path = os.path.join(stack_path, ".env.example")
    dot_env_path = os.path.join(stack_path, ".env")

    if os.path.isfile(dot_env_example_path) and not os.path.isfile(dot_env_path):
        raise Exit(
            f"Environment file required for stack {stack_name}."
            f" Please copy {dot_env_example_path} to {dot_env_path}"
        )

    return dot_env_path


def _check_dot_secret(stack_path):
    stack_name = os.path.basename(stack_path)
    dot_secret_example_path = os.path.join(stack_path, ".secret.example")
    dot_secret_path = os.path.join(stack_path, ".secret")

    if os.path.isfile(dot_secret_example_path) and not os.path.isfile(dot_secret_path):
        raise Exit(
            f"Secret file required for stack {stack_name}."
            f" Please copy {dot_secret_example_path} to {dot_secret_path}"
        )

    return dot_secret_path


def _create_secrets(ctx, dot_secret_path):
    if os.path.isfile(dot_secret_path):
        dot_secret = DotEnv(dotenv_path=dot_secret_path)
        secret_config = dot_secret.dict()
        for secret_name, secret_value in secret_config.items():
            ctx.run(f"echo {secret_value} | docker secret create {secret_name} -")


def _remove_secrets(ctx, dot_secret_path):
    if os.path.isfile(dot_secret_path):
        dot_secret = DotEnv(dotenv_path=dot_secret_path)
        secret_config = dot_secret.dict()
        for secret_name, secret_value in secret_config.items():
            ctx.run(f"docker secret rm {secret_name}")


@task
def stack_deploy(ctx, stack=None):
    stack_path = _check_stack(stack)
    dot_env_path = _check_dot_env(stack_path)
    dot_secret_path = _check_dot_secret(stack_path)

    _create_secrets(ctx, dot_secret_path)

    with ctx.cd(stack_path):
        ctx.run(f"docker stack deploy -c <(docker-compose config) {stack}")


@task
def stack_update(ctx, stack=None):
    stack_path = _check_stack(stack)
    dot_env_path = _check_dot_env(stack_path)

    with ctx.cd(stack_path):
        ctx.run(f"docker stack deploy -c <(docker-compose config) {stack}")


@task
def stack_rm(ctx, stack=None):
    stack_path = _check_stack(stack)
    dot_secret_path = _check_dot_secret(stack_path)

    with ctx.cd(stack_path):
        ctx.run(f"docker stack rm {stack}")

    _remove_secrets(ctx, dot_secret_path)


@task
def generate_bcrypt_hash(ctx):
    import getpass
    from passlib.hash import bcrypt

    print(bcrypt.hash(getpass.getpass()))
