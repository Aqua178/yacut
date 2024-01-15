from datetime import datetime

from . import db
from .constants import ORIGINAL_URL_LENGTH, CUSTOM_LINK_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH), unique=True, nullable=False)
    short = db.Column(db.String(CUSTOM_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )
