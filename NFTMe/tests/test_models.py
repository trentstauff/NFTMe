from NFTMe.models import User, UserNFT
from NFTMe.__init__ import app, db, bcrypt


#### This file of unit tests ensures the functionality of the models are as expected. ####
def test_new_user():
    """
    GIVEN a username, email, password, and balance
    WHEN a new User is created
    THEN check if the email, username, (hashed) password, and balance are correctly set
    """

    email = "test@test.com"
    username = "test"
    password = "password"
    balance = 100

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(username=username, email=email, password=hashed_password, money=balance)
    assert user.email == "test@test.com"
    assert user.password != "password"
    assert user.money == 100


def test_new_nft():
    """
    GIVEN a user, a title, status, price, and photo
    WHEN a new UserNFT is created
    THEN check if all fields have been set properly
    """

    user = User(
        username="test", email="test@test.com", password="password", money=10000
    )
    title = "my nft"
    status = 1
    price = 1000
    photo = "/static/nfts/hello.png"

    nft = UserNFT(
        title=title,
        status=status,
        price=price,
        nft_image=photo,
        username=user.username,
        user_id=user.id,
    )
    assert nft.username == "test"
    assert nft.user_id == user.id
    assert nft.title == "my nft"
    assert nft.status == 1
    assert nft.price == 1000
    assert nft.nft_image == "/static/nfts/hello.png"


# In the future, more tests here...
