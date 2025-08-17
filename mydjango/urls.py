from django.contrib import admin
from django.urls import path, include
from django.conf import settings           # ✅ required
from django.conf.urls.static import static
from shop import views as shop_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('login/', shop_views.login_view, name='login'),  # global 'login'

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)