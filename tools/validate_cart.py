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
    client = Client()
    response = client.get("/carrinho/", HTTP_HOST="localhost")
    body = response.content.decode("utf-8", errors="ignore")
    print(response.status_code)
    print("{{ cart.get_total_price" in body)


if __name__ == "__main__":
    main()
