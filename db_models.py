import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

users_words = sq.Table('users_words', Base.metadata,
    sq.Column('user_id', sq.Integer, sq.ForeignKey('users.id')),
    sq.Column('word_id', sq.Integer, sq.ForeignKey('words.id'))
)

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key=True)
    words = relationship('Words', secondary=users_words, backref="users")

class Words(Base):
    __tablename__ = 'words'
    id = sq.Column(sq.Integer, primary_key=True)
    word = sq.Column(sq.String(length=20), nullable=False)
    tr = sq.Column(sq.String(length=20), nullable=False)
    var_1 = sq.Column(sq.String(length=20), nullable=False)
    var_2 = sq.Column(sq.String(length=20), nullable=False)
    var_3 = sq.Column(sq.String(length=20), nullable=False)
    is_base = sq.Column(sq.Boolean)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def new_user(session, message):
    user = session.query(Users).filter(Users.id == message.from_user.id).first()
    if not user:
        user = Users(id=message.from_user.id)
        session.add(user)
        session.commit()
        base_words = session.query(Words).filter(Words.is_base == True).all()
        for word in base_words:
            session.execute(users_words.insert().values(user_id=user.id, word_id=word.id))
        session.commit()

def get_word(session, message):
    word = session.query(Words).join(users_words) \
    .filter(users_words.c.user_id == message.from_user.id) \
    .order_by(sq.func.random()).first()
    return word

def del_word(session, message, word_to_del):
    word = session.query(users_words).filter(users_words.c.word_id == Words.id) \
        .filter(users_words.c.user_id == message.from_user.id) \
        .filter(Words.word.ilike(word_to_del)).first()
    if word:
        session.query(users_words).filter(users_words.c.word_id == Words.id) \
            .filter(users_words.c.user_id == message.from_user.id) \
            .filter(Words.word.ilike(word_to_del)).delete()
        session.commit()
        return 'Слово удалено ❌ Продолжаем?'
    else:
        return 'Слово не найдено!\nНажмите дальше ⏭, чтобы продолжить тренинг'

def add_word(session, message, added_word):
    word = Words(**added_word)
    session.add(word)
    session.commit()
    session.execute(users_words.insert().values(user_id=message.from_user.id, word_id=word.id))
    session.commit()