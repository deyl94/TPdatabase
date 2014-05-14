# coding=utf-8
__author__ = 'deyl94'

from forumAPI.db import forumFunctions, postFunctions, threadFunctions
from django.http import HttpResponse
import json

def create(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            forum = forumFunctions.new_forum(name=content["name"],
                                             short_name=content["short_name"],
                                             user=content["user"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": forum}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def details(request):
    if request.method == "GET":
        get_params = request.GET.dict()
        related = request["related"]
        try:
            forum = forumFunctions.forum_details(short_name=get_params["forum"],
                                                 related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": forum}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_posts(request):
    if request.method == "GET":
        content = request.GET.dict()
        related = request["related"]
        optional = dict([(k, content[k]) for k in ["limit", "order", "since"] if k in content])
        try:
            posts = postFunctions.posts_list(entity="forum", params=optional, identifier=content["forum"],
                                       related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": posts}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_threads(request):
    if request.method == "GET":
        content = request.GET.dict()
        related = request["related"]
        optional = dict([(k, content[k]) for k in ["limit", "order", "since"] if k in content])
        try:
            threads = threadFunctions.threads_list(entity="forum", identifier=content["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": threads}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_users(request):
    if request.method == "GET":
        content = request.GET.dict()
        optional = dict([(k, content[k]) for k in ["limit", "order", "since_id"] if k in content])
        try:
            users = forumFunctions.list_users(content["forum"], optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": users}), content_type='application/json')
    else:
        return HttpResponse(status=400)