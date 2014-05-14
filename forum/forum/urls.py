# coding=utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forum.views.home', name='home'),
    # url(r'^forum/', include('forum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Forum
    url(r'^db/api/forum/create/$', 'forumAPI.views.forum.create', name='create_forum'),
    url(r'^db/api/forum/details/$', 'forumAPI.views.forum.details', name='details_forum'),
    url(r'^db/api/forum/listPosts/$', 'forumAPI.views.forum.list_posts', name='listPosts_forum'),
    url(r'^db/api/forum/listThreads/$', 'forumAPI.views.forum.list_threads', name='listThreads_forum'),
    url(r'^db/api/forum/listUsers/$', 'forumAPI.views.forum.list_users', name='listUsers_forum'),

    # Post
    url(r'^db/api/post/create/$', 'forumAPI.views.post.create', name='create_post'),
    url(r'^db/api/post/details/$', 'forumAPI.views.post.details', name='details_post'),
    url(r'^db/api/post/list/$', 'forumAPI.views.post.post_list', name='list_post'),
    url(r'^db/api/post/remove/$', 'forumAPI.views.post.remove', name='remove_post'),
    url(r'^db/api/post/restore/$', 'forumAPI.views.post.restore', name='restore_post'),
    url(r'^db/api/post/update/$', 'forumAPI.views.post.update', name='update_post'),
    url(r'^db/api/post/vote/$', 'forumAPI.views.post.vote', name='vote_post'),

    # User
    url(r'^db/api/user/create/$', 'forumAPI.views.user.create', name='create_user'),
    url(r'^db/api/user/details/$', 'forumAPI.views.user.details', name='details_user'),
    url(r'^db/api/user/follow/$', 'forumAPI.views.user.follow', name='follow_user'),
    url(r'^db/api/user/listFollowers/$', 'forumAPI.views.user.list_followers', name='list_followers'),
    url(r'^db/api/user/listFollowing/$', 'forumAPI.views.user.list_following', name='list_following'),
    url(r'^db/api/user/listPosts/$', 'forumAPI.views.user.list_posts', name='posts_user'),
    url(r'^db/api/user/unfollow/$', 'forumAPI.views.user.unfollow', name='unfollow_user'),
    url(r'^db/api/user/updateProfile/$', 'forumAPI.views.user.update_profile', name='update_user'),


    # Thread
    url(r'^db/api/thread/close/$', 'forumAPI.views.thread.close', name='close_thread'),
    url(r'^db/api/thread/create/$', 'forumAPI.views.thread.create', name='create_thread'),
    url(r'^db/api/thread/details/$', 'forumAPI.views.thread.details', name='details_thread'),
    url(r'^db/api/thread/list/$', 'forumAPI.views.thread.thread_list', name='list_thread'),
    url(r'^db/api/thread/listPosts/$', 'forumAPI.views.thread.list_posts', name='list_posts_thread'),
    url(r'^db/api/thread/open/$', 'forumAPI.views.thread.open', name='open_thread'),
    url(r'^db/api/thread/remove/$', 'forumAPI.views.thread.remove', name='remove_thread'),
    url(r'^db/api/thread/restore/$', 'forumAPI.views.thread.restore', name='restore_thread'),
    url(r'^db/api/thread/subscribe/$', 'forumAPI.views.thread.subscribe', name='subscribe_thread'),
    url(r'^db/api/thread/unsubscribe/$', 'forumAPI.views.thread.unsubscribe', name='unsubscribe_thread'),
    url(r'^db/api/thread/update/$', 'forumAPI.views.thread.update', name='update_thread'),
    url(r'^db/api/thread/vote/$', 'forumAPI.views.thread.vote', name='vote_thread'),

    # TRUNCATE базы
    url(r'^db/clear/$', 'forumAPI.db.dbFunctions.clear', name='clear')
)
