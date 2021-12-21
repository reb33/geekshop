import os
from datetime import datetime
from urllib.parse import urlunparse, urlencode, urlparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != "vk-oauth2":
        return
    api_url = urlunparse(
        (
            "http",
            "api.vk.com",
            "method/users.get",
            None,
            urlencode(
                {
                    "fields": ",".join(("bdate", "sex", "about", "photo_200_orig", "has_photo", "personal")),
                    "access_token": response["access_token"],
                    "v": 5.131,
                }
            ),
            None,
        )
    )

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    resp_body = resp.json()['response'][0]
    if resp_body['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif resp_body['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE

    if resp_body['about']:
        user.userprofile.about = resp_body['about']

    if resp_body['bdate']:
        age = timezone.now().year - datetime.strptime(resp_body['bdate'], '%d.%m.%Y').date().year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if resp_body.get('personal', {}).get('langs'):
        user.userprofile.languages = ','.join(resp_body['personal']['langs'])

    if resp_body['has_photo']:
        photo = requests.get(resp_body['photo_200_orig'])
        file_ext = urlparse(photo.url).path.rsplit('.', 1)[1]
        file_name = os.path.join(user.avatar.field.upload_to, f'{user.username}.{file_ext}')
        with open(
                os.path.join(
                    user.avatar.field.storage.location,
                    file_name
                ),
                'wb'
        ) as file:
            file.write(photo.content)
        user.avatar = file_name
    user.save()
