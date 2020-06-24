import csv
import sys

from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Column, VARCHAR, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

sys.path.append('.')

from mysql import SQL_URI

if not SQL_URI:
    SQL_URI = 'sqlite:///biblio.db'

engine = create_engine(SQL_URI)

session = Session(engine)
Base = declarative_base()


class Livro(Base):
    __tablename__ = 'livros'
    ID = Column(Integer, primary_key=True)
    RowKey = Column(VARCHAR(20))
    Title = Column(VARCHAR(200))
    Colection = Column(VARCHAR(200))
    Subject = Column(VARCHAR(200))
    Authors = Column(VARCHAR(200))
    estante = Column(VARCHAR(10))


class LivroView(ModelView):
    column_searchable_list = ['RowKey', 'Title']
    column_filters = ['Subject', 'estante']


if __name__ == '__main__':
    # sys.exit(0)
    Base.metadata.create_all(engine)
    with open('livros.csv') as csv_in:
        reader = csv.DictReader(csv_in)
        for linha in reader:
            livro = Livro(**linha)
            session.add(livro)
    session.commit()
