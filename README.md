# lyra
# 💹 Lyra Crypto CLI App

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()

Lyra is a command-line application built with Python that helps manage and simulate crypto portfolios using real-time data. It uses SQLAlchemy ORM for database interactions and supports core operations like viewing user holdings, seeding data, and tracking transactions.

---

## 📦 Features

- ✅ Seed real-time top 10 cryptocurrencies from Coinlore API
- 👤 Create 10,000 fake users with Faker
- 💼 Assign random holdings to users
- 💰 Track user crypto holdings and transactions
- 🧠 Built with SQLAlchemy ORM and Python
- 🧪 Fully CLI-based for quick testing and interaction

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lyra.git
cd lyra
2. Set Up Virtual Environment
bash
Copy
Edit
pipenv install
pipenv shell
3. Seed the Database
bash
Copy
Edit
python cli.py seed
This fetches live crypto data and populates the database with users and holdings.

🛠 CLI Commands
Run all commands from the project root directory.

🔄 Seed Database
bash
Copy
Edit
python cli.py seed
👥 List Users
bash
Copy
Edit
python cli.py list-users
💼 View User Holdings
bash
Copy
Edit
python cli.py user-holdings USER_ID
📜 View User Transactions
bash
Copy
Edit
python cli.py transactions USER_ID
⚙️ Installing as a CLI Package
To make Lyra globally accessible from the command line:

1. Create setup.py
python
Copy
Edit
from setuptools import setup, find_packages

setup(
    name='lyra',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
        'SQLAlchemy',
        'requests',
        'Faker',
    ],
    entry_points={
        'console_scripts': [
            'lyra=cli:cli',
        ],
    },
)
2. Install Locally
bash
Copy
Edit
pip install -e .
3. Use Anywhere
bash
Copy
Edit
lyra seed
lyra list-users
lyra user-holdings 1
lyra transactions 1
📂 Project Structure
csharp
Copy
Edit
lyra/
├── cli.py                  # CLI entry-point (Click commands)
├── lib/
│   ├── __init__.py
│   ├── seed.py             # Seeding logic
│   ├── models.py           # SQLAlchemy models
│   └── db/
│       ├── __init__.py
│       └── database.py     # Engine and session
├── setup.py
├── Pipfile
├── Pipfile.lock
└── README.md
✅ Learning Goals Checklist
Goal	Status
CLI app solving real-world problem	✅ Met
SQLAlchemy ORM with 3+ related tables	✅ Met
Virtual environment managed with Pipenv	✅ Met
Organized, modular package structure	✅ Met
Use of lists, dicts, and tuples	✅ Met

🙌 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss improvements.

📝 License
This project is licensed under the MIT License – see the LICENSE file for details.

yaml
Copy
Edit
