from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

db_url="mysql+pymysql://root:PoonaM123@localhost:3306/finance_records"

engine=create_engine(url=db_url,echo=True)

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()


def getdb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()