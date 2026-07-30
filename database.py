from cryptography.fernet import Fernet
from sqlalchemy import Column, Integer, String, create_engine, UniqueConstraint, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

# getting data out of .env file
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY").encode()
cipher=Fernet(SECRET_KEY)  # creating symmetric encryption, so unnoticed changes were impossible
path=os.getenv("DATABASE_URL")

Base=declarative_base()

# class of database
class UserPasswords(Base):
    __tablename__="user_passwords"

    id=Column(Integer, primary_key=True)
    where_used=Column(String, nullable=False)
    username=Column(String, nullable=False)
    password=Column(String, nullable=False)

    __table_args__=(
        UniqueConstraint("where_used", "username", name="_where_used_username"),
    )  # no repeating where_used with username (separately possible)

    def set_password(self, simple_password: str):
        """
        Function gets starting password(e.g. 12345), which is turn into ciphered one
        """

        encrypted=cipher.encrypt(simple_password.encode("utf-8"))

        self.password=encrypted.decode("utf-8")

    def get_password(self):
        """
        Function return unencrypted password
        """
        if not self.password:
            return None

        decrypted=cipher.decrypt(self.password.encode("utf-8"))

        return decrypted.decode("utf-8")

# Creating engine and class Session for future sessions

engine=create_engine(path)
Session=sessionmaker(bind=engine)