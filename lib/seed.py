from lib.models import Base, Crypto
from lib.db.database import engine, SessionLocal
import requests

def get_crypto_prices():
    url = "https://api.coinlore.net/api/tickers/?limit=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()["data"]
    else: 
        raise Exception("Failed to fetch prices")
    

def seed_cryptos():
    Base.metadata.create_all(bind = engine)

    session = SessionLocal()
    cryptos = get_crypto_prices()

    for data in cryptos:
        existing = session.query(Crypto).filter_by(symbol = data["symbol"]).first()
        if existing:
            continue

        crypto = Crypto(
            id=int(data["id"]),
            symbol=data["symbol"],
            name=data["name"],
            name_id=data["nameid"],
            rank=int(data["rank"]),
            price_usd=float(data["price_usd"]),
            percent_change_24hrs=float(data.get("percent_change_24h", 0.0)),
            percent_change_1hrs=float(data.get("percent_change_1h", 0.0)),
            percent_change_7d=float(data.get("percent_change_7d", 0.0)),
            price_btc=float(data["price_btc"]),
            market_cap_usd=float(data["market_cap_usd"]),
            volume24=float(data["volume24"]),
            volume24a=float(data["volume24a"]),
            csupply=float(data["csupply"]),
            tsupply=float(data["tsupply"]),
            msupply=float(data["msupply"]) if data["msupply"] else None,
        )
        session.add(crypto)
        
    session.commit()
    session.close()
    print("✅ Crypto data successfully saved to the database.")



if __name__ == "__main__":
   seed_cryptos()
