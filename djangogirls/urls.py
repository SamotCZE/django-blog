from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'djangogirls.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', auth_views.login, name='user_login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='user_logout'),
    url(r'', include('blog.urls')),
]
