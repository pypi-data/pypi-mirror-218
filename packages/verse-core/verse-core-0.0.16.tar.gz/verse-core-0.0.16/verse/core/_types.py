from __future__ import annotations

import json
from abc import ABC
from enum import Enum
from typing import Any, Dict, List, Optional, cast

__all__ = [
    "And",
    "BuiltInFunction",
    "Comparison",
    "Expression",
    "ExpressionType",
    "Field",
    "Function",
    "Key",
    "Not",
    "Option",
    "Or",
    "OrderBy",
    "OrderByDirection",
    "OrderByTerm",
    "Output",
    "OutputTerm",
    "Parameter",
    "Ref",
    "RefType",
    "Select",
    "SelectTerm",
    "Store",
    "Transform",
    "TransformTerm",
    "Update",
    "UpdateOp",
    "UpdateOperation",
    "ValueType",
]


def _serialize(value: Any) -> str:
    if value is None or isinstance(value, (str, int, float, bool, dict, list)):
        return json.dumps(value)
    return str(value)


class Action:
    op: str
    args: Dict[str, Any]

    def __init__(self, op: str, **kwargs: Any):
        self.op = op
        self.args = locals()["kwargs"]

    def __str__(self) -> str:
        _str = f"{self.op}"
        for key, value in self.args.items():
            name = key.replace("_", " ").strip().upper()
            _str = _str + f" {name} {_serialize(value=value)}"
        return _str

    def __getattr__(self, name):
        if name == "op":
            return self.op
        if name in self.args:
            return self.args.get(name)
        return None

    def __getitem__(self, name):
        if name == "op":
            return self.op
        if name in self.args:
            return self.args.get(name)
        return None


ValueType = str | int | float | bool | dict | list | None


class Field:
    path: str

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return self.path


class Parameter:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"@{self.name}"


class Function:
    namespace: str
    name: str
    args: tuple

    def __init__(
        self,
        namespace: str,
        name: str,
        *args: ValueType | RefType,
    ):
        self.namespace = namespace
        self.name = name
        self.args = args

    def __str__(self) -> str:
        _str = f"{self.namespace}.{self.name}"
        _str = _str + f"({', '.join(_serialize(a) for a in self.args)})"
        return _str


class BuiltInFunction(Function):
    def __init__(self, name: str, *args: ValueType | RefType):
        Function.__init__(self, "builtin", name, *args)

    def __str__(self) -> str:
        _str = self.name
        _str = _str + f"({', '.join(_serialize(a) for a in self.args)})"
        return _str


class Ref:
    ref: str

    def __init__(self, ref: str):
        self.ref = ref

    def __str__(self) -> str:
        return f"{{{{{self.ref}}}}}"


RefType = Field | Parameter | Function | Ref


class Key:
    value: ValueType | RefType

    def __init__(self, value: ValueType | RefType):
        self.value = value

    def __str__(self) -> str:
        if isinstance(self.value, dict):
            return f"""{', '.join(
                f'{k}={_serialize(v)}'
                for k, v in self.value.items())}"""
        return _serialize(self.value)


class Expression(ABC):
    @staticmethod
    def comparison(
        lexpr: ExpressionType,
        op: ComparisonOp | str,
        rexpr: ExpressionType,
    ):
        return Comparison(lexpr=lexpr, op=op, rexpr=rexpr)

    @staticmethod
    def and_(lexpr: ExpressionType, rexpr: ExpressionType) -> And:
        return And(lexpr=lexpr, rexpr=rexpr)

    @staticmethod
    def or_(lexpr: ExpressionType, rexpr: ExpressionType) -> Or:
        return Or(lexpr=lexpr, rexpr=rexpr)

    @staticmethod
    def not_(self) -> Not:
        return Not(expr=self)


ExpressionType = ValueType | RefType | Expression


