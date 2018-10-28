"""
Rubix Coding Challenge - Rubix Bakery

This file contains all the functions required
to process an order from Rubix Bakery.

An order is received in a json format and
the output is returned in json as well

Author: Renji Harold <renjiharold@nbnco.com.au>
Started: 28 October 2018.
"""

import itertools as it

from bakery.products import BakeryProducts


def process_orders(orders):
    """
    This function returns all the orders processed in json format

    :param orders:
    :return:
    """
    processed_order_list = []
    try:
        if not orders:
            return get_error_response()

        for order in orders:
            processed_order_details = process_order(order=order["order_details"])
            processed_order_dict = {
                "order_code": order["order_code"],
                "order_details": processed_order_details,
            }
            processed_order_list.append(processed_order_dict)

        return {"orders": processed_order_list, **get_success_response()}

    except KeyError as k:
        return get_error_response(
            "error while processing order: key not found - " + str(k)
        )
    except Exception as e:
        return get_error_response(
            "error while processing order: " + str(e) if str(e) else repr(e)
        )


def process_order(order):
    """
    This function processed each order in the request and returns
    the processed order in json
    :param order:
    :return:
    """
    order_details = {}
    for order_code, order_qty in order.items():
        if order_code in BakeryProducts.PRODUCTS:
            packs = BakeryProducts.PRODUCTS[order_code].keys()
            pack_breakdown = get_pack_breakdown(packs=packs, order_qty=order_qty)
            total_cost = get_total_cost(
                pack_breakdown=pack_breakdown, order_code=order_code
            )
            order_details[order_code] = get_processed_order(
                order_code=order_code,
                order_qty=order_qty,
                pack_breakdown=pack_breakdown,
                total_cost=total_cost,
            )
        else:
            order_details[order_code] = "Invalid order code"
    return order_details


def get_pack_breakdown(packs, order_qty):
    """
    This function calculates the break down of the packs
    for each product based on the quantity ordered

    :param packs:
    :param order_qty:
    :return:
    """
    pack_list = sorted(list(packs), reverse=True)
    all_pack_combo = get_all_combinations(pack_list)
    valid_combo_list = get_valid_combo(all_pack_combo, order_qty)
    least_item_combo = get_least_combo(valid_combo_list)
    return least_item_combo


def get_all_combinations(item_list):
    """
    This function gets all the different possible
    combinations of packs for a given products pack

    :param item_list:
    :return:
    """
    all_combo = []
    for r in range(len(item_list), 0, -1):
        all_combo += list(it.combinations(item_list, r))
    return all_combo


def get_valid_combo(combo_list, order_qty):
    """
    This function retrieves all the valid list of
    combinations of packs for the quantity ordered

    :param combo_list:
    :param order_qty:
    :return:
    """
    valid_combo = []
    for combo in combo_list:
        valid, pack_out = is_valid_combo(combo, order_qty)
        if valid:
            valid_combo.append(pack_out)
    return valid_combo


def is_valid_combo(pack_lst, ord_qty):
    """
    This function checks generations a possible combination
    of a pack and checks if it is valid against the
    quantity ordered.

    :param pack_lst:
    :param ord_qty:
    :return:
    """
    pack_cnt = get_pack(pack_lst, ord_qty)
    pack_sm = sum(key * value for key, value in pack_cnt.items())
    if pack_sm == ord_qty:
        return True, pack_cnt
    return False, None


def get_pack(pack_lst, ord_qty):
    """
    This function generates a possible combination
    of a pack with the quantity ordered

    :param pack_lst:
    :param ord_qty:
    :return:
    """
    pack_dict = {}
    for i in pack_lst:
        if ord_qty >= i:
            qty = ord_qty // i
            pack_dict.update({i: qty})
            ord_qty = ord_qty - i * qty
    return pack_dict


def get_least_combo(combo_list):
    """
    This function returns the combination which
    has the least number of packs

    :param combo_list:
    :return:
    """
    max_sum = 999999999
    least_combo = {}
    for combo in combo_list:
        current_sum = sum(quantity for pack_type, quantity in combo.items())
        if current_sum < max_sum:
            least_combo = combo
            max_sum = current_sum
    return least_combo


def get_total_cost(pack_breakdown, order_code):
    """
    For a given combination of a pack for a product
    this function calculates the total cost

    :param pack_breakdown:
    :param order_code:
    :return:
    """
    total_cost = 0
    for pack_type, quantity in pack_breakdown.items():
        cost = BakeryProducts.PRODUCTS[order_code].get(pack_type)
        total_cost += cost * quantity
    return round(total_cost, 2)


def get_processed_order(order_code, order_qty, pack_breakdown, total_cost):
    """
    This function returns a fully formed json response
    for the order based on the input parameters received.

    :param order_code:
    :param order_qty:
    :param pack_breakdown:
    :param total_cost:
    :return:
    """
    print("input: ", order_code, order_qty, pack_breakdown, total_cost)
    pack_breakdown_list = []

    for pack_type, quantity in pack_breakdown.items():
        pack_breakdown_dict = {
            "pack_type": pack_type,
            "pack_cost": "$" + str(BakeryProducts.PRODUCTS[order_code].get(pack_type)),
            "pack_quantity": quantity,
        }
        pack_breakdown_list.append(pack_breakdown_dict)

    order_detail_dict = {
        "order_quantity": order_qty,
        "total_cost": "$" + str(total_cost),
        "pack_breakdown": pack_breakdown_list
        if pack_breakdown_list
        else "invalid order quantity",
    }
    print("output:", order_detail_dict)
    return order_detail_dict


def get_success_response():
    """
    This function returns a custom success response

    :return:
    """
    return {"status": "success", "message": "order successfully processed"}


def get_error_response(error_message=None):
    """
    This function returns a custom error response.

    :param error_message:
    :return:
    """
    if error_message:
        return {"status": "error", "message": error_message}
    return {"status": "error", "message": "please provide order in proper format"}
