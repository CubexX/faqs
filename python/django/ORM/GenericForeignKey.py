from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


###################################################################


from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from likes.models import Like


class Tweet(models.Model):
    body = models.CharField(max_length=140)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.body

    @property
    def total_likes(self):
        return self.likes.count()


###################################################################


from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like

User = get_user_model()


def add_like(obj, user):
    """Лайкает `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    """Удаляет лайк с `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)


###################################################################


>>> tweet = Tweet.objects.create(body='People are space puppets')

>>> tweet_model_type = ContentType.objects.get_for_model(tweet)
>>> Like.objects.create(content_type=tweet_model_type, object_id=tweet.id, user=user)
>>> Like.objects.count()
1
>>> Like.objects.first().content_object
<Tweet: People are space puppets>
>>> tweet.total_likes
1