class Comparison(Expression):
    lexpr: ExpressionType
    op: ComparisonOp
    rexpr: ExpressionType

    def __init__(
        self,
        lexpr: ExpressionType,
        op: ComparisonOp | str,
        rexpr: ExpressionType,
    ):
        self.lexpr = lexpr
        self.rexpr = rexpr

        if isinstance(op, ComparisonOp):
            self.op = op
        elif isinstance(op, str):
            self.op = ComparisonOp(op.upper())
        else:
            ValueError("Op has invalid type")

    def __str__(self) -> str:
        _str = f"{_serialize(self.lexpr)} {self.op.value} "
        if self.op == ComparisonOp.BETWEEN:
            val = cast(list, self.rexpr)
            _str = _str + f"{_serialize(val[0])} AND {_serialize(val[1])}"
        else:
            _str = _str + _serialize(self.rexpr)
        return _str


class ComparisonOp(str, Enum):
    LT = "<"
    LT_EQ = "<="
    GT = ">"
    GT_EQ = ">="
    EQ = "="
    NEQ = "!="
    IN = "IN"
    NOT_IN = "NOT IN"
    BETWEEN = "BETWEEN"
    LIKE = "LIKE"


class And(Expression):
    lexpr: ExpressionType
    rexpr: ExpressionType

    def __init__(
        self,
        lexpr: ExpressionType,
        rexpr: ExpressionType,
    ):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def __str__(self) -> str:
        return f"({_serialize(self.lexpr)} AND {_serialize(self.rexpr)})"


class Or(Expression):
    lexpr: ExpressionType
    rexpr: ExpressionType

    def __init__(
        self,
        lexpr: ExpressionType,
        rexpr: ExpressionType,
    ):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def __str__(self) -> str:
        return f"({_serialize(self.lexpr)} OR {_serialize(self.rexpr)})"


class Not(Expression):
    expr: ExpressionType

    def __init__(self, expr: ExpressionType):
        self.expr = expr

    def __str__(self) -> str:
        return f"NOT {_serialize(self.expr)}"


class Update:
    ops: Dict[str, UpdateOperation]

    def __init__(self, ops: Optional[Dict[str, UpdateOperation]] = None):
        if ops is not None:
            self.ops = ops
        else:
            self.ops = {}

    def set(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.SET, value)

    def add(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.ADD, value)

    def replace(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.REPLACE, value)

    def remove(self, field: str):
        self.ops[field] = UpdateOperation(UpdateOp.REMOVE)

    def move(self, field: str, dest: str):
        self.ops[field] = UpdateOperation(UpdateOp.MOVE, dest)

    def array_add(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.ARRAY_ADD, value)

    def array_remove(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.ARRAY_REMOVE, value)

    def array_union(self, field: str, value: ExpressionType):
        self.ops[field] = UpdateOperation(UpdateOp.ARRAY_UNION, value)

    def __str__(self) -> str:
        return f"{', '.join(f'{k}={str(v)}' for k, v in self.ops.items())}"


class UpdateOperation:
    op: UpdateOp
    args: tuple

    def __init__(self, op: UpdateOp, *args: ExpressionType):
        self.op = op
        self.args = args

    def __str__(self) -> str:
        _str_args = f"{', '.join(_serialize(a) for a in self.args)}"
        return f"{self.op.value}({_str_args})"


class UpdateOp(str, Enum):
    SET = "SET"
    ADD = "ADD"
    REPLACE = "REPLACE"
    REMOVE = "REMOVE"
    MOVE = "MOVE"
    INCREMENT = "INCREMENT"
    ARRAY_ADD = "ARRAY_ADD"
    ARRAY_REMOVE = "ARRAY_REMOVE"
    ARRAY_UNION = "ARRAY_UNION"


class Select:
    terms: List[SelectTerm]

    def __init__(self, terms: Optional[List[SelectTerm]] = None):
        if terms is not None:
            self.terms = terms
        else:
            self.terms = []

    def add(self, expr: ExpressionType, alias: Optional[str] = None):
        self.terms.append(SelectTerm(expr=expr, alias=alias))

    def add_field(self, field: str, alias: Optional[str] = None):
        self.terms.append(SelectTerm(expr=Field(field), alias=alias))

    def __str__(self) -> str:
        if len(self.terms) == 0:
            return "*"
        return f"{', '.join(str(t) for t in self.terms)}"


