# dans urls.py
from django.urls import path, include
from .views import WilayaView, Type_SangSetview, hell, DonateurSetview,LoginView,LoginAdminView,RegisterAdminView,DonateurUpdateView,AdiminView
from .views import RegisterView,UserView,LogoutView,ListeDonateur,RefreshView,CountDonateur,UpdateDonateurStatus,updatedonateurtest,donateuradminview


urlpatterns = [
    
    path('he/',hell),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('refresh/',RefreshView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('liste/',ListeDonateur.as_view()),
    path('loginadmin/',LoginAdminView.as_view()),
    path('registeradmin/',RegisterAdminView.as_view()),
    path('donateurs/<int:pk>/update/', DonateurUpdateView.as_view()),
    path('don/',AdiminView.as_view()),
    path('don/<int:id>/', AdiminView.as_view()),
    path('donateur/<int:id>/', DonateurSetview.as_view()),
    path('wilaya/',WilayaView.as_view()),
    path('sang/',Type_SangSetview.as_view()),
    path('sang/<str:nom>/', Type_SangSetview.as_view()),
    path('count/',CountDonateur.as_view()),
    path('upd/',UpdateDonateurStatus.as_view()),
    path('test/',updatedonateurtest.as_view()),
    path('don/a_fait/',donateuradminview.as_view())
]
