"""
Tests for orders manager
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json

import pytest
from flask import Flask

from store_manager import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    result = client.get("/health-check")
    assert result.status_code == 200
    assert result.get_json() == {"status": "ok"}


def test_stock_flow(client: Flask):
    # 1. Créez un article (`POST /products`)
    product_data = {"name": "Some Item", "sku": "12345", "price": 99.90}
    response = client.post(
        "/products", data=json.dumps(product_data), content_type="application/json"
    )
    expected_status_code = 201

    assert (
        response.status_code == expected_status_code
    ), "1. `POST /products` wrong status code"
    data = response.get_json()
    assert data["product_id"] > 0

    # 2. Ajoutez 5 unités au stock de cet article (`POST /stocks`)
    product_id = data["product_id"]
    stock_quantity = 5
    stock_data = {"product_id": product_id, "quantity": stock_quantity}
    response = client.post(
        "/stocks", data=json.dumps(stock_data), content_type="application/json"
    )
    expected_status_code = 201

    assert (
        response.status_code == expected_status_code
    ), "2. `POST /stocks` wrong status code"
    data = response.get_json()
    assert f"rows added: {product_id}" in data["result"]

    # 3. Vérifiez le stock, votre article devra avoir 5 unités dans le stock (`GET /stocks/:id`)
    response = client.get(f"/stocks/{product_id}", content_type="application/json")
    expected_status_code = 201

    assert (
        response.status_code == expected_status_code
    ), "3. `GET /stocks/:id` wrong status code"
    data = response.get_json()
    assert stock_quantity == data["quantity"]

    # 4. Faites une commande de l'article que vous avez crée, 2 unités (`POST /orders`)
    order_quantity = 2
    product_data = {
        "user_id": 1,
        "items": [{"product_id": product_id, "quantity": order_quantity}],
    }
    response = client.post(
        "/orders", data=json.dumps(product_data), content_type="application/json"
    )
    expected_status_code = 201
    order_id = response.get_json()["order_id"]

    assert (
        response.status_code == expected_status_code
    ), "4. `POST /orders` wrong status code"

    # 5. Vérifiez le stock encore une fois (`GET /stocks/:id`)
    response = client.get(f"/stocks/{product_id}", content_type="application/json")
    expected_status_code = 201

    assert (
        response.status_code == expected_status_code
    ), "5. `GET /stocks/:id` wrong status code"
    data = response.get_json()
    assert stock_quantity - order_quantity == data["quantity"]

    # 6. Étape extra: supprimez la commande et vérifiez le stock de nouveau.
    # Le stock devrait augmenter après la suppression de la commande.
    response = client.delete(f"/orders/{order_id}")
    expected_status_code = 200

    assert (
        response.status_code == expected_status_code
    ), "6. `DELETE /orders/:id` wrong status code"
    data = response.get_json()
    assert data["deleted"]

    # Vérifiez le stock encore une fois (`GET /stocks/:id`)
    response = client.get(f"/stocks/{product_id}", content_type="application/json")
    expected_status_code = 201

    assert (
        response.status_code == expected_status_code
    ), "6. `GET /stocks/:id` wrong status code"
    data = response.get_json()
    assert stock_quantity == data["quantity"]
