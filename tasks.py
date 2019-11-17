from invoke import task

from app import app_context
import app.fixtures

APP = 'app'
WSGI_APP = 'app.wsgi'
BIN = './venv/bin'

BLACK_BASE_CMD = 'black --py36 --skip-string-normalization --skip-numeric-underscore-normalization --line-length=100'


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
def install_fixture(ctx, fixture_name='initial'):
    """Install fixture to db"""
    with app_context():
        app.fixtures.install_fixture(fixture_name)


@task(post=[install_fixture])
def docker_up(ctx):
    """Run app in docker"""
    ctx.run(f'flask db upgrade')
    ctx.run(f'gunicorn --workers=4 --threads=4 -b :80 {WSGI_APP}:app')


@task
def docker_deploy(ctx, build=True):
    """Deploy app in docker"""
    build = '--build' if build else ''
    ctx.run(f'docker-compose -f ./docker/compose.yaml --no-ansi up {build}')
