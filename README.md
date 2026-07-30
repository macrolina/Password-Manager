# Password Manager
**Lightweight program for encrypted storage for passwords, usernames, and associated services.**

Designed with an **Offensive/Defencive(Red/Blue Team)** tactics. 
Manager was built in Python, using **SQLAlchemy**, **Customtkinter** and **Cryptography** modules.

# Security Features:
- Usage of the Shannon formula of information entropy.
- Symmetric Encryption using Fernet from cryptography.
- High-Entropy Password Generator creates passwords with entropy greater than 100 bits.

# Tech Stack
- **Core language:** Python 3.12
- **Database & ORM:** SQLite, SQLAlchemy
- **Cryptography:** cryptography.Fernet
- **GUI:** CustomTkinter
- **Security Modules:** secrets, math, os

# Project Structure

```text
.env.example # Template for environment variables
.gitignore # Exludes .env, local .db, and __pycache__
check_security.py # File for class of security(passwords checks etc.)
database.py # File for database creation and additional features
main.py # File of GUI and starting file
README.md # Project documantation
requirements.txt # List of required Python packages
```

# Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/macrolina/Password-Manager.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```
