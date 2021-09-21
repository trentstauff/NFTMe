from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from NFTMe.__init__ import db, login_manager, app, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    money = db.Column(db.Float)

    nfts = db.relationship("UserNFT", backref="owner", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# UserNFT model (IE a single NFT)
class UserNFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    nft_image = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=100000000)
    timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.String(40), nullable=False)
