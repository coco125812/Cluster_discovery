from django.urls import path
from . import views

urlpatterns = [
    path('getNodes/', views.get_nodes, name='get_nodes'),
    path('register/', views.register_node, name='register_node'),
    path('deregister/', views.deregister_node, name='deregister_node'),
    path('heartbeat/', views.heartbeat, name='heartbeat'),
    path('vote/', views.vote, name='vote'),
]
