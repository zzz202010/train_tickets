from django.urls import path
from Train import views

app_name = 'Train'
urlpatterns = [
    path('border/', views.book_order, name='book_order'),
    path('border1/', views.book_order1, name='book_order1'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('change/', views.change_password, name='change_password'),
    path('train/', views.search_train, name='search_train'),
    path('train1/', views.search_train1, name='search_train1'),
    path('corder/', views.check_order, name='check_order'),
    path('xorder/', views.change_order, name='change_order'),
    path('xorder1/', views.change_order1, name='change_order1'),
    path('xorder2/', views.change_order2, name='change_order2'),
    path('torder/', views.cancel_order, name='cancel_order'),
    path('problem/', views.problems, name='problems'),
    # path('forget/', views.forget_password, name='forget_password'),
]

