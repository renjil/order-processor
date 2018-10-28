import pytest
from bakery.bakery import (
    get_all_combinations,
    get_success_response,
    get_error_response,
    process_orders,
    process_order,
    get_pack_breakdown,
    get_valid_combo,
    is_valid_combo,
    get_pack,
    get_total_cost,
    get_least_combo,
    get_processed_order,
)
from bakery.products import BakeryProducts

SAMPLE_ORDER_OUTPUT = {
    "orders": [
        {
            "order_code": "ORD1",
            "order_details": {
                "VS5": {
                    "order_quantity": 10,
                    "total_cost": "$17.98",
                    "pack_breakdown": [
                        {"pack_type": 5, "pack_cost": "$8.99", "pack_quantity": 2}
                    ],
                },
                "MB11": {
                    "order_quantity": 14,
                    "total_cost": "$54.8",
                    "pack_breakdown": [
                        {"pack_type": 8, "pack_cost": "$24.95", "pack_quantity": 1},
                        {"pack_type": 2, "pack_cost": "$9.95", "pack_quantity": 3},
                    ],
                },
                "CF": {
                    "order_quantity": 13,
                    "total_cost": "$25.85",
                    "pack_breakdown": [
                        {"pack_type": 5, "pack_cost": "$9.95", "pack_quantity": 2},
                        {"pack_type": 3, "pack_cost": "$5.95", "pack_quantity": 1},
                    ],
                },
            },
        }
    ],
    "status": "success",
    "message": "order successfully processed",
}
SAMPLE_ORDER_INPUT = [
    {"order_code": "ORD1", "order_details": {"VS5": 10, "MB11": 14, "CF": 13}}
]
SAMPLE_ORDER_INVALID_INPUT = [
    {"order_code": "ORD1", "invalid_order_details": {"VS5": 10, "MB11": 14, "CF": 13}}
]


def test_get_success_response():
    expected_output = {"status": "success", "message": "order successfully processed"}
    assert expected_output, get_success_response()


def test_get_error_json_response():
    expected_output = {
        "status": "error",
        "message": "please provide order in proper format",
    }
    assert expected_output, get_error_response()


def test_process_orders():
    assert process_orders(SAMPLE_ORDER_INPUT) == SAMPLE_ORDER_OUTPUT


def test_process_orders_input_none():
    error_output = {
        "message": "please provide order in proper format",
        "status": "error",
    }
    assert process_orders(None) == error_output


def test_process_orders_input_empty():
    error_output = {
        "message": "please provide order in proper format",
        "status": "error",
    }
    assert process_orders([]) == error_output


def test_process_orders_input_invalid():
    error_output = {
        "message": "error while processing order: key not found - 'order_details'",
        "status": "error",
    }
    assert process_orders(SAMPLE_ORDER_INVALID_INPUT) == error_output


def test_process_orders_input_error():
    error_output = {
        "message": "error while processing order: string indices must be integers",
        "status": "error",
    }
    assert (
        process_orders({"order_code": "ORD1", "order_details": {"VS5": "11"}})
        == error_output
    )


def test_process_order():
    expected_output = {
        "VS5": {
            "order_quantity": 10,
            "total_cost": "$17.98",
            "pack_breakdown": [
                {"pack_type": 5, "pack_cost": "$8.99", "pack_quantity": 2}
            ],
        }
    }
    assert process_order({"VS5": 10}) == expected_output


def test_process_order_invalid_order_code():
    expected_output = {"ERR": "Invalid order code"}
    assert process_order({"ERR": 10}) == expected_output


def test_process_order_invalid_quantity():
    expected_output = {
        "VS5": {
            "order_quantity": 1,
            "total_cost": "$0",
            "pack_breakdown": "invalid order quantity",
        }
    }
    assert process_order({"VS5": 1}) == expected_output


def test_get_pack_breakdown():
    expected_output = {5: 2}
    assert (
        get_pack_breakdown(BakeryProducts.PRODUCTS["VS5"].keys(), 10) == expected_output
    )


def test_get_pack_breakdown_input_empty():
    assert get_pack_breakdown([], 10) == {}


def test_get_pack_breakdown_input_invalid():
    assert get_pack_breakdown("invalid", "10") == {}


def test_get_pack_breakdown_qty_empty():
    with pytest.raises(TypeError):
        get_pack_breakdown([3, 5], None)


def test_get_pack_breakdown_qty_string():
    with pytest.raises(TypeError):
        get_pack_breakdown([3, 5], "10")


def test_get_all_combinations():
    expected_output = [(5, 3), (5,), (3,)]
    assert get_all_combinations([5, 3]) == expected_output


