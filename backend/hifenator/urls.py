from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hfntr/', include('hfntr.urls', namespace='hfntr'))
]
