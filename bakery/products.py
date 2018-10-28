"""
Rubix Coding Challenge - Rubix Bakery

This file contains valid packs for each product
sold by Rubix Bakery.

It also shows a valid sample order in json format

Author: Renji Harold <renjiharold@nbnco.com.au>
Started: 28 October 2018.
"""


class BakeryProducts:
    PRODUCTS = {
        "VS5": {3: 6.99, 5: 8.99},
        "MB11": {2: 9.95, 5: 16.95, 8: 24.95},
        "CF": {3: 5.95, 5: 9.95, 9: 16.99},
    }

    SAMPLE_ORDER = {
        "order": [
            {
                "order_code": "ORD1",
                "order_details": {
                    "product_code1": "product_quantity",
                    "product_code2": "product_quantity",
                    "product_code3": "product_quantity",
                },
            },
            {
                "order_code": "ORD2",
                "order_details": {
                    "product_code1": "product_quantity",
                    "product_code2": "product_quantity",
                    "product_code3": "product_quantity",
                },
            },
        ]
    }
