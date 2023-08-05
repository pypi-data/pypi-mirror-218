from types import UnionType
from typing import TypeVar, Any, Iterable, Callable, Awaitable, Sequence, get_origin, get_args, get_type_hints
from dataclasses import is_dataclass, field, fields, Field, astuple
from decimal import Decimal

from graphql import GraphQLResolveInfo
from asyncpg import Connection
import pypika
from pypika.queries import QueryBuilder
from aiodataloader import DataLoader

from .database import LockedDB
from .exceptions import NoRowsError, MultipleRowsError, DatabaseQueryError
from .request_utils import get_state, get_db


T = TypeVar('T')


class ValueEnum:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return self.__dict__[item]

    def __getitem__(self, item):
        return self.__dict__[item]


class Registry:
    def __init__(
            self,
            query_class: type[pypika.Query] = pypika.Query,
            schema_name: str | None = None,
            custom_loader: Callable[[GraphQLResolveInfo, QueryBuilder], Awaitable[list]] | None = None
    ):
        self.schema_name = schema_name
        self.models = []
        self.custom_loader = custom_loader
        self.query_class = query_class


class BaseModel:
    registry: Registry
    table_name: str
    primary_keys: list[str]
    t: pypika.Table
    fs: list[pypika.Field]
    Fields: Any
    f: Any  # Fields
    dataclass_fields: dict[str, Field]
    database_fields: dict[str, pypika.Field]
    field_count: int
    relations: dict[str, 'Relation']

    @classmethod
    def _check_relation(cls, relation: 'Relation'):
        local_fields = cls.database_fields.keys()
        for local_field in relation.join_on.values():
            if local_field not in local_fields:
                raise Exception(f"Field {local_field} does not exist in {cls.__name__}")

    @classmethod
    def build_from_tuple(cls, rec) -> 'BaseModel.f':
        if rec is None:
            return None
        return cls.f(*rec)

    @classmethod
    def build_from_mapping(cls, rec) -> 'BaseModel.f':
        if rec is None:
            return None
        return cls.f(**rec)

    @classmethod
    def build(cls, rec) -> 'BaseModel.f':
        try:
            return cls.build_from_mapping(rec)
        except TypeError:
            return cls.build_from_tuple(rec)

    @classmethod
    def build_all(cls, recs: Sequence) -> list['BaseModel.f']:
        try:
            return [cls.build_from_mapping(rec) for rec in recs]
        except TypeError:
            return [cls.build_from_tuple(rec) for rec in recs]

    @classmethod
    def primary_key_filter(cls, primary_keys: Sequence) -> pypika.Criterion:
        """ Return Criterion to be used in a .where() """
        if not len(primary_keys):
            raise DatabaseQueryError("Primary key filter must have at least one value")
        conditions = [getattr(cls.f, cls.primary_keys[i]) == pk_value for i, pk_value in enumerate(primary_keys)]
        return pypika.Criterion.all(conditions)

    @classmethod
    def get_query(cls, primary_keys: Sequence) -> QueryBuilder:
        """ Primary keys can be Params """
        q = cls.registry.query_class.from_(cls.t).select(*cls.fs).where(cls.primary_key_filter(primary_keys))
        return q

    @classmethod
    async def get(cls, db: Connection | LockedDB, primary_keys: Sequence) -> 'BaseModel.f | None':
        """ Primary keys need to be real values """
        pk_params = [pypika.Parameter(f'${i+1}') for i in range(len(primary_keys))]
        q = cls.get_query(pk_params)
        rows = await db.fetch(q, *primary_keys)
        row_count = len(rows)
        if row_count == 0:
            return None
        if row_count > 1:
            raise MultipleRowsError
        return cls.build_from_mapping(rows[0])

    @classmethod
    async def get_or_error(cls, db: Connection | LockedDB, primary_keys: Sequence) -> 'BaseModel.f':
        """ Primary keys need to be real values """
        row = await cls.get(db, primary_keys)
        if row is None:
            raise NoRowsError
        return row

    @classmethod
    def delete_query(cls, primary_keys: Sequence) -> QueryBuilder:
        """ Primary keys can be Params """
        if len(primary_keys) != len(cls.primary_keys):
            raise DatabaseQueryError("Primary keys argument in BaseModel.delete_query() must match BaseModel's in length")
        q = cls.registry.query_class.from_(cls.t).delete().where(cls.primary_key_filter(primary_keys))
        return q

    @classmethod
    async def delete(cls, db: Connection | LockedDB, primary_keys: Sequence) -> None:
        """ Primary keys need to be real values """
        pk_params = [pypika.Parameter(f'${i + 1}') for i in range(len(primary_keys))]
        q = cls.delete_query(pk_params)
        await db.execute(q, *primary_keys)

    @classmethod
    def insert_query(
            cls,
            start_number: int | None = 1,
            placeholder: str = '${}'
    ) -> QueryBuilder:
        """ Assuming order of values is the same as order of astuples(dataclass) """
        return cls.registry.query_class.into(cls.t)\
            .columns(*cls.database_fields.values())\
            .insert(*cls.generate_params(start_number, placeholder))

    @classmethod
    async def insert(cls, db: Connection | LockedDB, obj: 'BaseModel.f'):
        await db.execute(cls.insert_query(), *astuple(obj))

    @classmethod
    async def insert_many(cls, db: Connection | LockedDB, objs: Iterable['BaseModel.f']):
        await db.executemany(cls.insert_query(), [astuple(obj) for obj in objs])

    @classmethod
    def update_query(
            cls,
            start_number: int | None = 1,
            placeholder: str = '${}'
    ) -> QueryBuilder:
        params = cls.generate_params(start_number, placeholder)
        q = cls.registry.query_class.update(cls.t)
        for field_name, db_field in cls.database_fields.items():
            if field_name in cls.primary_keys:
                q = q.where(db_field == params.pop(0))
            else:
                q = q.set(db_field, params.pop(0))
        return q

    @classmethod
    async def update(cls, db: Connection | LockedDB, obj: 'BaseModel.f'):
        await db.execute(cls.update_query(), *astuple(obj))

    @classmethod
    async def update_many(cls, db: Connection | LockedDB, objs: Iterable['BaseModel.f']):
        await db.executemany(cls.update_query(), [astuple(obj) for obj in objs])

    @classmethod
    def join_relation(cls, q: QueryBuilder, relation_name: str, join_type: pypika.JoinType = pypika.JoinType.inner) -> tuple[QueryBuilder, type['BaseModel']]:
        try:
            relation = cls.relations[relation_name]
        except KeyError:
            raise Exception(f"Could not find Relation {relation_name} in model {cls.__name__}")

        rel_model = relation.model

        if not q.is_joined(rel_model.t):
            q = q.join(rel_model.t, join_type).on(pypika.Criterion.all([
                getattr(rel_model.f, rel_col) == getattr(cls.f, local_col)
                for rel_col, local_col in relation.join_on.items()
            ]))

        return q, rel_model

    @classmethod
    def generate_params(cls, start_number: int | None = 1, placeholder: str = '${}') -> list[pypika.Parameter]:
        return [
            pypika.Parameter(placeholder if start_number is None else placeholder.format(start_number + i))
            for i in range(cls.field_count)
        ]

    @classmethod
    async def batch_get(cls, info: GraphQLResolveInfo, keys_list: Sequence[tuple]) -> list:
        loader = cls.registry.custom_loader or (lambda x, y: get_db(x).fetch(y))
        q = cls.registry.query_class.from_(cls.t).select(*cls.fs).where(
            pypika.Tuple(*(getattr(cls.f, pk) for pk in cls.primary_keys)).isin(keys_list)
        )
        d = {tuple(getattr(obj, pk) for pk in cls.primary_keys): obj for obj in cls.build_all(await loader(info, q))}
        return [d.get(keys) for keys in keys_list]

    @classmethod
    async def dataloader_get(cls, info, primary_keys: tuple):
        state = get_state(info)
        if not hasattr(state, 'auto_loaders'):
            state.auto_loaders = {}

        try:
            dl = state.auto_loaders[cls.__name__]
        except KeyError:
            async def batch_get_wrapper(keys_list: Sequence[tuple]):
                return await cls.batch_get(info, keys_list)  # attach info
            dl = state.auto_loaders[cls.__name__] = DataLoader(batch_get_wrapper)
        return await dl.load(primary_keys)


