import os
from dotenv import load_dotenv


class Setup:

    def __init__(self, env: str) -> None:
        """env: The environment to get envvars from"""
        load_dotenv(env)
        self.POSTGRES_PROTO = os.getenv("POSTGRES_PROTO")
        self.POSTGRES_LOGIN = os.getenv("POSTGRES_LOGIN")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")
        self.POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
    
    @property
    def database_url(self) -> str:
        if not all([
            self.POSTGRES_PROTO,
            self.POSTGRES_LOGIN,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB_NAME,
        ]):
            raise ValueError("PostgresQL db url should be full")

        _db_url = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            self.POSTGRES_PROTO,
            self.POSTGRES_LOGIN,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB_NAME,
        )
        return _db_url
        

# Input the filename from which the program could get envvars
setup = Setup(".env")