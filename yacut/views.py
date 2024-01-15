import random
import string
from urllib.parse import urljoin

from flask import Markup, flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    random_url = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=6))
    return random_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    url_map = URLMap()
    if form.validate_on_submit():
        original = form.original_link.data
        short_name = form.custom_id.data
        if not short_name:
            short_name = get_unique_short_id()

        """Проверка на наличие короткой ссылки в БД"""
        if URLMap.query.filter_by(short=short_name).count():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)

        """Проверка на наличие длинной ссылки в БД"""
        if URLMap.query.filter_by(original=original).count():
            flash('Предложенный вариант длинной ссылки уже существует.')
            return render_template('yacut.html', form=form)

        url_map = URLMap(
            original=original,
            short=short_name
        )
        db.session.add(url_map)
        db.session.commit()
        absolute = request.url_root
        base_url = urljoin(absolute, short_name)
        flash(Markup(f'Ваша новая ссылка готова: <a href="{base_url}">{base_url}</a>'))
    return render_template('yacut.html', form=form, id=url_map.id)


@app.route('/<short_id>', methods=['GET'])
def url(short_id):
    model_url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(model_url.original)
