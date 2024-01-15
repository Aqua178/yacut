import string

ORIGINAL_URL_LENGTH = 512
CUSTOM_LINK_LENGTH = 16
URL_LENGTH = 6
SYMBOLS = string.ascii_uppercase + string.digits + string.ascii_lowercase
PATTERN_LETTERS = r'[а-яА-ЯеёЁ\W]'
PATTERN_LENGHT = r'^\w{17,}'
