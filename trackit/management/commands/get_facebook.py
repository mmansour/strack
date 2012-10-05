from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import time

class Command(BaseCommand):
    help = 'Get all facebook likes'
    def handle(self, *args, **options):

        yt = Youtuber.objects.exclude(facebook_url__isnull=True)\
            .exclude(facebook_url__exact='')\
            .exclude(facebook_error__isnull=False)

        for user in yt:
            time.sleep(1)
            if user.facebook_url[:4] != 'http':
                clean_url = 'http://{0}'.format(user.facebook_url)
            else:
                clean_url = user.facebook_url

            fburldb = Youtuber.objects.get(title=user.title)
            fbpage=urllib2.urlopen(clean_url)
            fbsoup=BeautifulSoup(fbpage.read())
            fbsociallink=fbsoup.findAll('meta',{'name':'description'})
            fbdigitlist = [s for s in fbsociallink[0]['content'].split()
                                if s.replace(",","").isdigit()]
#                        print k, fbdigitlist, fbsociallink[0]['content']
            fburldb.facebook_likes = fbdigitlist[0]
            fburldb.save()

            print 'User: {0}, Likes: {1} Url: {2}'.format(user.title, fbdigitlist[0], clean_url)
        print 'Done pulling Facebook Likes'


