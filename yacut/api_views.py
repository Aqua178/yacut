import re
from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from .constants import PATTERN_LETTERS, PATTERN_LENGHT


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

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    long_url = data['url']

    if 'custom_id' not in data or data['custom_id'] is None:
        short_url = get_unique_short_id()
    else:
        short_url = data['custom_id']

        check_letters = re.search(PATTERN_LETTERS, short_url)
        check_length = re.search(PATTERN_LENGHT, short_url)
        if check_letters or check_length:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=short_url).count():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

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
