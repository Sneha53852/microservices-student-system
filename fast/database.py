import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# No default on purpose: a missing setting should fail loudly, and
# credentials must never live in the code.
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()