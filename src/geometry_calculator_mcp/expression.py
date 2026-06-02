from __future__ import annotations

import ast
import math
import operator
from typing import Dict, Optional

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "tau": math.tau,
    "e": math.e,
}

ALLOWED_FUNCTIONS = {
    "abs": abs,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "radians": math.radians,
    "degrees": math.degrees,
}

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate_expression(expression: str, variables: Optional[Dict[str, float]] = None) -> dict:
    normalized = expression.replace("^", "**")
    tree = ast.parse(normalized, mode="eval")
    value = _evaluate_node(tree.body, variables or {})
    return {
        "value": value,
        "expression": expression,
        "meta": {
            "dimension": "2d",
            "units": {},
            "tolerance": 1e-9,
            "deterministic": True,
        },
    }


def _evaluate_node(node: ast.AST, variables: Dict[str, float]) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.Name):
        if node.id in variables:
            return float(variables[node.id])
        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown variable or constant: {node.id}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return OPERATORS[op_type](_evaluate_node(node.left, variables), _evaluate_node(node.right, variables))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return UNARY_OPERATORS[op_type](_evaluate_node(node.operand, variables))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_FUNCTIONS:
            raise ValueError("Unsupported function call")
        args = [_evaluate_node(arg, variables) for arg in node.args]
        return float(ALLOWED_FUNCTIONS[node.func.id](*args))

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")
