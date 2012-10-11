from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import time

class Command(BaseCommand):
    help = 'Clean up facebook urls'
    def handle(self, *args, **options):

        yt = Youtuber.objects.exclude(facebook_url__isnull=True).exclude(facebook_url__exact='')

        for user in yt:
            fburldb = Youtuber.objects.get(title=user.title)
            clean_url = user.facebook_url

            if user.facebook_url[:4] != 'http':
                clean_url = 'http://{0}'.format(user.facebook_url)
            if user.facebook_url[:5] == 'https':
                clean_url = user.facebook_url.replace('https','http')
            if user.facebook_url[:11] == 'http://face':
                clean_url = user.facebook_url.replace('http://face','http://www.face')

            try:
                fburldb.facebook_url = clean_url.lower()
                print 'Clean fb url %s' % clean_url.lower()
            except Exception, e:
                print 'Error sanitizing URL'
            finally:
                fburldb.save()

        print 'Done cleaning Facebook URLS'


  