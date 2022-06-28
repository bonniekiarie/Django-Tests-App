from django.urls import path
from .views import home_view, score_view, signup

urlpatterns = [
    path('', home_view, name='home'),
    path('score/', score_view, name = "score"),
     path('signup/', signup, name = "signup"),
]
