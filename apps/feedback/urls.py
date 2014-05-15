from django.conf.urls import *

from .views import *

urlpatterns = patterns('',

                       #url(r'^sent/$', FeedbackSent.as_view(), name='sent'),
                       url(r'^error/$', ErrorSend.as_view(), name='error_send'),
                       url(r'^send/$', Sended.as_view(), name='sent'),
                       url(r'^$', feedback_save, name='index'),
)