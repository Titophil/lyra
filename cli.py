#!/usr/bin/env python3
import typer
import sys
from lib.seed import seed_all
from lib.db.database import SessionLocal
from lib.models import Base, Crypto, User, Holding, Transaction



app = typer.Typer()

@app.command()
def seed():
    """Seed the database with initial data."""
    seed_all()

@app.command()
def list_users(limit: int = 10):
    """List users in the system."""
    session = SessionLocal()
    users = session.query(User).limit(limit).all()
    for user in users:
        typer.echo(f"{user.id} | {user.username} | {user.email}")
    session.close()

@app.command()
def user_holdings(user_id: int = typer.Option(..., help="ID of the user")):
    """Display holdings for a specific user."""
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        typer.echo("❌ User not found.")
        return
    typer.echo(f"🧾 Holdings for {user.username}:")
    for holding in user.holdings:
        typer.echo(f"- {holding.crypto.symbol}: {holding.amount}")
    session.close()

@app.command()
def transactions(user_id: int = typer.Option(..., help="ID of the user")):
    """List transactions for a user."""
    session = SessionLocal()
    txs = session.query(Transaction).filter_by(user_id=user_id).all()
    for tx in txs:
        typer.echo(f"{tx.timestamp} | {tx.type.upper()} | {tx.crypto_symbol} | {tx.amount} @ ${tx.price_usd}")
    session.close()

@app.command()
def add_user(username: str, email: str, password: str):
    """Add a new user."""
    session = SessionLocal()
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
    typer.echo(f"✅ Created user {username}")
    session.close()

@app.command()
def buy(user_id: int, symbol: str, amount: float, price: float):
    """Buy crypto for a user."""
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    crypto = session.query(Crypto).filter_by(symbol=symbol.upper()).first()

    if not user or not crypto:
        typer.echo("❌ User or Crypto not found.")
        return

    holding = session.query(Holding).filter_by(user_id=user.id, crypto_id=crypto.id).first()
    if holding:
        holding.amount += amount
    else:
        holding = Holding(user_id=user.id, crypto_id=crypto.id, crypto_symbol=crypto.symbol, amount=amount)
        session.add(holding)

    tx = Transaction(user_id=user.id, crypto_symbol=crypto.symbol, amount=amount, price_usd=price, type="buy")
    session.add(tx)

    session.commit()
    typer.echo(f"💸 Bought {amount} {symbol.upper()} at ${price}")
    session.close()

@app.command()
def sell(user_id: int, symbol: str, amount: float, price: float):
    """Sell crypto for a user."""
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    crypto = session.query(Crypto).filter_by(symbol=symbol.upper()).first()

    if not user or not crypto:
        typer.echo("❌ User or Crypto not found.")
        return

    holding = session.query(Holding).filter_by(user_id=user.id, crypto_id=crypto.id).first()
    if not holding or holding.amount < amount:
        typer.echo("❌ Insufficient holdings.")
        return

    holding.amount -= amount
    if holding.amount == 0:
        session.delete(holding)

    tx = Transaction(user_id=user.id, crypto_symbol=crypto.symbol, amount=amount, price_usd=price, type="sell")
    session.add(tx)

    session.commit()
    typer.echo(f"✅ Sold {amount} {symbol.upper()} at ${price}")
    session.close()

@app.command()
def portfolio_value(user_id: int):
    """Calculate total portfolio value in USD."""
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        typer.echo("❌ User not found.")
        return

    total = 0.0
    for h in user.holdings:
        total += h.amount * h.crypto.price_usd
    typer.echo(f"📊 Portfolio value: ${total:,.2f}")
    session.close()

@app.command()
def crypto_rank(symbol: str = typer.Argument(..., help="Symbol of the cryptocurrency")):
    """Check the ranking of a cryptocurrency."""
    session = SessionLocal()
    crypto = session.query(Crypto).filter(Crypto.symbol == symbol.upper()).first()
    if not crypto:
        typer.echo(f"❌ Cryptocurrency with symbol '{symbol}' not found.")
    else:
        typer.echo(f"🏅 {crypto.name} ({crypto.symbol}) is ranked #{crypto.rank}")
    session.close()

@app.command()
def delete_user(user_id: int):
    """Delete a user and all their related data (holdings, transactions)."""
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        typer.echo("❌ User not found.")
        return

    session.delete(user)
    session.commit()
    session.close()

    typer.echo(f"✅ User {user.username} (ID: {user_id}) has been deleted.")


def interactive_menu():
    commands = {
        "1": ("Seed the database with initial data", seed),
        "2": ("List users", list_users),
        "3": ("Display holdings for a user", user_holdings),
        "4": ("List transactions for a user", transactions),
        "5": ("Add a new user", add_user),
        "6": ("Buy crypto for a user", buy),
        "7": ("Sell crypto for a user", sell),
        "8": ("Calculate total portfolio value", portfolio_value),
        "9": ("Check crypto ranking", crypto_rank),
        "10": ("Delete a user", delete_user),
        "q": ("Quit", None)
    }

    while True:
        typer.echo("\nChoose an option:")
        for key, (desc, _) in commands.items():
            typer.echo(f"{key}. {desc}")

        choice = input("Enter your choice: ").strip()

        if choice == "q":
            typer.echo("Exiting...")
            sys.exit(0)

        cmd = commands.get(choice)
        if not cmd:
            typer.echo("Invalid choice, try again.")
            continue

        desc, func = cmd


        if func == seed:
            func()
        elif func == list_users:
            limit = input("Enter limit (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            func(limit=limit)
        elif func == user_holdings:
            user_id = input("Enter user ID: ").strip()
            if user_id.isdigit():
                func(user_id=int(user_id))
            else:
                typer.echo("Invalid user ID.")
        elif func == transactions:
            user_id = input("Enter user ID: ").strip()
            if user_id.isdigit():
                func(user_id=int(user_id))
            else:
                typer.echo("Invalid user ID.")
        elif func == add_user:
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            func(username=username, email=email, password=password)
        elif func == buy:
            try:
                user_id = int(input("User ID: ").strip())
                symbol = input("Crypto Symbol: ").strip()
                amount = float(input("Amount: ").strip())
                price = float(input("Price: ").strip())
                func(user_id=user_id, symbol=symbol, amount=amount, price=price)
            except ValueError:
                typer.echo("Invalid input.")
        elif func == sell:
            try:
                user_id = int(input("User ID: ").strip())
                symbol = input("Crypto Symbol: ").strip()
                amount = float(input("Amount: ").strip())
                price = float(input("Price: ").strip())
                func(user_id=user_id, symbol=symbol, amount=amount, price=price)
            except ValueError:
                typer.echo("Invalid input.")
        elif func == portfolio_value:
            user_id = input("User ID: ").strip()
            if user_id.isdigit():
                func(user_id=int(user_id))
            else:
                typer.echo("Invalid user ID.")
        elif func == crypto_rank:
            symbol = input("Crypto Symbol: ").strip()
            func(symbol=symbol)
        elif func == delete_user:
            user_id = input("User ID: ").strip()
            if user_id.isdigit():
                func(user_id=int(user_id))
            else:
                typer.echo("Invalid user ID.")


@app.command()
def menu():
    interactive_menu()


if __name__ == "__main__":
    app()

