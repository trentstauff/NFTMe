from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    FloatField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from NFTMe.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    money = FloatField(
        "Starting Balance (example: 10000, not $10,000)",
        validators=[
            NumberRange(
                min=0,
                max=500000000,
                message="(Starting balance must be less than $500,000,000.)",
            )
        ],
    )

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    money = FloatField(
        "Balance",
        validators=[
            NumberRange(
                min=0,
                max=1000000000,
                message="(Balance must be less than $1,000,000,000. Enter without $ sign or commas.)",
            )
        ],
    )

    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class UploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    picture = FileField(
        "Upload NFT", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    status = BooleanField("For Sale")
    price = FloatField(
        "Price",
        validators=[
            NumberRange(
                min=0, max=100000000, message="(Price must be less than $100,000,000.)"
            )
        ],
    )
    submit = SubmitField("Upload")


class ModifyNFTForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            Length(min=2, max=100, message="(Must be less than 20 characters.)")
        ],
    )
    price = FloatField(
        "Price",
        validators=[
            NumberRange(
                min=0,
                max=100000000,
                message="(Must be less than $100,000,000. Enter without $ sign or commas.)",
            )
        ],
    )
    status = BooleanField("For Sale")
    submit = SubmitField("Update")
