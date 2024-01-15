import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка', validators=[
            DataRequired(message='Обязательное поле'),
            URL(),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Regexp(re.compile(r'^[a-zA-Z0-9]{1,16}$')), Optional(),
        ]
    )
    submit = SubmitField('Создать')
