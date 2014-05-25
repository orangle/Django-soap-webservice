from django.conf.urls import patterns, include, url

urlpatterns = patterns('webservice.views',
    (r'get_student_soap$', 'get_student_soap'),
)
