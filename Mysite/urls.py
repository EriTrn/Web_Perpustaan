from django.conf import settings
from antarmuka.views import DetailAntarmuka, index, AddPost, UpdatePost, DeletePost, SearchAntarmuka
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from antarmuka import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('detail/<int:pk>', views.DetailAntarmuka.as_view(), name='detail'),
    # Add post
    path('add/', views.AddPost.as_view(), name='add'),
    path('<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('search/', SearchAntarmuka.as_view(), name='search'),
    path('contact/', views.contact_us, name='contact_us'),
    path('accounts/', include('allauth.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)