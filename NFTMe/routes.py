import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from NFTMe.__init__ import app, db, bcrypt
from NFTMe.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    UploadForm,
    ModifyNFTForm,
)
from NFTMe.models import User, UserNFT
from flask_login import login_user, current_user, logout_user, login_required


# Home route, aka the NFT Marketplace.
@login_required
@app.route("/home")
def home():
    user = current_user
    nfts = UserNFT.query.all()
    return render_template("home.html", user=user, nfts=nfts)


# The about page, describing what NFTMe is.
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        rounded_money = round(form.money.data, 2)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            money=rounded_money,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


# Login page
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # if we have have a post request to log in rather than a form submission
    if request.method == "POST" and request.form.get("test", False):
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=False)
            return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", title="Login", form=form)


# Logout page
@app.route("/logout", methods=["GET", "POST"])
def logout(testing=False):
    logout_user()

    if testing:
        return True

    return redirect(url_for("login"))


# Account page, where users can update settings and see their NFTs.
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "profile")
            current_user.image_file = picture_file

        if form.money.data:
            current_user.money = round(form.money.data, 2)

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))

    # this is for the html to auto place the users current information on the page
    elif request.method == "GET":

        form.username.data = current_user.username
        form.email.data = current_user.email
        form.money.data = current_user.money

    image_file = "/static/profile_pics/" + current_user.image_file

    nfts = UserNFT.query.filter_by(user_id=current_user.id)

    return render_template(
        "account.html", title="Account", image_file=image_file, form=form, nfts=nfts
    )


# Where users can see their NFTs.
@app.route("/my_nfts", methods=["GET", "POST"])
@login_required
def my_nfts():

    nfts = UserNFT.query.filter_by(user_id=current_user.id)
    return render_template(
        "my_nfts.html", title="My NFTs", nfts=nfts, user=current_user
    )


# Allows users to buy NFTs for sale.
@app.route("/buy/<string:nft_id>", methods=["GET", "POST"])
@login_required
def buy(nft_id):

    nft = UserNFT.query.get(nft_id)
    buyer = current_user
    seller = User.query.filter_by(id=nft.user_id).first()

    if buyer.money < nft.price:
        flash("Sorry, you can't afford that NFT.", "danger")
        return redirect(url_for("home"))
    else:
        buyer.money -= round(nft.price, 2)
        seller.money += round(nft.price, 2)

        nft.user_id = buyer.id
        nft.username = buyer.username
        db.session.commit()
        flash("Successfully bought NFT.", "success")
        return redirect(url_for("home"))

    return redirect(url_for("home"))


# Allows users to modify NFT posting properties.
@app.route("/modify/<string:nft_id>", methods=["GET", "POST"])
@login_required
def modify(nft_id):
    user = current_user
    nft = UserNFT.query.get(nft_id)

    form = ModifyNFTForm()

    if form.validate_on_submit():
        if form.price.data:
            nft.price = form.price.data
        if form.title.data:
            nft.title = form.title.data
        if form.status.data != nft.status:
            nft.status = form.status.data

        db.session.commit()
        flash("NFT Successfully Updated.", "success")

        return redirect(url_for("home"))

    elif request.method == "GET":

        form.title.data = nft.title
        form.status.data = nft.status
        form.price.data = nft.price

    return render_template("modify.html", title="Modify your NFT", nft=nft, form=form)


# Allows users to upload a NFT to the site.
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    form = UploadForm()

    if form.validate_on_submit():

        picture_file = save_picture(form.picture.data, "NFT")
        nft = UserNFT(
            title=form.title.data,
            nft_image=picture_file,
            owner=current_user,
            username=current_user.username,
            status=form.status.data,
            price=form.price.data,
        )
        db.session.add(nft)
        db.session.commit()
        flash("NFT Successfully Uploaded.", "success")
        return redirect(url_for("home"))

    return render_template("upload.html", title="Upload a NFT", form=form)


# Helper function to save pictures to the database.
def save_picture(form_picture, type):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if type == "profile":
        picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    else:
        picture_path = os.path.join(app.root_path, "static/nfts", picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
