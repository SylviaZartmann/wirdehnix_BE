from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls'))
    #path('filmography/', admin.site.urls),
    #path('authentication/', admin.site.urls),
] + staticfiles_urlpatterns()
