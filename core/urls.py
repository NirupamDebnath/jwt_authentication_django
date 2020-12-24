import debug_toolbar

from django.urls import include, path
from django.contrib import admin


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include(('authentication.urls',
                           "authentication"), namespace='authentication')),
    path('__debug__/', include(debug_toolbar.urls)),
]
