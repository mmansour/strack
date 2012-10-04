from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2


class Command(BaseCommand):
    help = 'Get all Twitter Followers'
    def handle(self, *args, **options):

        yt = Youtuber.objects.exclude(twitter_url__isnull=True).exclude(twitter_url__exact='')

        for user in yt:
            twitterdb = Youtuber.objects.get(title=user.title)
            twiturl = user.twitter_url
            twitcleanurl = twiturl.replace('www.','').replace('#!/','')
            twitpage=urllib2.urlopen(str(twitcleanurl))
            twitsoup=BeautifulSoup(twitpage.read())
            twitsocialdata=twitsoup.findAll('a',{'data-nav':'followers'})
#               print k, twitsociallink[0].findAll(text=True)[1], twitsociallink[0].findAll(text=True)[2]
            twitfollowers = [f.findAll(text=True) for f in twitsocialdata]
            twitsorteddata = sorted(twitfollowers)
            twitterdb.twitter_followers = twitsorteddata[0][1]
            twitterdb.save()
            print 'User: {0}, Followers: {1} Url: {2}'.format(user.title, twitsorteddata[0][1], user.twitter_url)
        print 'Done Pulling Twitter Followers'

