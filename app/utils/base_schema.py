import marshmallow
import marshmallow_sqlalchemy

from app import db


class BaseOpts(marshmallow_sqlalchemy.ModelSchemaOpts):
    def __init__(self, meta, *args, **kwargs):
        if not hasattr(meta, 'sqla_session'):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta, *args, **kwargs)


class ModelSchema(marshmallow_sqlalchemy.ModelSchema):
    OPTIONS_CLASS = BaseOpts


class Schema(marshmallow.Schema):
    OPTIONS_CLASS = BaseOpts
