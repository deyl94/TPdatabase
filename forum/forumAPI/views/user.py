# coding=utf-8
__author__ = 'deyl94'

from forumAPI.db import userFunctions, postFunctions
from django.http import HttpResponse
import json

def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        optional = dict([(k, request_data[k]) for k in ["isAnonymous"] if k in request_data])
        try:
            user = userFunctions.new_user(email=request_data["email"], username=request_data["username"],
                                   about=request_data["about"], name=request_data["name"], optional=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def details(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        try:
            user_details = userFunctions.details(email=request_data["user"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user_details}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def follow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        try:
            following = userFunctions.add_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": following}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_followers(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        followers_param = dict([(k, request_data[k]) for k in ["limit", "order", "since_id"] if k in request_data])
        try:
            follower_l = userFunctions.followers_list(email=request_data["user"], type="follower", params=followers_param)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": follower_l}), content_type='application/json')
    else:
        return HttpResponse(status=400)


def list_following(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        followers_param = dict([(k, request_data[k]) for k in ["limit", "order", "since_id"] if k in request_data])
        try:
            followings = userFunctions.followers_list(email=request_data["user"], type="followee", params=followers_param)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": followings}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def list_posts(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        optional = dict([(k, request_data[k]) for k in ["limit", "order", "since"] if k in request_data])
        try:
            posts_l = postFunctions.posts_list(entity="user", params=optional, identifier=request_data["user"], related=[])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": posts_l}), content_type='application/json')
    else:
        return HttpResponse(status=400)

def unfollow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        try:
            following = followers.remove_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": following}), content_type='application/json')
    else:
        return HttpResponse(status=405)

def update_profile(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        try:
            user = users.update_user(email=request_data["user"], name=request_data["name"], about=request_data["about"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user}), content_type='application/json')
    else:
        return HttpResponse(status=405)