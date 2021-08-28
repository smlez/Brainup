from django.urls import path
from . import views

app_name = "brainup_api"
urlpatterns = [
    path('', views.api_root, name="root"),
    path('collections/', views.CollectionsList.as_view(), name="collections_list"),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name="collection_details"),
    path('cards/', views.CardsList.as_view(), name="cards_list"),
    path('cards/<int:pk>', views.CardDetail.as_view(), name="card_details"),
    path('cards/edit', views.CardsListEdit.as_view(), name='cards_list_edit')
]
