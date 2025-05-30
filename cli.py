# cli.py
import typer
from lib.seed import seed_all
from lib.db.database import SessionLocal
from lib.models import User, Holding, Crypto, Transaction

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

if __name__ == "__main__":
    app()
