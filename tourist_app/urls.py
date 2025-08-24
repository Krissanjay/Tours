from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('create/',TourCreateView.as_view(),name='create'),
    path('detail/<int:pk>/',TourDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',TourUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',TourDelete.as_view(),name='delete'),
    path('search/<str:name>/',TourSearch.as_view(),name='search'),
    path('',views.index,name='index'),
    path('index/',views.tr,name='tr'),
    path('create_tour/',views.create,name='create_tour'),
    path('update_tour/<int:id>/',views.update,name='update_tour'),
    path('delete_tour/<int:id>/',views.delete,name='delete_tour'),
    path('detail_tour/<int:id>/',views.details,name='detail_tour'),

]