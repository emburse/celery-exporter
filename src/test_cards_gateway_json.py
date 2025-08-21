from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from .cards_gateway_json import decode_cards_gateway_json_minimal


@pytest.mark.parametrize(
    "subject, expected",
    [
        pytest.param("hello", "hello", id="string"),
        pytest.param("<<builtins:int 42>>", 42, id="int"),
        pytest.param("<<builtins:float 3.14>>", 3.14, id="float"),
        pytest.param(
            "<<datetime:datetime 2023-08-21T12:34:56>>",
            datetime.fromisoformat("2023-08-21T12:34:56"),
            id="datetime",
        ),
        pytest.param("<<decimal:Decimal 123.45>>", Decimal("123.45"), id="decimal"),
        pytest.param(
            "<<uuid:UUID 12345678-1234-5678-1234-567812345678>>",
            UUID("12345678-1234-5678-1234-567812345678"),
            id="uuid",
        ),
        pytest.param(
            "<<custom:Type something>>", "<custom:Type: something>", id="unknown_type"
        ),
        pytest.param(["<<builtins:int 1>>", "<<builtins:int 2>>"], [1, 2], id="list"),
        pytest.param(
            {"a": "<<builtins:int 1>>", "b": "<<builtins:int 2>>"},
            {"a": 1, "b": 2},
            id="dict",
        ),
        pytest.param(
            {"_model": "Connection", "id": "conn-MbGi8EGKekuoUSDbh4VYYR"},
            {
                "type": "django_model",
                "model": "Connection",
                "data": {"id": "conn-MbGi8EGKekuoUSDbh4VYYR"},
            },
            id="_model",
        ),
        pytest.param(
            {
                "_type": "CustomClass",
                "args": [1],
                "kwargs": {"x": 2},
                "state": {"y": 3},
            },
            {
                "type": "custom_object",
                "class": "CustomClass",
                "args": [1],
                "kwargs": {"x": 2},
                "state": {"y": 3},
            },
            id="_type",
        ),
        pytest.param(
            {"_import": "some.module"},
            {"type": "import", "path": "some.module"},
            id="_import",
        ),
    ],
)
def test_decode_cards_gateway_json_minimal(subject, expected) -> None:
    assert decode_cards_gateway_json_minimal(subject) == expected
