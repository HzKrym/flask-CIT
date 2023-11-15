from flask import Flask, render_template, request, abort, jsonify

from sqlalchemy import create_engine, ForeignKey, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker

from sqlalchemy.orm.exc import NoResultFound

from typing import List, Optional

app = Flask(__name__)
engine = create_engine('sqlite:///db///users.db')
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'user_account'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30))
  fullname: Mapped[Optional[str]]

  def __repr__(self) -> str:
    return f'User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})'

User.metadata.create_all(engine)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/add_user')
def add_user_page():
  return render_template('add_user.html')

@app.route('/user', methods=['POST'])
def add_user():
  if not request.json or not 'name' in request.json:
    return render_template('404.html', error='Invalid request'), 404
    
  name = request.json.get('name', '')
  fullname = request.json.get('fullname', '')

  with Session() as session:
    try:
      existing_user = session.query(User).filter_by(name=name).one()
      existing_user.fullname = fullname
      session.commit()
      message = f'User {name} updated successfully!'
      print(message)
      return jsonify({'message': message})

    except NoResultFound:
      user = User(name=name, fullname=fullname)
      session.add(user)
      session.commit()
      message = f'User {name} added successfully!'
      print(message)
      return jsonify({'message': message})

    except Exception as e:
      return render_template('404.html', error=str(e)), 404

@app.route('/user/<name>')
def user_by_name(name):
  with Session() as session:
    try:
      user = session.query(User).filter_by(name=name).one()
      return render_template('user.html', name=user.name, fullname=user.fullname)
    except NoResultFound:
      return render_template('404.html', error=f'User with name {name} not found'), 404
    except Exception as e:
      return render_template('404.html', error=str(e)), 404

@app.route('/users')
def all_users():
    with Session() as session:
        users = session.query(User).all()
        return render_template('users.html', users=users)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=str(error)), 404

if __name__ == '__main__':
    app.run(debug=True)
    