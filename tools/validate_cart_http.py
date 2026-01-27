import urllib.request


def main():
    url = "http://127.0.0.1:8000/carrinho/"
    with urllib.request.urlopen(url, timeout=10) as response:
        body = response.read().decode("utf-8", errors="ignore")
        print(response.status)
        print(response.headers.get("Cache-Control"))
        print(response.headers.get("Pragma"))
        print("{{ cart.get_total_price" in body)


if __name__ == "__main__":
    main()
