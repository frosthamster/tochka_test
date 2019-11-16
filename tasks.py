from invoke import task

APP = 'app'
BLACK_BASE_CMD = 'black --py36 --skip-string-normalization --skip-numeric-underscore-normalization --line-length=120'


@task
def lint(ctx):
    ctx.run(f'pylint --jobs 4 --rcfile=setup.cfg {APP}')
    ctx.run(f'{BLACK_BASE_CMD} --check {APP}')


@task
def pretty(ctx):
    ctx.run(f"unify {APP} --in-place --recursive --quote='")
    ctx.run(f'{BLACK_BASE_CMD} {APP}')