def database_model(registry: Registry):
    def database_model_sub(cls: type[T]) -> type[T]:
        # Check proper setup
        assert issubclass(cls, BaseModel)
        assert isinstance(cls.table_name, str)
        assert isinstance(cls.primary_keys, list)
        subcls = cls.Fields
        assert is_dataclass(subcls)
        assert cls.f is subcls

        # Rename Subclass
        subcls.__name__ = cls.__name__ + subcls.__name__

        # Build Table
        cls.t = pypika.Table(cls.table_name, registry.schema_name)

        # Collect Fields
        dc_fields = fields(subcls)

        # Check primary keys
        for pk in cls.primary_keys:
            if pk not in [f.name for f in dc_fields]:
                raise TypeError(f"primary key column '{pk}' not found in {cls.__name__}")

        # Build fields
        cls.fs = []
        cls.dataclass_fields = {}
        cls.database_fields = {}
        for dc_field in dc_fields:
            field_name = dc_field.name
            db_real_name = dc_field.metadata.get('db_name', field_name)
            # Todo: Make sure works when aliasing
            table_field = pypika.Field(db_real_name, field_name if field_name != db_real_name else None, cls.t)
            setattr(subcls, field_name, table_field)  # After dataclass processing, reset class attibutes
            cls.fs.append(table_field)
            cls.dataclass_fields[field_name] = dc_field
            cls.database_fields[field_name] = table_field
        cls.field_count = len(cls.database_fields)

        # Check relations
        if not hasattr(cls, 'relations'):
            cls.relations = {}
        for relation in cls.relations.values():
            cls._check_relation(relation)

        # Add to registry
        registry.models.append(cls)
        cls.registry = registry
        return cls
    return database_model_sub


class Relation:
    def __init__(self, model: type[BaseModel], **join_on: str):
        if not len(join_on):
            raise Exception("There has to be at least one join condition")

        join_fields = model.database_fields.keys()
        for join_field in join_on:
            if join_field not in join_fields:
                raise Exception(f"Field {join_field} does not exist in {model.__name__}")

        self.model = model
        self.join_on = join_on


def db_name(val: str):
    return field(metadata={'db_name': val})


def get_field_main_type(model: type[BaseModel], field_name: str) -> type:
    type_ = model.dataclass_fields[field_name].type

    if get_origin(type_) is UnionType:
        type_ = get_args(type_)[0]

    if get_origin(type_) is list:
        return list

    return type_


def set_dataclass_attribute(obj, field_name: str, field_value):
    """ Like setattr but try to handle types"""
    field_type = get_type_hints(obj.__class__)[field_name]

    if get_origin(field_type) is UnionType:
        field_type = get_args(field_type)[0]

    if field_type is Decimal and isinstance(field_value, float):  # Convert float to Decimal
        field_value = Decimal(field_value)

    setattr(obj, field_name, field_value)
