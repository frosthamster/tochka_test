def pytest_addoption(parser):
    """Хук, добавляющий аргументы по пересозданию тестовой базы в pytest"""
    group = parser.getgroup('db')
    group.addoption(
        '--create-db',
        action='store_true',
        default=False,
        help='recreate test db schema and fixture'
    )
    group.addoption(
        '--fixture-name',
        default='initial',
        help='initial test fixture name'
    )
