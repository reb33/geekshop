from string import digits

from django.core.exceptions import ValidationError


def check_name(data):
    if len(data) < 1:
        raise ValidationError("Имя обязательное поле")
    if data[0] in digits:
        raise ValidationError("Имя не может начинаться с цифры")
    if data.isdigit():
        raise ValidationError("Имя не может состаять из цифр")


def check_size_file(data):
    if data.size > 20 * 1024 * 1024:
        raise ValidationError("Размер фотографии не должен превышать 20 mb")
