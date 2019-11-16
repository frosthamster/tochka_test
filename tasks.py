from invoke import task

from app import create_app
from app.fixtures import run_fixture

APP = 'app'
BLACK_BASE_CMD = 'black --py36 --skip-string-normalization --skip-numeric-underscore-normalization --line-length=120'


@task
def lint(ctx):
    """Run linters"""
    ctx.run(f'pylint --jobs 4 --rcfile=setup.cfg {APP}')
    ctx.run(f'{BLACK_BASE_CMD} --check {APP}')


@task
def pretty(ctx):
    """Run code formatters"""
    ctx.run(f"unify {APP} --in-place --recursive --quote='")
    ctx.run(f'{BLACK_BASE_CMD} {APP}')


@task
def load_fixture(ctx, fixture_name):
    """Load fixture to db"""
    with create_app().test_request_context():
        run_fixture(fixture_name)
