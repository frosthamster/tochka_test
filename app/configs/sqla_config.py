from contextlib import contextmanager

import flask_sqlalchemy
import sqlalchemy.util
from flask_sqlalchemy.model import BindMetaMixin
from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


class NoNameMeta(BindMetaMixin, DeclarativeMeta):
    """Метакласс, аналогичный такому из flask-sqlalchemy, но без автомотической генерации имён таблиц"""


class SQLAlchemy(flask_sqlalchemy.SQLAlchemy):
    @contextmanager
    def session_scope(self, *args, remove=False, **kwargs):
        """
        Декоратор/контекстный менеджер, предоставляющий обёртку над транзакцией в базе
        в __exit__ выполняется commit, при ошибке, автоматически выполняется rollback

        Args:
            *args: аргументы для создания сессии
            remove: нужно ли уничтожать сессию по окончанию операции
            **kwargs: аргументы для создания сессии

        Returns: созданная сессия
        """
        session = self.session(*args, **kwargs)
        try:
            yield session
            session.commit()
        except Exception:
            with sqlalchemy.util.safe_reraise():
                session.rollback()
        finally:
            if remove:
                self.session.remove()

    def truncate_all_tables(self):
        """Метод, удаляющий данный из всех таблиц в базе, которые относятся к моделям"""
        meta = self.metadata
        for table in reversed(meta.sorted_tables):
            self.session.execute(table.delete())


class Model(flask_sqlalchemy.Model):
    def __repr__(self):
        return self._repr()

    def _repr(self, **kwargs):
        """
        Хелпер для определения __repr__
        Args:
            **kwargs: названия и значения атрибутов, которые необходимо отображать
        """
        identity = inspect(self).identity
        if identity is None:
            pk_repr = f'(transient {id(self)})'
        else:
            pk_repr = ', '.join(str(value) for value in identity)

        fields_repr = ' ' + ', '.join(f'{key}={value}' for key, value in kwargs.items())

        return f'<{type(self).__name__} pk={pk_repr}{fields_repr}>'


def get_db():
    return SQLAlchemy(
        model_class=declarative_base(cls=Model, metaclass=NoNameMeta, name='Model'),
        metadata=MetaData(
            naming_convention={
                'ix': 'idx_%(table_name)s_%(column_0_label)s',
                'uq': 'uq_%(table_name)s_%(column_0_name)s',
                'ck': 'ck_%(table_name)s_%(constraint_name)s',
                'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
                'pk': 'pk_%(table_name)s',
            }
        ),
        # psycopg2 fast execution helpers
        # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#psycopg2-fast-execution-helpers
        engine_options={
            'executemany_mode': 'values',
            'executemany_batch_page_size': 500,
            'executemany_values_page_size': 10_000,
        },
    )
