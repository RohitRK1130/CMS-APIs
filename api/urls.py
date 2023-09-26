from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', include(router.urls)),
    path('get-auth-token/', GetAuthToken),
    path('create-users/',CreateUser),
    path('content-items/',ContentItems)
]

