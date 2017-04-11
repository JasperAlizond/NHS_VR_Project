import json
import io
import zipfile
import string
import os

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.contrib.auth.views import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.forms import Form, ModelForm, HiddenInput
from django.core import serializers
from .models import Project, Video, Tag


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
    project = get_object_or_404(Project, id=project_id)
    s = io.BytesIO()
    zf = zipfile.PyZipFile(s, "w")
    videos = [(video, video.tag_set) for video in project.video_set.all()]
    meta_str = render_to_string("tagger/meta.xml", {
        "project": project,
        "videos": videos
        })
    zf.writestr("project/meta/meta.xml", str(meta_str))
    for video, tags in videos:
        zf.write(video.uploaded_video.path, arcname="project/"+video.uploaded_video.name)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = "attachment; filename={}.zip".format("".join([c.lower() for c in project.title if c in string.ascii_letters]))
    return response


        
    


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
        print(request.body)
        data = [item for item in json.loads(request.body) if "deleted" not in item]
        for item in json.loads(request.body):
            if item not in data:
                Tag.objects.filter(id=item["pk"]).delete();
        for obj in serializers.deserialize("json", json.dumps(data)):
            obj.save()
    return render(request, "tagger/video_editor.html", {"video": vid, "tags": vid.tag_set, "tags_json": serializers.serialize("json", vid.tag_set.all())})


@login_required
def video_delete(request, project_id, video_id):
    if request.method != "POST":
        raise HttpResponseNotAllowed(self.permitted_methods)
    Video.objects.get(pk=video_id).delete()
    return HttpResponseRedirect("/tagger/project/{}/video/".format(project_id))
