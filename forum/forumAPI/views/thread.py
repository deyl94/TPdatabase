__author__ = 'deyl94'

import json
from django.http import HttpResponse
from forumAPI.db import threadFunctions, postFunctions


def close(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.trigger(id=content["thread"], isClosed=1)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def create(request):
    if request.method == "POST":
        content = json.loads(request.body)
        optional = dict([(k, content[k]) for k in ["isDeleted"] if k in content])
        try:
            thread = threadFunctions.new_thread(forum=content["forum"], title=content["title"],
                                         isClosed=content["isClosed"],
                                         user=content["user"], date=content["date"],
                                         message=content["message"],
                                         slug=content["slug"], optional=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def details(request):
    if request.method == "GET":
        content = request.GET.dict()
        related = request["related"]
        try:
            thread = threadFunctions.details(id=content["thread"], related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)

def thread_list(request):
    if request.method == "GET":
        content = request.GET.dict()
        try:
            identifier = content["forum"]
            entity = "forum"
        except KeyError:
            try:
                identifier = content["user"]
                entity = "user"
            except KeyError:
                return HttpResponse(json.dumps({"code": 1, "response": "Any methods?"}),
                                    content_type='application/json')
        optional = dict([(k, content[k]) for k in ["limit", "order", "since"] if k in content])
        try:
            t_list = threadFunctions.threads_list(entity=entity, identifier=identifier, related=[], params=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": t_list}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_posts(request):
    if request.method == "GET":
        content = request.GET.dict()
        entity = "thread"
        optional = dict([(k, content[k]) for k in ["limit", "order", "since"] if k in content])
        try:
            p_list = postFunctions.posts_list(entity=entity, params=optional, identifier=content["thread"], related=[])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": p_list}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def open(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.trigger(id=content["thread"], isClosed=0)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.hide(thread_id=content["thread"], status=1)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def restore(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.hide(thread_id=content["thread"], status=0)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def subscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            subscription = threadFunctions.add_subscribe(email=content["user"], thread_id=content["thread"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": subscription}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def unsubscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            subscription = threadFunctions.delete_subscription(email=content["user"],
                                                             thread_id=content["thread"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": subscription}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def update(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.update(id=content["thread"], slug=content["slug"],
                                           message=content["message"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def vote(request):
    if request.method == "POST":
        content = json.loads(request.body)
        try:
            thread = threadFunctions.vote(id=content["thread"], vote=content["vote"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=400)