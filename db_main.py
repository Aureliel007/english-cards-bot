from datetime import datetime
from configparser import ConfigParser
import json

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from db_models import create_tables, Users, Words, users_words

config = ConfigParser()
config.read('config.ini')
engine = sq.create_engine(config['Settings']['DSN'])

# Создаем таблицы
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Записываем базовый набор слов в базу
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for word in data:
    session.add(Words(**word))
session.commit()

session.close()
