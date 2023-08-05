from .audit import Audit
from .belongs_to import BelongsTo
from .boolean import Boolean
from .category_tree import CategoryTree
from .column import Column
from .created import Created
from .datetime import DateTime
from .email import Email
from .float import Float
from .has_many import HasMany
from .integer import Integer
from .json import JSON
from .many_to_many import ManyToMany
from .many_to_many_with_data import ManyToManyWithData
from .select import Select
from .string import String
from .updated import Updated
from .uuid import UUID


def build_column_config(name, column_class, **kwargs):
    return (name, {**{"class": column_class}, **kwargs})


def audit(name, **kwargs):
    return build_column_config(name, Audit, **kwargs)


def belongs_to(name, **kwargs):
    return build_column_config(name, BelongsTo, **kwargs)


def boolean(name, **kwargs):
    return build_column_config(name, Boolean, **kwargs)


def category_tree(name, **kwargs):
    return build_column_config(name, CategoryTree, **kwargs)


def created(name, **kwargs):
    return build_column_config(name, Created, **kwargs)


def datetime(name, **kwargs):
    return build_column_config(name, DateTime, **kwargs)


def email(name, **kwargs):
    return build_column_config(name, Email, **kwargs)


def float(name, **kwargs):
    return build_column_config(name, Float, **kwargs)


def has_many(name, **kwargs):
    return build_column_config(name, HasMany, **kwargs)


def integer(name, **kwargs):
    return build_column_config(name, Integer, **kwargs)


def json(name, **kwargs):
    return build_column_config(name, JSON, **kwargs)


def many_to_many(name, **kwargs):
    return build_column_config(name, ManyToMany, **kwargs)


def many_to_many_with_data(name, **kwargs):
    return build_column_config(name, ManyToManyWithData, **kwargs)


def select(name, **kwargs):
    return build_column_config(name, Select, **kwargs)


def string(name, **kwargs):
    return build_column_config(name, String, **kwargs)


def updated(name, **kwargs):
    return build_column_config(name, Updated, **kwargs)


def uuid(name, **kwargs):
    return build_column_config(name, UUID, **kwargs)


__all__ = [
    "build_column_config",
    "audit",
    "Audit",
    "belongs_to",
    "BelongsTo",
    "boolean",
    "Boolean",
    "category_tree",
    "CategoryTree",
    "created",
    "Column",
    "Created",
    "datetime",
    "DateTime",
    "email",
    "Email",
    "float",
    "Float",
    "has_many",
    "HasMany",
    "integer",
    "Integer",
    "json",
    "JSON",
    "many_to_many",
    "ManyToMany",
    "many_to_many_with_data",
    "ManyToManyWithData",
    "select",
    "Select",
    "string",
    "String",
    "updated",
    "Updated",
    "uuid",
    "UUID",
]
