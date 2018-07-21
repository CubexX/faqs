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

>>> tweet = Tweet.objects.create(body='People are space puppets')

>>> tweet_model_type = ContentType.objects.get_for_model(tweet)
>>> Like.objects.create(content_type=tweet_model_type, object_id=tweet.id, user=user)
>>> Like.objects.count()
1
>>> Like.objects.first().content_object
<Tweet: People are space puppets>
>>> tweet.total_likes
1
