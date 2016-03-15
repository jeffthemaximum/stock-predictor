from django.conf.urls import url
from news_check import views
from news_check.views import VibeView

urlpatterns = [
    url(
        r'^$',
        views.companies,
        name='company'
    ),
    url(
        r'^vibe/',
        VibeView.as_view(),
        name='vibe_list'
    ),
    url(
        r'^(?P<symbol>[-\w]+)/$',
        views.company_detail,
        name='detail'
    ),
    url(
        r'^update-vibe/(?P<symbol>[-\w]+)/$',
        views.update_vibe,
        name='update_vibe'
    ),
]
