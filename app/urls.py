from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^profile/',views.new_profile, name='profile'),
    url(r'^upload/$',views.new_image,name='add_photo'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^photo/like/(?P<id>\d+)', views.like_photo, name='likephoto'),
    url(r'^image_details/(?P<id>\d+)', views.image_details, name='imagedetails'),
    url(r'^searching/', views.search_results, name='searching'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profiles'),
    url(r'^user/(?P<user_id>\d+)', views.user_profile, name='userProfiles'),




]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
