from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from trackit.models import Youtuber
import urllib2
import csv
import re
import time
from urlparse import urlparse

class Command(BaseCommand):
    help = 'Import local data to production'
    def handle(self, *args, **options):

        reader = csv.reader(open('/users/mattmansour/django/sites/dev/socialtracker/docs/allchannels_s.csv', 'rU'), delimiter=',')




