from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from Models.Base import Base
# need the imports to create the db
import Models.ProductModel
import Models.UserModel
import Models.SaleItemModel
import Models.SaleModel
import Models.RefundModel
import os

def get_app_data_folder():
    app_name = "Store Manager"
    appdata = os.getenv('LOCALAPPDATA')
    app_folder = os.path.join(appdata, app_name)
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    return app_folder


app_folder = get_app_data_folder()
db_path = os.path.join(app_folder, 'store.db')

engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
