from typing import List, Optional

from ._types import (
    Action,
    ExpressionType,
    Key,
    Option,
    OrderBy,
    Output,
    RefType,
    Select,
    Store,
    Transform,
    Update,
    ValueType,
)


def _filter_args(args: dict):
    return {k: v for k, v in args.items() if v is not None}


class StorageAction:
    GET = "GET"
    SET = "SET"
    INSERT = "INSERT"
    REPLACE = "REPLACE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    QUERY = "QUERY"

    @staticmethod
    def get(
        from_: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        attr: Optional[str | List[str]] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.GET, **_filter_args(locals()))

    @staticmethod
    def query(
        select: Optional[Select] = None,
        from_: Optional[Store] = None,
        where: Optional[ExpressionType] = None,
        order_by: Optional[OrderBy] = None,
        limit: Optional[ValueType | RefType] = None,
        offset: Optional[ValueType | RefType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.QUERY, **_filter_args(locals()))

    @staticmethod
    def set(
        into: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        value: Optional[ValueType | RefType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.SET, **_filter_args(locals()))

    @staticmethod
    def insert(
        into: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        value: Optional[ValueType | RefType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.INSERT, **_filter_args(locals()))

    @staticmethod
    def replace(
        into: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        value: Optional[ValueType | RefType] = None,
        where: Optional[ExpressionType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.REPLACE, **_filter_args(locals()))

    @staticmethod
    def update(
        into: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        set: Optional[Update] = None,
        where: Optional[ExpressionType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.UPDATE, **_filter_args(locals()))

    @staticmethod
    def delete(
        from_: Optional[Store] = None,
        key: Optional[ValueType | RefType | Key] = None,
        where: Optional[ExpressionType] = None,
        option: Optional[Option] = None,
        transform: Optional[Transform] = None,
        output: Optional[Output] = None,
    ):
        return Action(StorageAction.DELETE, **_filter_args(locals()))
