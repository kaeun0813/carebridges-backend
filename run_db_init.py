# run_db_init.py
from app.db.session import engine
from app.db.base import Base
from app import models  # 반드시 모델을 import

Base.metadata.create_all(bind=engine)
print("테이블 생성 완료!")
from sqlalchemy import inspect
from app.db.session import engine

inspector = inspect(engine)
print(inspector.get_table_names())
