import re
from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    url_map = URLMap()
    data = request.get_json()

    """Проверка на наличие тела запроса"""
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    """Проверка на наличие ключа url"""
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    long_url = data['url']

    """Проверка на наличие ключа custom_id"""
    if 'custom_id' not in data or data['custom_id'] is None:
        short_url = get_unique_short_id()
    else:
        short_url = data['custom_id']

        """Проверка короткой ссылки на содержание недопустимых символов и
        на превышение лимита по кол-ву символов"""
        check_letters = re.search(r'[а-яА-ЯеёЁ\W]', short_url)
        check_length = re.search(r'^\w{17,}', short_url)
        if check_letters or check_length:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    """Проверка наличия короткой ссылки в БД"""
    if URLMap.query.filter_by(short=short_url).count():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    """Проверка наличия короткой ссылки в БД"""
    if URLMap.query.filter_by(original=long_url).count():
        raise InvalidAPIUsage('Предложенный вариант длинной ссылки уже существует.')

    url_map = URLMap(
        original=long_url,
        short=short_url
    )
    db.session.add(url_map)
    db.session.commit()
    absolute = request.url_root
    base_url = urljoin(absolute, short_url)
    return jsonify({'url': url_map.original, 'short_link': base_url}), HTTPStatus.CREATED
