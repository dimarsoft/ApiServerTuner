import sqlalchemy
import databases
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./request_info.db"

# создаем таблицу в базе данных
metadata = sqlalchemy.MetaData()

requests_table = sqlalchemy.Table(
    "requests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("mode", sqlalchemy.String),
    sqlalchemy.Column("file", sqlalchemy.String),
    sqlalchemy.Column("image_class", sqlalchemy.String),
    sqlalchemy.Column("time_elapsed", sqlalchemy.String),
    sqlalchemy.Column("start_time", sqlalchemy.String),
    sqlalchemy.Column("end_time", sqlalchemy.String)
)

# настройка подключения к базе данных
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
# Удаление таблицы "requests" из базы данных
# requests.drop(engine)

metadata.create_all(engine)
