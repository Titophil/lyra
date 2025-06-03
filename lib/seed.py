from lib.db.database import engine, SessionLocal
from lib.models import Base, Crypto, User, Holding
import requests
from faker import Faker
import random

fake = Faker()

def get_crypto_prices():
    url = "https://api.coinlore.net/api/tickers/?limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else: 
        raise Exception("Failed to fetch prices")
    
def seed_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    cryptos = get_crypto_prices()
    for data in cryptos:
        existing = session.query(Crypto).filter_by(symbol=data["symbol"]).first()
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

    session.commit()  # Commit cryptos first

    # Create admin user if not exists
    admin_user = session.query(User).filter_by(username="admin").first()
    if not admin_user:
        admin_user = User(username="admin", email="admin@example.com", password="hashed_password")
        session.add(admin_user)
        session.commit()  # commit to get id

    users = []
    created_usernames = set()
    created_emails = set()

    for _ in range(10000):
        username = fake.user_name()
        email = fake.email()

        if username in created_usernames or email in created_emails:
            continue

        # Fix here: Use User.email instead of user.email in filter
        if session.query(User).filter((User.username == username) | (User.email == email)).first():
            continue

        user = User(username=username, email=email, password=fake.password())
        session.add(user)
        users.append(user)
        created_usernames.add(username)
        created_emails.add(email)

    session.commit()  # Commit all users so they have ids

    cryptos_in_db = session.query(Crypto).all()
    for user in users:
        for _ in range(random.randint(1, 3)):
            crypto = random.choice(cryptos_in_db)
            amount = round(random.uniform(0.01, 5.0), 4)
            holding = Holding(
                user_id=user.id,
                crypto_id=crypto.id,
                amount=amount,
                crypto_symbol=crypto.symbol  # add if required by model
            )
            session.add(holding)
    
    session.commit()
    session.close()
    print("✅ Seeded cryptos and users")

if __name__ == "__main__":
    seed_all()
