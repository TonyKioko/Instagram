from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^profile/',views.new_profile, name='profile'),
    url(r'^upload/$',views.new_image,name='add_photo'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),




]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
