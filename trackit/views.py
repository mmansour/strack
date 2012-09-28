from trackit.models import Youtuber
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
#from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect


def track_list(request):
    t_list = Youtuber.objects.filter(status=2).order_by('title')
    return render_to_response('tracklist.html',
                       {'t_list':t_list},
                        context_instance=RequestContext(request))






