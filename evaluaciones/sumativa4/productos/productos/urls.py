from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from app.api import api 
from app.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('app.urls')),  
    path('api/', api.urls),  
    path('', lambda request: HttpResponseRedirect('login/')),
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),
]
