from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Vendor, MenuItem, Review, Base

engine = create_engine('sqlite:///columbia.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import Vendor, MenuItem, Review, Base
    Base.metadata.create_all(bind=engine)

@app.route('/', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        search = request.form['menuItem']
        entries = db_session.query(MenuItem).filter(MenuItem.name.contains(search)).order_by(MenuItem.likes.desc()).all()
    else:
        entries = db_session.query(MenuItem).order_by(MenuItem.likes.desc()).all()
    return render_template('search_results.html', entries=entries, neighborhood="Crown Heights")


if __name__ == '__main__':
    init_db()
    app.run()
