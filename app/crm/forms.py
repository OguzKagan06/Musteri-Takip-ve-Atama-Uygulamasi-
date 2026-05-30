from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional

class CustomerForm(FlaskForm):
    reference = StringField('Referans Kodu', validators=[Optional()])
    name = StringField('Ad', validators=[DataRequired()])
    surname = StringField('Soyad', validators=[DataRequired()])
    birth_date = DateField('Doğum Tarihi', validators=[Optional()])
    district = StringField('İlçe', validators=[Optional()])
    profession = StringField('Meslek', validators=[Optional()])
    phone = StringField('Telefon', validators=[Optional()])
    assigned_user_id = SelectField('Atanacak Arayıcı', coerce=int, validators=[Optional()])
    call_status = SelectField('Görüşme Durumu', choices=[
        ('Yeni Kayıt', 'Yeni Kayıt'), 
        ('Ulaşıldı', 'Ulaşıldı'), 
        ('Telefonu Açmadı', 'Telefonu Açmadı'), 
        ('Tekrar Aranacak', 'Tekrar Aranacak')
    ], validators=[DataRequired()], default='Yeni Kayıt')
    submit = SubmitField('Kaydet')

class NoteForm(FlaskForm):
    content = TextAreaField('Görüşme Notu', validators=[DataRequired()])
    submit = SubmitField('Not Ekle')
