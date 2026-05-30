from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class SendNotificationForm(FlaskForm):
    user_id = SelectField('Kime', coerce=str, validators=[DataRequired()])
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    submit = SubmitField('Bildirim Gönder')

class AdminDeleteUserForm(FlaskForm):
    admin_password = PasswordField('Admin Şifresi', validators=[DataRequired()])
    submit = SubmitField('Kullanıcıyı Kalıcı Olarak Sil')
