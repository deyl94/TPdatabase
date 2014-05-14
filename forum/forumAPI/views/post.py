__author__ = 'deyl94'

import json
from django.http import HttpResponse
from forumAPI.db import postFunctions

def create(request):
    if request.method == "POST":
        content = json.loads(request.body)
        optional = dict([(k, content[k]) for k in ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"] if k in content])
        try:
            post = postFunctions.new_post(date=content["date"], thread=content["thread"],
                                message=content["message"], user=content["user"],
                                forum=content["forum"], optional=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def details(request):
    if request.method == "GET":
        content = request.GET.dict()
        related = request["related"]
        try:
            post = postFunctions.details(content["post"], related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def post_list(request):
    if request.method == "GET":
        content = request.GET.dict()
        try:
            identifier = content["forum"]
            entity = "forum"
        except KeyError:
            try:
                identifier = content["thread"]
                entity = "thread"
            except Exception as e:
                return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')

        optional = dict([(k, content[k]) for k in ["limit", "order", "since"] if k in content])
        try:
            p_list = postFunctions.posts_list(entity=entity, params=optional, identifier=identifier, related=[])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": p_list}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def remove(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            post = postFunctions.hide(post_id=content["post"], status=1)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def restore(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            post = postFunctions.hide(post_id=content["post"], status=0)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def update(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            post = postFunctions.update(update_id=content["post"], message=content["message"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def vote(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            post = postFunctions.vote(vote_id=content["post"], vote_type=content["vote"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": post}), content_type='application/json')
    else:
        return HttpResponse(status=400)