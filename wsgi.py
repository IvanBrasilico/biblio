import sys

sys.path.append('.')
from biblio.main import app

if __name__ == '__main__':
    app.run(debug=True)