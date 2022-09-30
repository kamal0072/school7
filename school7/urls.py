
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:group_name>/',views.index,name='index'),
    path("test/msgfromview/",views.msgfromview,name='msg-from-view'),
]
