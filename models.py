from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# class Cupcakes(db.Model):

#     __tablename__ = 'Cupcakes'

#     id = db.Column(db.Integer,
#                     primary_key=True,
#                     autoincrement=True)
#     flavor = db.Column(db.Text,
#                     nullable=False)
#     size = db.Column(db.Text,
#                     nullable=False)
#     rating = db.Column(db.Float,
#                     nullable=False)
#     image = db.Column(db.Text)

#     def serialize(self):
#         """Returns a JSON-compatible object.  In this case, a dictionary."""
#         return {
#             'id': self.id,
#             'flavor': self.flavor,
#             'size': self.size,
#             'rating': self.rating,
#             'image': self.image
#         }