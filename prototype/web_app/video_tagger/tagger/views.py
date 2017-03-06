from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.views import login_required
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.forms import Form
from .models import Project

@login_required
def project_list(request):
    return render(request,
                  "tagger/project_list.html",
                  {"projects": Project.objects.all()})


class ProjectCreateForm(Form):
    pass

@login_required
def project_create(request):
    pass

@login_required
def project_detail(request):
    detail

@login_required
def project_delete(request, project_id):
    if request.method != "POST":
        raise HttpResponseNotAllowed()
    Project.objects.get(pk=id).delete()
    return HttpResponseRedirect("/tagger/project/")

@login_required
def project_export(request):
    pass


@login_required
def video_list(request):
    pass

@login_required
def video_create(request):
    pass

@login_required
def video_editor(request):
    pass

@login_required
def video_delete(request):
    pass
