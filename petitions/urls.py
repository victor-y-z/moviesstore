from django.urls import path
from . import views

app_name = 'petitions'

urlpatterns = [
    path('', views.petition_list, name='list'),
    path('create/', views.create_petition, name='create'),
    path('<int:petition_id>/', views.petition_detail, name='detail'),
    path('<int:petition_id>/vote/', views.vote_petition, name='vote'),
    path('<int:petition_id>/delete-vote/', views.delete_vote, name='delete_vote'),
]
