import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


def main():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    api_key = os.getenv("COINGECKO_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Preencha COINGECKO_API_KEY no .env.")

    params = {
        "ids": "bitcoin",
        "vs_currencies": "brl",
        "include_last_updated_at": "true",
    }
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params=params,
            headers={"x-cg-demo-api-key": api_key},
            timeout=30,
        )
    except requests.RequestException:
        raise SystemExit("Falha de conexao com o CoinGecko.") from None

    if response.status_code != 200:
        raise SystemExit(f"CoinGecko respondeu HTTP {response.status_code}.")

    try:
        bitcoin = response.json()["bitcoin"]
        price = bitcoin["brl"]
        if isinstance(price, bool) or not isinstance(price, (int, float)) or not 0 < price < float("inf"):
            raise ValueError()
        timestamp = bitcoin["last_updated_at"]
        if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)) or timestamp <= 0:
            raise ValueError()
        source_time = datetime.fromtimestamp(timestamp, timezone.utc)
    except (ValueError, KeyError, TypeError, OverflowError, OSError):
        raise SystemExit("Resposta inesperada: preco ou horario ausente/invalido.") from None

    print(json.dumps({
        "coin_id": "bitcoin",
        "quote_currency": "brl",
        "price": price,
        "source_updated_at": source_time.isoformat(),
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))


if __name__ == "__main__":
    main()
