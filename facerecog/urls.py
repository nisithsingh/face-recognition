from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'facerecog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webcamrecog.views.home'),
    url(r'^home/$', 'webcamrecog.views.home'),
    url(r'^train/$', 'webcamrecog.views.train'),
    url(r'^save/$', 'webcamrecog.views.save'),
    url(r'^compare/$', 'webcamrecog.views.compare'),
    url(r'^recog/$', 'webcamrecog.views.recog'),    
    # url(r'^convert/$', 'webcamrecog.views.convertFullImgToTrainImage'),
)