class SelectTerm:
    expr: ExpressionType
    alias: Optional[str]

    def __init__(self, expr: ExpressionType, alias: Optional[str] = None):
        self.expr = expr
        self.alias = alias

    def __str__(self) -> str:
        _str = f"{_serialize(self.expr)}"
        if self.alias is not None:
            _str = f"{_str} AS {self.alias}"
        return _str


class OrderBy:
    terms: List[OrderByTerm]

    def __init__(
        self,
        terms: Optional[List[OrderByTerm]] = None,
    ):
        if terms is not None:
            self.terms = terms
        else:
            self.terms = []

    def add(
        self,
        expr: ExpressionType,
        direction: Optional[OrderByDirection | str] = None,
    ):
        self.terms.append(OrderByTerm(expr=expr, direction=direction))

    def add_field(
        self,
        field: str,
        direction: Optional[OrderByDirection | str] = None,
    ):
        self.terms.append(OrderByTerm(expr=Field(field), direction=direction))

    def __str__(self) -> str:
        return ", ".join([str(t) for t in self.terms])


class OrderByTerm:
    expr: ExpressionType
    direction: Optional[OrderByDirection]

    def __init__(
        self,
        expr: ExpressionType,
        direction: Optional[OrderByDirection | str] = None,
    ):
        self.expr = expr

        if direction is None:
            self.direction = None
        elif isinstance(direction, OrderByDirection):
            self.direction = direction
        elif isinstance(direction, str):
            self.direction = OrderByDirection(direction.upper())
        else:
            ValueError("Direction has invalid type")

    def __str__(self) -> str:
        _str = _serialize(self.expr)
        if self.direction:
            _str = f"{_str} {self.direction.value}"
        return _str


class OrderByDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Option:
    args: Dict[str, Any]

    def __init__(self, **kwargs: ExpressionType):
        self.args = locals()["kwargs"]

    def __str__(self) -> str:
        return f"""{', '.join(
            f'{k}={_serialize(v)}'
            for k, v in self.args.items())}"""


class Transform:
    terms: List[TransformTerm]

    def __init__(self, terms: Optional[List[TransformTerm]] = None):
        if terms is not None:
            self.terms = terms
        else:
            self.terms = []

    def add(self, expr: ExpressionType, dest: str):
        self.terms.append(TransformTerm(expr=expr, dest=dest))

    def add_field(self, field: str, dest: str):
        self.terms.append(TransformTerm(expr=Field(field), dest=dest))

    def __str__(self) -> str:
        return f"{', '.join(str(t) for t in self.terms)}"


class TransformTerm:
    expr: ExpressionType
    dest: str

    def __init__(self, expr: ExpressionType, dest: str):
        self.expr = expr
        self.dest = dest

    def __str__(self) -> str:
        return f"{_serialize(self.expr)} AS {self.dest}"


class Output:
    terms: List[OutputTerm]

    def __init__(self, terms: Optional[List[OutputTerm]] = None):
        if terms is not None:
            self.terms = terms
        else:
            self.terms = []

    def add(self, source: ExpressionType, dest: ExpressionType):
        self.terms.append(OutputTerm(expr=source, dest=dest))

    def add_field(self, field: str, dest: ExpressionType):
        self.terms.append(OutputTerm(expr=Field(field), dest=dest))

    def __str__(self) -> str:
        return ", ".join([str(o) for o in self.terms])


class OutputTerm:
    expr: ExpressionType
    dest: ExpressionType

    def __init__(self, expr: ExpressionType, dest: ExpressionType):
        self.expr = expr
        self.dest = dest

    def __str__(self) -> str:
        return f"{_serialize(self.expr)} INTO {_serialize(self.dest)}"


class Store:
    id: str

    def __init__(self, id: str):
        self.id = id

    def __str__(self) -> str:
        return self.id
