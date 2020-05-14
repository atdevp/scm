from django.urls import path, re_path
from app.project.api.rest import ProjectList, ProjectDetail, ProjectPostBuildAPI
from app.project.api.rest import ProjectPostGetCompileCommandAPI
from app.project.api.ws import output_compile_log

urlpatterns = [
    path('list.go', ProjectList.as_view()),
    path('create.go', ProjectList.as_view()),
    re_path('^(?P<pk>[0-9]+)/list.go$', ProjectDetail.as_view()),
    re_path('^(?P<pk>[0-9]+)/update.go$', ProjectDetail.as_view()),
    re_path('^(?P<pk>[0-9]+)/delete.go$', ProjectDetail.as_view()), 
    re_path('^(?P<pk>[0-9]+)/pre/build.go$', ProjectPostBuildAPI.as_view()),
    re_path('^(?P<pk>[0-9]+)/post/getCompileCommand.go', ProjectPostGetCompileCommandAPI.as_view()),
    re_path('post/build.go', output_compile_log)
]