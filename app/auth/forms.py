from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User
from app import db

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane seçin.')

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')
