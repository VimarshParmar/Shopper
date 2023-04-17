from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Shopper Admin"
admin.site.site_title = "Shopper Admin Panel"
admin.site.index_title = "Welcome to Shopper Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
]
