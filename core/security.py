from passlib.context import CryptContext


class PasswordHelper:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(secret=plain_password, hash=hashed_password)
