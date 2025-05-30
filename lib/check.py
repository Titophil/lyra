from lib.models import Crypto, User
from lib.db.database import SessionLocal

def check_seed_data():
    session = SessionLocal()


    print("\n===Sample Cryptocurrencies ===")
    cryptos = session.query(Crypto).limit(5).all()
    for crypto in cryptos:
        print(f"{crypto.name} ({crypto.symbol}): ${crypto.price_usd}")

    print("\n=== Users ===")
    users = session.query(User).all()
    for user in users:
        print(f"Username: {user.username}, Balance: ${user.balance_usd}")

    session.close()

if __name__ == "__main__":
    check_seed_data()
