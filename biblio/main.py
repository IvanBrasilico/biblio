import sys

from flask import Flask, render_template
from flask_admin import Admin, BaseView, expose
from flask_babelex import Babel

sys.path.append('.')
from biblio.models import Livro, session, LivroView, Emprestimo, Pessoa, PessoaView, EmprestimoView

SECRET = 'secret'

app = Flask(__name__)
app.secret_key = SECRET
babel = Babel(app)


@babel.localeselector
def get_locale():
    return 'pt'


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Flask and Flask-SQLAlchemy initialization here
admin = Admin(app, name='biblio', template_mode='bootstrap3')
admin.add_view(LivroView(Livro, session))
admin.add_view(PessoaView(Pessoa, session))
admin.add_view(EmprestimoView(Emprestimo, session))


class HomeView(BaseView):
    @expose('/')
    def index(self):
        emprestimos_ativos = session.query(Emprestimo).filter(
            Emprestimo.devolucao.is_(None)).order_by(Emprestimo.inicio).all()
        return self.render('emprestimos.html', emprestimos=emprestimos_ativos)


admin.add_view(HomeView(name='Home', endpoint='home'))


@app.route('/')
def home():
    emprestimos_ativos = session.query(Emprestimo).filter(
        Emprestimo.devolucao.is_(None)).order_by(Emprestimo.inicio).all()
    return render_template('emprestimos.html', emprestimos=emprestimos_ativos)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
    app.logger.info('db_session remove')


if __name__ == '__main__':
    app.run(threaded=False, debug=True)
