from django.urls import path, include

app_name = "general"

urlpatterns = [
    
    path("api/v1/", include("general.api.v1.urls")),
]
