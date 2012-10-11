from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import time

class Command(BaseCommand):
    help = 'Get all facebook likes'
    def handle(self, *args, **options):

        yt = Youtuber.objects.exclude(facebook_url__isnull=True).exclude(facebook_url__exact='')
        clean_url = ""
        
#        for user in yt:
############ TEST URL CLEAN UP
#            fburldb = Youtuber.objects.get(title=user.title)
#
#            if user.facebook_url[:4] != 'http':
#                clean_url = 'http://{0}'.format(user.facebook_url)
#            elif user.facebook_url[:5] == 'https':
#                clean_url = user.facebook_url.replace('https','http')
#            elif user.facebook_url[:11] == 'http://face':
#                clean_url = user.facebook_url.replace('http://face','http://www.face')
#            else:
#                clean_url = user.facebook_url
#
#            print clean_url.lower()

        for user in yt:
############ THIS WORKS BUT CLEAN UP URLS
            time.sleep(1)
            fburldb = Youtuber.objects.get(title=user.title)
            try:
#                if user.facebook_url[:4] != 'http':
#                    clean_url = 'http://{0}'.format(user.facebook_url)
#                else:
#                    clean_url = user.facebook_url
                if user.facebook_url[:4] != 'http':
                    clean_url = 'http://{0}'.format(user.facebook_url)
                elif user.facebook_url[:5] == 'https':
                    clean_url = user.facebook_url.replace('https','http')
                elif user.facebook_url[:11] == 'http://face':
                    clean_url = user.facebook_url.replace('http://face','http://www.face')
                else:
                    clean_url = user.facebook_url

                sanitized_url = clean_url.lower()

                print 'Clean fb url %s' % sanitized_url

                fbpage=urllib2.urlopen(sanitized_url)
                fbsoup=BeautifulSoup(fbpage.read())
                fbsociallink=fbsoup.findAll('meta',{'name':'description'})
                fbdigitlist = [s for s in fbsociallink[0]['content'].split()
                                    if s.replace(",","").isdigit()]
    #                        print k, fbdigitlist, fbsociallink[0]['content']
                fburldb.facebook_likes = fbdigitlist[0]
                fburldb.facebook_url = sanitized_url
                fburldb.save()
                print 'User: {0}, Likes: {1} Url: {2}'.format(user.title, fbdigitlist[0], sanitized_url)
            except IndexError, e:
                fburldb.facebook_error = 'Missing Likes: {0}'.format(e)
                fburldb.save()
                print 'User: {0}, Missing Likes: {1}'.format(user.title, e)
            except urllib2.HTTPError, e:
                fburldb.facebook_error = 'FB Page not found: {0}'.format(e)
                fburldb.save()
                print 'User: {0}, FB Page not found: {1}'.format(user.title, e)
            except urllib2.URLError, e:
                fburldb.facebook_error = 'URL Error: {0}'.format(e)
                fburldb.save()
                print 'User: {0}, URL Error: {1}'.format(user.title, e)
            except UnicodeEncodeError, e:
                fburldb.facebook_error = 'Weird characters in url: {0}'.format(e)
                fburldb.save()
                print 'Weird characters in url: {0}'.format(e)

        print 'Done pulling Facebook Likes'


