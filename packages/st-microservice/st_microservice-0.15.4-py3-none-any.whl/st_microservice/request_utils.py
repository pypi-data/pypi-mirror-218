from typing import Any, Callable, Coroutine

from starlette.requests import Request, State
from ariadne.types import GraphQLResolveInfo
from aiodataloader import DataLoader

from .auth_utils import User
from .database import LockedDB


def get_request(info: GraphQLResolveInfo) -> Request:
    return info.context['request']


def get_user(info: GraphQLResolveInfo) -> User:
    return get_request(info).user


def get_state(info: GraphQLResolveInfo) -> State:
    return get_request(info).state


def get_db(info: GraphQLResolveInfo) -> LockedDB:
    return get_state(info).db


def get_dataloader(
        info: GraphQLResolveInfo,
        loader_key: str,
        batch_function_wrapper: Callable[[GraphQLResolveInfo], Callable[[list], Coroutine[Any, Any, list]]]
):
    state = get_state(info)
    if not hasattr(state, 'loaders'):
        state.loaders = {}
    return state.loaders.setdefault(loader_key, DataLoader(batch_function_wrapper(info), max_batch_size=10_000))

