from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import csv
import re
import time
from urlparse import urlparse
import datetime

class Command(BaseCommand):
    help = 'Import local data to production'
    def handle(self, *args, **options):

#        reader = csv.reader(open('/users/mattmansour/django/sites/dev/socialtracker/docs/social-tracker-raw-data.csv', 'rU'), delimiter=',')
        reader = csv.reader(open('/home/mattym/webapps/socialtracker/docs/social-tracker-raw-data.csv', 'rU'), delimiter=',')
        #col[2] title user
        #col[3] slug
        #col[4] site id
        #col[5] desc
        #col[6] status
        #col[7] pubdate
        #col[11] youtube channel
        #col[12] facebook likes
        #col[13] facebook url
        #col[14] twitter follows
        #col[15] twitter url
        #col[16] facebook error
        #col[17] twitter error

        for col in reader:
            obj, created = Youtuber.objects.get_or_create(title=col[2],
                                                          slug=col[3],
                                                          site_id=col[4],
                                                          publish_date=datetime.datetime.now(),
                                                          youtube_channel=col[11],
                                                          facebook_likes=col[12],
                                                          facebook_url=col[13],
                                                          twitter_followers=col[14],
                                                          twitter_url=col[15],
                                                          facebook_error=col[16],
                                                          twitter_error=col[17]
            )

            print obj, created

        print 'Updated DB'






