from ._types import BuiltInFunction, Field, Function, RefType, ValueType


class TypeFunction:
    @staticmethod
    def is_type(field: str, type: str) -> Function:
        return BuiltInFunction("IS_TYPE", field, type)

    @staticmethod
    def is_defined(field: str) -> Function:
        return BuiltInFunction("IS_DEFINED", field)


class StringFunction:
    @staticmethod
    def length(field: str) -> Function:
        return BuiltInFunction("LENGTH", field)


class ArrayFunction:
    @staticmethod
    def array_contains(field: str, value: ValueType | RefType) -> Function:
        return BuiltInFunction("ARRAY_CONTAINS", field, value)

    @staticmethod
    def array_length(field: str) -> Function:
        return BuiltInFunction("ARRAY_LENGTH", field)


class AggregateFunction:
    @staticmethod
    def count() -> Function:
        return BuiltInFunction("COUNT", Field("*"))
