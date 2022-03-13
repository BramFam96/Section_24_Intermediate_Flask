"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


def update_db(data):
  if type(data) is list:
    db.session.add_all(data);
    db.session.commit();
  else:
    db.session.add(data);
    db.session.commit();


def delete_data(data):
  db.session.delete(data);
  db.session.commit();


# MODELS GO BELOW!

class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, default='https://tinyurl.com/demo-cupcake')

    def serialize(self):
      """Serialize a cupcake SQLAlchemy obj to dictionary."""
      return {
        "id": self.id,
        "flavor": self.flavor,
        "size": self.size,
        "rating": self.rating,
        "image": self.image,
    }