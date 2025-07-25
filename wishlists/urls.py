from django.urls import path
from .views import Wishlists, WishlistDetail, WishlistRooms, WishlistExperiences


urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>/", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>/", WishlistRooms.as_view()),
    path("<int:pk>/experiences/<int:experience_pk>/", WishlistExperiences.as_view()),
]
