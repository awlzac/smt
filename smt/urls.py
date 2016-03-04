
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    # any url -> addrmap
    url(r'', include('addrmap.urls', namespace="addrmap")),
]
