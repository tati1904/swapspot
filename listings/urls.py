from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Items
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:pk>/', views.delete_item, name='delete_item'),

    # Exchange
    path('exchange/create/<int:sender_item_id>/<int:receiver_item_id>/', views.create_exchange, name='create_exchange'),
    path('exchange/accept/<int:exchange_id>/', views.accept_exchange, name='accept_exchange'),
    path('exchange/reject/<int:exchange_id>/', views.reject_exchange, name='reject_exchange'),
    path('exchange/<int:exchange_id>/', views.view_exchange, name='view_exchange'),
    path('exchange/<int:exchange_id>/send_message/', views.send_message, name='send_message'),
    path('exchange/<int:exchange_id>/review/', views.leave_review, name='leave_review'),

    # Reviews
    path('user/<int:user_id>/reviews/', views.view_reviews, name='view_reviews'),

    # Auth and Misc
    path('register/', views.register, name='register'),
    path('help/', views.help_contact, name='help_contact'),
]
