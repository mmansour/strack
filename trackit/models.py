from django.db import models
from mezzanine.core.models import Displayable


class Youtuber(Displayable):
    youtube_name = models.CharField(max_length=100, verbose_name="Youtube Name", blank=True, null=True)
    youtube_channel = models.CharField(max_length=400, verbose_name="Youtube Channel", blank=True, null=True)
    facebook_likes = models.CharField(max_length=20, blank=True, null=True, verbose_name="Facebook Likes")
    facebook_url = models.CharField(max_length=400, blank=True, null=True, verbose_name="Facebook url")
    twitter_followers = models.CharField(max_length=20, blank=True, null=True, verbose_name="Twitter Followers")
    twitter_url = models.CharField(max_length=400, blank=True, null=True, verbose_name="Twitter Url")
    facebook_error = models.CharField(max_length=400, blank=True,null=True, verbose_name="Facebook Error")
    twitter_error = models.CharField(max_length=400, blank=True,null=True, verbose_name="Twitter Error")

#    @models.permalink
#    def get_absolute_url(self):
#        return ('ghhwhatis.views.what_is', [self.slug,])

    def __unicode__(self):
        return self.title

