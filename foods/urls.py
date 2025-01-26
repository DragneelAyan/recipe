from django.urls import path, include
from foods import views

urlpatterns = [
    path('recipes/', views.recipeview, name='recipes'),
    path('deleterecipe/<int:id>/', views.deleterecipe, name='deleterecipe'),
    path('updaterecipe/<int:id>/', views.updaterecipe, name='updaterecipe'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutpage, name='logout'),
]
