from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^pdfEdit', hello.views.pdfEdit, name='pdfEdit'),
    url(r'^signatureCapture', hello.views.signatureCapture, name='signatureCapture'),
    url(r'^app/hello/static/images/pdfs/\w{2,40}', hello.views.pdfServe, name='pdfServe'),
    path('admin/', admin.site.urls),
]
