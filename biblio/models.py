import os
import sys
from datetime import datetime

from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Column, VARCHAR, create_engine, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session, relationship

sys.path.append('.')

SQL_URI = os.environ.get('SQL_URI')

if SQL_URI:
    engine = create_engine(SQL_URI, pool_recycle=600)
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    Base = declarative_base()
    Base.query = session.query_property()
else:
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

    def __str__(self):
        return '{} ISBN {} Autores {}'.format(self.Title, self.RowKey, self.Authors)


class Pessoa(Base):
    __tablename__ = 'pessoas'
    ID = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(50))

    def __str__(self):
        return self.nome


class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    ID = Column(Integer, primary_key=True)
    pessoa = relationship(Pessoa)
    pessoa_id = Column(Integer, ForeignKey('pessoas.ID'))
    livro = relationship(Livro)
    livro_id = Column(Integer, ForeignKey('livros.ID'))
    inicio = Column(TIMESTAMP, index=True)
    devolucao = Column(TIMESTAMP, index=True)

    @property
    def get_pessoa(self):
        return self.pessoa.nome

    @property
    def get_livro(self):
        return self.livro.Title

    @property
    def get_data(self):
        if self.inicio:
            return datetime.strftime(self.inicio, '%d/%m/%y %H:%M')
        return ''


class LivroView(ModelView):
    column_searchable_list = ['RowKey', 'Title']
    column_filters = ['Subject', 'estante']


class PessoaView(ModelView):
    column_searchable_list = ['nome']


class EmprestimoView(ModelView):
    column_filters = ['pessoa', 'livro']


if __name__ == '__main__':
    # sys.exit(0)
    Base.metadata.create_all(engine)
    """
    with open('livros.csv') as csv_in:
        reader = csv.DictReader(csv_in)
        for linha in reader:
            livro = Livro(**linha)
            session.add(livro)
    session.commit()
    """
