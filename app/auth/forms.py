from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
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

class UpdateProfileForm(FlaskForm):
    avatar = FileField('Profil Fotoğrafı', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yüklenebilir!')])
    password = PasswordField('Yeni Şifre (Değiştirmek istemiyorsanız boş bırakın)', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Yeni Şifreyi Onayla', validators=[EqualTo('password')])
    submit = SubmitField('Güncelle')
