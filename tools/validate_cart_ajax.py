import os
import sys
from pathlib import Path

import django
from django.test import Client


def main():
    base_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopmarket.settings")
    django.setup()

    from catalog.models import Product

    product = Product.objects.filter(is_active=True).first()
    if not product:
        print("No active product found to test AJAX.")
        return

    client = Client()
    add_response = client.post(
        f"/carrinho/add/{product.id}/",
        {"quantity": 1},
        HTTP_HOST="localhost",
    )
    print("add_status", add_response.status_code)

    ajax_response = client.post(
        "/carrinho/update-ajax/",
        {"product_id": product.id, "quantity": 2},
        HTTP_HOST="localhost",
    )
    print("ajax_status", ajax_response.status_code)
    try:
        print(ajax_response.json())
    except ValueError:
        print(ajax_response.content.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()
