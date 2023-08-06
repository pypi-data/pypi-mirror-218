from ._types import BuiltInFunction, Field, Function, RefType, ValueType


class FunctionName:
    IS_TYPE = "IS_TYPE"
    IS_DEFINED = "IS_DEFINED"

    LENGTH = "LENGTH"

    ARRAY_CONTAINS = "ARRAY_CONTAINS"
    ARRAY_LENGTH = "ARRAY_LENGTH"

    COUNT = "COUNT"


class TypeFunction:
    @staticmethod
    def is_type(field: str, type: str) -> Function:
        return BuiltInFunction(FunctionName.IS_TYPE, field, type)

    @staticmethod
    def is_defined(field: str) -> Function:
        return BuiltInFunction(FunctionName.IS_DEFINED, field)


class StringFunction:
    @staticmethod
    def length(field: str) -> Function:
        return BuiltInFunction(FunctionName.LENGTH, field)


class ArrayFunction:
    @staticmethod
    def array_contains(field: str, value: ValueType | RefType) -> Function:
        return BuiltInFunction(FunctionName.ARRAY_CONTAINS, field, value)

    @staticmethod
    def array_length(field: str) -> Function:
        return BuiltInFunction(FunctionName.ARRAY_LENGTH, field)


class AggregateFunction:
    @staticmethod
    def count() -> Function:
        return BuiltInFunction(FunctionName.COUNT, Field("*"))
