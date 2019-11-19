from invoke import task

from app import app_context
import app.fixtures

APP = 'app'
WSGI_APP = 'app.wsgi'
BIN = './venv/bin'

BLACK_BASE_CMD = 'black --py36 --skip-string-normalization --skip-numeric-underscore-normalization --line-length=100'


@task
def run(ctx):
    """Run app on debug server"""
    ctx.run('flask run --host=0.0.0.0 --port=8080 --no-reload')


@task
def lint(ctx):
    """Run linters"""
    ctx.run(f'pylint --jobs 4 --rcfile=setup.cfg {APP}')
    ctx.run(f'{BLACK_BASE_CMD} --check {APP}')


@task
def pretty(ctx):
    """Run code formatters"""
    ctx.run(f"unify {APP} --in-place --recursive")
    ctx.run(f'{BLACK_BASE_CMD} {APP}')


@task
def install_fixture(ctx, fixture_name='initial'):
    """Install fixture to db"""
    with app_context():
        app.fixtures.install_fixture(fixture_name)


@task
def db_upgrade(ctx):
    """Run app migrations"""
    ctx.run('flask db upgrade')


@task(pre=[db_upgrade, install_fixture])
def docker_up(ctx):
    """Run app in docker"""
    ctx.run(f'gunicorn --workers=4 --threads=4 --bind :80 {WSGI_APP}:app')
