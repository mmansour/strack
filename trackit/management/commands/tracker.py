from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import csv
import re
import time
from urlparse import urlparse

class Command(BaseCommand):
    help = 'Reads CSV list of youtube channels and gets Facebook Likes and Twitter Followers'
    def handle(self, *args, **options):

#        reader = csv.reader(open('/users/mattmansour/django/sites/dev/socialtracker/docs/allchannels_s.csv', 'rU'), delimiter=',')
        ytsocialrequestdict = {}
        ytsocialkeywords = ['facebook', 'twitter']
        ytexactMatch = re.compile(r'\b%s\b' % '\\b|\\b'.join(ytsocialkeywords), flags=re.IGNORECASE)

        fblikeslist = []
        twitterfollowerslist = []
        socialmissingurllist = []

#        for col in reader:
#            time.sleep(1)
#            ####################################################
#            # HIT YouTube. FIND SOCIAL LINKS. ADD CHANNEL NAME AND SOCIAL LINKS TO DB and DICTIONARY
#            try:
#                yturl=col[2]
#                ytpage=urllib2.urlopen(yturl)
#                ytsoup=BeautifulSoup(ytpage.read())
#                ytsociallinks=ytsoup.findAll('a',{'class':'yt-uix-redirect-link'})
#                ytsocialrequestdict[col[1]] = [s['href'] for s in ytsociallinks if ytexactMatch.findall(s['href'])]
#                obj, created = Youtuber.objects.get_or_create(title=col[1], youtube_channel=col[2],)
#                print 'Created user: {0} {1}'.format(obj, created)
#            except Exception, e:
#                obj, created = Youtuber.objects.get_or_create(title="Bad_YouTube_Channel: {0}".format(col[1]), youtube_channel=col[2], status=1)
#                print 'Error, {0} {1}'.format(col[2], e)

        ytchannel = Youtuber.objects.filter(status=2)
        for yt in ytchannel:
            time.sleep(1)
            ####################################################
            # HIT YouTube. FIND SOCIAL LINKS. ADD CHANNEL NAME AND SOCIAL LINKS TO DB and DICTIONARY
            try:
                ytpage=urllib2.urlopen(yt.youtube_channel)
                ytsoup=BeautifulSoup(ytpage.read())
                ytsociallinks=ytsoup.findAll('a',{'class':'yt-uix-redirect-link'})
                ytsocialrequestdict[yt.title] = [s['href'] for s in ytsociallinks if ytexactMatch.findall(s['href'])]
                print 'Request for user: {0}'.format(yt.title)
            except Exception, e:
                print 'Yt Request Error, {0}'.format(e)

        for k, v in ytsocialrequestdict.iteritems():

            #ADD Missing Socials For Each Channel to List
            for sl in ytsocialkeywords:
                if sl not in ytexactMatch.findall(' '.join(v)):
                    socialmissingurllist.append([k, 'Missing Link:', sl])

            for l in v:
                time.sleep(1)
                url = urlparse(l)
                if url.netloc == 'www.facebook.com' or url.netloc == 'facebook.com':
                    fburldb = Youtuber.objects.get(title=k)
                    fburl = ""
                    try:
                        fburl = l
                        fbpage=urllib2.urlopen(fburl)
                        fbsoup=BeautifulSoup(fbpage.read())
                        fbsociallink=fbsoup.findAll('meta',{'name':'description'})
                        fbdigitlist = [s for s in fbsociallink[0]['content'].split()
                                            if s.replace(",","").isdigit()]
#                        print k, fbdigitlist, fbsociallink[0]['content']
                        fblikeslist.append([k, fbdigitlist[0], fburl])
                        fburldb.facebook_likes = fbdigitlist[0]
                        fburldb.facebook_url = fburl
                    except Exception, e:
                        fburldb.facebook_error = fburl
#                        print 'Facebook Error: {0} {1} {2}'.format(k, l, e)
                    finally:
                        fburldb.save()

                if url.netloc == 'twitter.com' or url.netloc == 'www.twitter.com':
                    # DO THIS UP ON TWITTER
                    twitterdb = Youtuber.objects.get(title=k)
                    twitcleanurl = ""
                    try:
                        twiturl = l
                        twitcleanurl = twiturl.replace('www.','').replace('#!/','')
                        twitpage=urllib2.urlopen(twitcleanurl)
                        twitsoup=BeautifulSoup(twitpage.read())
                        twitsocialdata=twitsoup.findAll('a',{'data-nav':'followers'})
        #               print k, twitsociallink[0].findAll(text=True)[1], twitsociallink[0].findAll(text=True)[2]
                        twitfollowers = [f.findAll(text=True) for f in twitsocialdata]
                        twitsorteddata = sorted(twitfollowers)
                        twitterfollowerslist.append([k, twitsorteddata[0][1], twitcleanurl])
                        twitterdb.twitter_url = twitcleanurl
                        twitterdb.twitter_followers = twitsorteddata[0][1]

                    except Exception, e:
#                        print 'Twitter Request Error: {0} {1} {2}'.format(k, twitcleanurl, e)
                        twitterdb.twitter_error = twitcleanurl
                    finally:
                        twitterdb.save()

