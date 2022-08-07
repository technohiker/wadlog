
from datetime import datetime, date
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    """Registered users."""

    __tablename__ = 'users'

    def __repr__(self):
        return f'<User: #{self.id} #{self.username}, Mod: #{self.email}'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True)

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True)

    password = db.Column(
        db.Text,
        nullable=False)

    date_joined = db.Column(
        db.Date,
        nullable=False,
        default=datetime.utcnow())

    image_url = db.Column(
        db.Text,
        default='/static/images/default_profile.png')

    #user_mods = db.relationship('user_mods')

  #  comments = db.relationship('comments')

  #  user_logs = db.relationship('user_logs',
  #      secondary='user_mods'
  #      )

  # [print(log) for log in mod.user_logs for mod in user1.user_mods]

    #Register user.
    @classmethod
    def signup(cls, username, password, email, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')



        user = Users(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Check if user and password matches."""
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Mods(db.Model):
    """Information of the various mods users can download."""

    __tablename__ = 'mods'

    def __repr__(self):
        return f'<Mod: #{self.id} Title: #{self.title}'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.Text,
        nullable=False
    )

    file_id = db.Column(
        db.Integer,
        nullable=False,
        unique=True
    )

    url = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    date_uploaded = db.Column(
        db.Date,
        nullable=False
    )

    date_updated = db.Column(
        db.Date,
        default=datetime.now().strftime('%Y-%m-%d'),
        nullable=False
    )

    author = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.Text,
        nullable=False
    )

    rating = db.Column(
        db.Float,
        default=0
    )

    rating_count = db.Column(
        db.Integer,
        nullable=False
    )

class User_Mods(db.Model):
    """A user's record of a mod they own."""

    __tablename__ = 'user_mods'

    def __repr__(self):
        return f'<User_Mod: #{self.id} User: #{self.user_id}, Mod: #{self.mod_id}'


    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete='cascade')
    )

    mod_id = db.Column(
        db.Integer,
        db.ForeignKey('mods.id',ondelete='cascade')
    )

    date_added = db.Column(
        db.Date,
        default=datetime.utcnow(),
        nullable=False
    )

    user_review = db.Column(
        db.Text
    )

    user_notes = db.Column(
        db.Text
    )

    play_status = db.Column(
        db.Text,
        nullable=False, #Should probably be enum.
        default="Not Playing"
    )

    now_playing = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    user = db.relationship('Users',backref='user_mods')

    mod = db.relationship('Mods',backref='user_mods')

    db.UniqueConstraint(user_id,mod_id,name='user_mod_unique')

class User_Logs(db.Model):

    __tablename__ = 'user_logs'

    def __repr__(self):
        return f'<User_Log: #{self.id} User_Mod: #{self.user_mod_id}, {self.activity_type}, {self.description}'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    user_mod_id = db.Column(
        db.Integer,
        db.ForeignKey('user_mods.id',ondelete='cascade')
    )
    
    date_added = db.Column(
        db.DateTime,
        nullable=False
    )

    activity_type = db.Column(
        db.Text,
        nullable=False #Should probably be enum.
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

  #  user = db.relationship('Users',secondary='user_mods', backref='user_logs')
    user_mod = db.relationship('User_Mods',backref='user_logs')
  #  mod = db.relationship('Mods', secondary='user_mods',backref='user_logs')

  # Enabling the above relationships causes SQLAlchemy warnings about conflicting relationships.

class Comments(db.Model):

    __tablename__ = 'comments'

    def __repr__(self):
        return f'<Comment: #{self.id} User ID: #{self.user_id}, Target User: #{self.target_user}, {self.time}, {self.text}'


    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete='cascade')
    )

    target_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete='cascade')
    )

    time = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    users = db.relationship('Users',backref='comments',foreign_keys=user_id)