def test_get_all_combinations_empty_input():
    assert get_all_combinations([]) == []


def test_get_all_combinations_null_input():
    with pytest.raises(TypeError):
        get_all_combinations(None)


def test_get_valid_combo():
    expected_output = [{5: 2}, {5: 2}]
    assert get_valid_combo([(5, 3), (5,), (3,)], 10) == expected_output


def test_get_valid_combo_again():
    expected_output = [{8: 1, 2: 3}, {5: 2, 2: 2}, {2: 7}]
    assert (
        get_valid_combo([(8, 5, 2), (8, 5), (8, 2), (5, 2), (8,), (5,), (2,)], 14)
        == expected_output
    )


def test_get_valid_combo_invalid_qty():
    expected_output = []
    assert get_valid_combo([(5, 3), (5,), (3,)], 7) == expected_output


def test_get_valid_combo_null_input():
    with pytest.raises(TypeError):
        get_valid_combo(None, 7)


def test_get_valid_combo_string_qty():
    with pytest.raises(TypeError):
        get_valid_combo([(5, 3), (5,), (3,)], "7")


def test_get_valid_combo_null_qty():
    with pytest.raises(TypeError):
        get_valid_combo([(5, 3), (5,), (3,)], None)


def test_is_valid_combo():
    valid, pack = is_valid_combo((5, 3), 10)
    assert valid is True and pack == {5: 2}


def test_is_valid_combo_false():
    valid, pack = is_valid_combo((12, 3), 10)
    assert valid is False and pack is None


def test_is_valid_combo_invalid_input():
    with pytest.raises(TypeError):
        is_valid_combo("invalid", 10)


def test_get_pack():
    expected_output = {5: 2}
    assert get_pack((5, 3), 10) == expected_output


def test_get_pack_again():
    expected_output = {3: 4}
    assert get_pack((3, 8), 12) == expected_output


def test_get_pack_invalid_test_case():
    expected_output = {}
    assert get_pack((3, 8), 1) == expected_output


def test_get_pack_invalid_ety():
    with pytest.raises(TypeError):
        get_pack((3, 8), None)


def test_get_pack_invalid_pack():
    with pytest.raises(TypeError):
        get_pack(None, 10)


def test_get_least_combo():
    expected_output = {8: 1, 2: 3}
    assert get_least_combo([{8: 1, 2: 3}, {5: 2, 2: 2}, {2: 7}]) == expected_output


def test_get_least_combo_again():
    expected_output = {3: 2, 4: 3}
    assert get_least_combo([{4: 3, 3: 2}, {3: 6}]) == expected_output


def test_get_least_combo_empty_input():
    expected_output = {}
    assert get_least_combo([]) == expected_output


def test_get_least_combo_null_input():
    with pytest.raises(TypeError):
        assert get_least_combo(None)


def test_get_total_cost():
    expected_output = 54.8
    assert get_total_cost({8: 1, 2: 3}, "MB11") == expected_output


def test_get_total_cost_invalid_order_code():
    with pytest.raises(KeyError):
        assert get_total_cost({8: 1, 2: 3}, "invalid")


def test_get_total_cost_invalid_order_code_pack_combo():
    with pytest.raises(TypeError):
        assert get_total_cost({8: 1, 2: 3}, "VS5")


def test_get_total_cost_null_order_code():
    with pytest.raises(KeyError):
        assert get_total_cost({8: 1, 2: 3}, None)


def test_get_total_cost_empty_pack():
    assert get_total_cost({}, "VS5") == 0


def test_get_total_cost_null_pack():
    with pytest.raises(AttributeError):
        assert get_total_cost(None, "VS5")


def test_get_processed_order():
    expected_output = {
        "order_quantity": 10,
        "total_cost": "$17.98",
        "pack_breakdown": [{"pack_type": 5, "pack_cost": "$8.99", "pack_quantity": 2}],
    }
    assert get_processed_order("VS5", 10, {5: 2}, 17.98) == expected_output


def test_get_processed_order_again():
    expected_output = {
        "order_quantity": 1,
        "total_cost": "$20",
        "pack_breakdown": [{"pack_type": 3, "pack_cost": "$6.99", "pack_quantity": 3}],
    }
    assert get_processed_order("VS5", 1, {3: 3}, 20) == expected_output


def test_get_processed_invalid_order_qty():
    expected_output = {
        "order_quantity": 7,
        "total_cost": "$0",
        "pack_breakdown": "invalid order quantity",
    }
    assert get_processed_order("VS5", 7, {}, 0) == expected_output
