from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:collection_id>/', views.collection, name='collection'),
    path('<int:collection_id>/learning/', views.learning, name='learning'),
    path('<int:collection_id>/<int:card_id>/', views.card, name='card'),
    path('make_card/', views.card_creation, name="card_creation"),
    path('expired_cards/', views.show_expired, name='show_expired'),
    re_path(r'learn_expired/(?P<index>[\w-]+)', views.learn_expired, name='learn_expired'),
    path('make_collection/', views.collection_creation, name="collection_creation")
]
