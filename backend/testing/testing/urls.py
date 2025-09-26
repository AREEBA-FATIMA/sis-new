# """
# URL configuration for testing project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('students.urls')),
#     path('api/', include('teachers.urls')),   # ✅ notice trailing slash fix
#     path("api/", include("exams.urls")),
#     path("api/", include("classes.urls")),
#     path("api/", include("campus.urls")),
#     path("api/attendance/", include("attendance.urls")),
#     path("api/user/", include("user.urls")),    
# ]


# from django.contrib import admin
# from django.urls import path, include
# from graphene_django.views import GraphQLView
# from django.views.decorators.csrf import csrf_exempt

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("students.urls")),  # agar DRF bhi use ho raha hai
#     path("api/", include("campus.urls")),
#     path("api/", include("teachers.urls")),
#     path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),  # GraphQL
#     path("graphql/", GraphQLView.as_view(graphiql=True)),
#     path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),  # ✅ GraphQL endpoint
  
# ]
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# ✅ Import your schema
# from classes_section.schema import schema
# from students.schema import schema
# from teachers.schema import schema
# import campus.schema as campus_schema
# import classes_section.schema as classes_section_schema
from testing.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # API routes (DRF)
    path("api/", include("students.urls")),
    path("api/", include("campus.urls")),
    path("api/", include("teachers.urls")),
    path('api/classes/', include('classes.urls')),
    path('api/subjects/', include('subjects.urls')), 

    # GraphQL endpoint (CSRF exempt for testing)
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),]
