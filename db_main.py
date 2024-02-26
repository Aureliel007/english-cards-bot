from datetime import datetime
from configparser import ConfigParser

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from db_models import create_tables, upload_words, Users, Words, users_words

config = ConfigParser()
config.read('config.ini')
engine = sq.create_engine(config['Settings']['DSN'])

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    create_tables(engine)   # Создаем таблицы
    upload_words(session)   # Записываем базовый набор слов в базу

session.close()
