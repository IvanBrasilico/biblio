import sys

from flask import Flask
from flask_admin import Admin

sys.path.append('.')
from biblio.models import Livro, session, LivroView

SECRET = 'secret'

app = Flask(__name__)
app.secret_key = SECRET

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Flask and Flask-SQLAlchemy initialization here
admin = Admin(app, name='biblio', template_mode='bootstrap3')
admin.add_view(LivroView(Livro, session))

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
    app.logger.info('db_session remove')

if __name__ == '__main__':
    app.run(threaded=False, debug=True)
