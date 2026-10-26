from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('', homee),
    path('h/',h1),
    path('about/',about),
    path('add/', add),
    path('student/', student_content),
    path('teacher/',Teachers),
    path('updateteacher/<int:id>/',Teacher_update),
    path('drf/',drf, name = 'drf'),
    path('get_studentdetails/',get_studentdetails, name = 'get_studentdetails'),
    path('post_data/',post_data, name = 'post_data'),
    path('api-token-auth/', obtain_auth_token),
    path('profile/',profile, name = 'profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',login, name = 'login'),
    path('StudentListView/', StudentListView.as_view(), name='student-list'),
    path('StudentListView1/<id>/', StudentListView1.as_view(), name='student-detail'),
    path('fastapi_student/',fastapi_students)
]