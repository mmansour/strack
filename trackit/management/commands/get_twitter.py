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
            time.sleep(1)
            twitterdb = Youtuber.objects.get(title=user.title)
            try:
                twiturl = user.twitter_url
                twitcleanurl = twiturl.replace('www.','').replace('#!/','')

                if twitcleanurl[:4] != 'http':
                    twitcleanurl = 'http://{0}'.format(twitcleanurl)

                twitpage=urllib2.urlopen(twitcleanurl)
                twitsoup=BeautifulSoup(twitpage.read())
                twitsocialdata=twitsoup.findAll('a',{'data-nav':'followers'})
    #                print k, twitsociallink[0].findAll(text=True)[1], twitsociallink[0].findAll(text=True)[2]
                twitfollowers = [f.findAll(text=True) for f in twitsocialdata]
                twitsorteddata = sorted(twitfollowers)
                twitterdb.twitter_followers = twitsorteddata[0][1]
                twitterdb.save()

                print 'User: {0}, Followers: {1} Url: {2}'.format(user.title, twitsorteddata[0][1], twitcleanurl)
            except IndexError, e:
                twitterdb.twitter_error = 'Missing Followers: {0}'.format(e)
                twitterdb.save()
                print 'User: {0}, Missing Followers: {1}'.format(user.title, e)
            except urllib2.HTTPError, e:
                twitterdb.twitter_error = 'FB Page not found: {0}'.format(e)
                twitterdb.save()
                print 'User: {0}, FB Page not found: {1}'.format(user.title, e)
            except urllib2.URLError, e:
                twitterdb.twitter_error = 'URL Error: {0}'.format(e)
                twitterdb.save()
                print 'User: {0}, URL Error: {1}'.format(user.title, e)
            except UnicodeEncodeError, e:
                twitterdb.twitter_error = 'Weird characters in url: {0}'.format(e)
                twitterdb.save()
                print 'Weird characters in url: {0}'.format(e)
            except httplib.BadStatusLine, e:
                twitterdb.twitter_error = 'Bad status line: {0}'.format(e)
                twitterdb.save()
                print 'Bad status line: {0}'.format(e)

                
        print 'Done Pulling Twitter Followers'

