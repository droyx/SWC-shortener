from rest_framework import routers
from .views import ShortenerView

router = routers.SimpleRouter()
router.register(r"short", ShortenerView, basename="shorten")

urlpatterns = router.urls
