from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SendNotificationForm(FlaskForm):
    user_id = SelectField('Kime', coerce=int, validators=[DataRequired()])
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    submit = SubmitField('Bildirim Gönder')
