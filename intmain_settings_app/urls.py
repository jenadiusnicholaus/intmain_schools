
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("intmain_main_app.urls")),
    path("student-dashboard/", include("student_dashboard.urls")),
    path("user-authentication/", include("authentication.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
