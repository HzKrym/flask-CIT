from flask import Flask, render_template, request, abort
from sqlalchemy import create_engine

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

app = Flask(__name__)
engine = create_engine("sqlite:///D:\\projects\\python\\flask-test\\db\\mySite.db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
User.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name1=name)

@app.route('/user/<id>')
def user_by_id(id):
    session = Session(engine)
    user = session.query(User).get(id)
    return render_template('user.html', name=user.name, fullname=user.fullname)

@app.route('/add_user')
def add_user_page():
    return render_template('add_user.html')

@app.route('/user', methods=['POST'])
def add_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    
    name = request.json('name')
    fullname = request.json.get('fullname', '')
    user = User(name = name, fullname = fullname)

    session = Session(engine)
    session.add(user)
    session.commit()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404