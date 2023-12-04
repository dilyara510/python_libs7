from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
=======
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> 52cbfbd74f821ccddb3502551a7f68197e596d39

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
<<<<<<< HEAD
]
=======
    path('api/', include('base.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 52cbfbd74f821ccddb3502551a7f68197e596d39
