# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('',views.home,name="home"),
#     path('login/',views.login,name='login'),
#     path('signup/',views.signup,name='signup'),
#     path('logout/',views.logout,name='logout'),
# ]



from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('about/',views.about,name='about'),
    path('workflow/',views.workflow,name='workflow'),
    # path('skindisorders/',views.skindisorders,name='skindisorders'),
    path('skindisorders/',views.skindisorders,name='skindisorders'),
    path('diagnosis/',views.diagnosis,name='diagnosis'),
    #  path('home/',views.home,name='home'),
]
