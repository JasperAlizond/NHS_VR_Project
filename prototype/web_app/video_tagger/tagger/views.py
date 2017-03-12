import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.views import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.forms import Form, ModelForm, HiddenInput
from django.core import serializers
from .models import Project, Video

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title"] 

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["title", "uploaded_video", "project"] 
        widgets = {"project": HiddenInput()}

@login_required
def project_list(request):
    return render(request,
                  "tagger/project_list.html",
                  {"projects": Project.objects.all()})


@login_required
def project_create(request):
    if request.method == "POST":
        f = ProjectForm(request.POST)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect("/tagger/project/")
    else:
        return render(request,
                "tagger/project_detail.html",
                {"project_form": ProjectForm()})

@login_required
def project_detail(request, project_id):
    if request.method == "POST":
        f = ProjectForm(request.POST, instance=get_object_or_404(Project, id=project_id))
        if f.is_valid():
            f.save()
        return HttpResponseRedirect("/tagger/project/")
    else:
        return render(request,
                "tagger/project_detail.html",
                {"project_form": ProjectForm(instance=get_object_or_404(Project, id=project_id))})

@login_required
def project_delete(request, project_id):
    if request.method != "POST":
        raise HttpResponseNotAllowed(self.permitted_methods)
    Project.objects.get(pk=project_id).delete()
    return HttpResponseRedirect("/tagger/project/")

@login_required
def project_export(request, project_id):
    pass


@login_required
def video_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    videos = project.video_set
    return render(request,
            "tagger/video_list.html",
            {
                "project": project,
                "videos": videos
            }
            )

@login_required
def video_create(request, project_id):
    f = VideoForm(initial={"project":project_id})
    if request.method == "POST":
        f = VideoForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect("/tagger/project/{}/video/".format(project_id))
        return render(request,
                "tagger/video_detail.html",
                {"video_form": f})
    else:
        return render(request,
                "tagger/video_detail.html",
                {"video_form": f})

@login_required
def video_editor(request, project_id, video_id):
    vid = get_object_or_404(Video, id=video_id)
    if request.method == "POST":
        pass
    return render(request, "tagger/video_editor.html", {"video": vid, "tags": vid.tag_set, "tags_json": serializers.serialize("json", vid.tag_set.all())})

@login_required
def video_delete(request, project_id, video_id):
    if request.method != "POST":
        raise HttpResponseNotAllowed(self.permitted_methods)
    Video.objects.get(pk=video_id).delete()
    return HttpResponseRedirect("/tagger/project/{}/video/".format(project_id))
