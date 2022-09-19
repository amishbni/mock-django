from django.contrib import admin
from django.urls import path
from app.views import time_now

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', time_now),
]
