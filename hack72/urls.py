from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView, home_view, DiscussionPage

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('', home_view, name='home'),
    path('students/', include('students.urls')),
    path('parents/', include('parent.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('discussion/',DiscussionPage.as_view(), name='discussion_page')
]


urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
