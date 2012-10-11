from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import time
import httplib


class Command(BaseCommand):
    help = 'Get all Twitter Followers'
    def handle(self, *args, **options):

        yt = Youtuber.objects.exclude(twitter_url__isnull=True).exclude(twitter_url__exact='')

        for user in yt:
            twitterdb = Youtuber.objects.get(title=user.title)
            try:
                clean_url = user.twitter_url.replace('www.','').replace('#!/','')
                if user.twitter_url[:4] != 'http':
                    clean_url = 'http://{0}'.format(user.twitter_url)
                if user.twitter_url[:5] == 'https':
                    clean_url = user.twitter_url.replace('https','http')
                twitterdb.twitter_url = clean_url.lower()
                print 'Clean twitter url %s' % clean_url.lower()
            except UnicodeEncodeError, e:
                print 'Unicode error sanitizing URL'
            finally:
                twitterdb.save()
        print 'Done Pulling Twitter Followers'

  