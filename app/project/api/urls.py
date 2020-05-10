from django.urls import path, re_path
from app.project.api.rest import ProjectList, ProjectDetail, ProjectPostBuild
from app.project.api.ws import output_compile_log

urlpatterns = [
    path('list.go', ProjectList.as_view()),  # GET
    path('create.go', ProjectList.as_view()),  # POST
    re_path('^(?P<pk>[0-9]+)/list.go$', ProjectDetail.as_view()),  # GET
    re_path('^(?P<pk>[0-9]+)/update.go$', ProjectDetail.as_view()),  # PUT
    re_path('^(?P<pk>[0-9]+)/delete.go$', ProjectDetail.as_view()),  # DELETE
    re_path('^(?P<pk>[0-9]+)/pre/build.go$', ProjectPostBuild.as_view()),  # DELETE
    re_path('^(?P<pk>[0-9]+)/post/build.go', output_compile_log)
]