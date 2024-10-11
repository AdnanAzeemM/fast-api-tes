from sqlmodel import SQLModel, create_engine


# Replace with your own PostgreSQL instance
DATABASE_URL = 'postgresql://fastapi_user:password@localhost/fastapi_db'

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)