from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random


class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

# profile 사진 업로드 경로 정하기
def profiles_image_path(instance, filename):
    return 'images/{}/profile_img/{}'.format(instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(
        max_length=50,
        blank=True,
        )
    profile_img = models.ImageField(
        default='images/icons/{}.png'.format(random.randrange(1, 20)),
        upload_to=profiles_image_path,
        )