import json
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

users_words = sq.Table('users_words', Base.metadata,
    sq.Column('user_id', sq.Integer, sq.ForeignKey('users.id', ondelete='CASCADE')),
    sq.Column('word_id', sq.Integer, sq.ForeignKey('words.id', ondelete='CASCADE'))
)

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key=True)
    words = relationship('Words', secondary=users_words, back_populates='users')

class Words(Base):
    __tablename__ = 'words'
    id = sq.Column(sq.Integer, primary_key=True)
    rus = sq.Column(sq.String(length=20), nullable=False)
    eng = sq.Column(sq.String(length=20), nullable=False)
    users = relationship('Users', secondary=users_words, back_populates='words', cascade='all, delete')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def upload_words(session):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for word in data:
        session.add(Words(**word))
    session.commit()

def new_user(session, message):
    user = session.query(Users).filter(Users.id == message.from_user.id).first()
    if not user:
        user = Users(id=message.from_user.id)
        session.add(user)
        session.commit()

def get_word(session, message):
    q = session.query(Words.rus, Words.eng) \
        .outerjoin(users_words).filter(sq.or_(
            users_words.c.user_id == None,
            users_words.c.user_id == message.from_user.id
            )).order_by(sq.func.random()).limit(4).all()
    word = {'word': q[0][0], 'tr': q[0][1], 'var_1': q[1][1], 'var_2': q[2][1], 'var_3': q[3][1]}
    return word

def del_word(session, message, word_to_del):
    q = session.query(Words).filter(Words.rus.ilike(word_to_del))
    word = q.first()
    if (word is not None) and word.users:
        user = word.users[0]
        if user.id == message.from_user.id:
            q.delete()
            session.commit()
            return 'Слово удалено ❌ Продолжаем?'
    else:
        return ('Слово не найдено!\n'
                'Вы можете удалить только добавленные Вами слова\n'
                'Нажмите дальше ⏭, чтобы продолжить тренинг')

def add_word(session, message, added_word):
    word = Words(**added_word)
    session.add(word)
    session.commit()
    session.execute(users_words.insert().values(user_id=message.from_user.id, word_id=word.id))
    session.commit()
