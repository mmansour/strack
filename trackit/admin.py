from trackit.models import Youtuber
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin


class YoutuberAdmin(DisplayableAdmin):

    fieldsets = [
        ("Title",                       {'fields': ['title']}),
        ("Youtube Channel",                       {'fields': ['youtube_channel']}),
        ("Published Date",              {'fields': ['publish_date']}),
        ("Published Status",            {'fields': ['status']}),
        ("Facebook Data",            {'fields': ['facebook_likes', 'facebook_url', 'facebook_error']}),
        ("Twitter Data",            {'fields': ['twitter_followers', 'twitter_url', 'twitter_error']}),
    ]

    list_display = ('title', 'status', 'publish_date', 'facebook_likes', 'facebook_url',
                    'facebook_error', 'twitter_followers', 'twitter_url', 'twitter_error')
    list_editable = ('status',)
    list_filter = ['status', 'publish_date','title','facebook_likes','facebook_url',
                   'twitter_followers', 'twitter_url','facebook_error','twitter_error']
    search_fields = ['title',]
    date_hierarchy = 'publish_date'

admin.site.register(Youtuber, YoutuberAdmin)

  