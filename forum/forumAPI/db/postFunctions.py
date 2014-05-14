# coding=utf-8
__author__ = 'roland'

import dbFunctions
import forumFunctions
import userFunctions
import threadFunctions

def new_post(date, thread, message, user, forum, optional):
    if len(dbFunctions.select_query("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("Нет thread с айдишником = " + str(thread) + " в форуме " + forum)
    if "parent" in optional:
        if len(dbFunctions.select_query("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                                    "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))) == 0:
            raise Exception("Нет поста с айдишником = " + optional["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    for param in optional:
        query += ", " + param
        values += ", %s"
        parameters.append(optional[param])

    query += ") VALUES " + values + ")"

    update_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    dbFunctions.change_query(update_posts, (thread, ))
    post_id = dbFunctions.change_query(query, parameters)

    post = dbFunctions.select_query('SELECT date, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, message, thread, user '
                       'FROM Posts WHERE id = %s', (post_id, ))
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'forum': post[1],
        'id': post[2],
        'isApproved': bool(post[3]),
        'isDeleted': bool(post[4]),
        'isEdited': bool(post[5]),
        'isHighlighted': bool(post[6]),
        'isSpam': bool(post[7]),
        'message': post[8],
        'thread': post[9],
        'user': post[10],

    }
    return post_response

def details(details_id, related):
    post = dbFunctions.select_query(
        'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (details_id, )
    )
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }

    if "user" in related:
        post_response["user"] = userFunctions.details(post["user"])
    if "forum" in related:
        post_response["forum"] = forumFunctions.details(short_name=post["forum"], related=[])
    if "thread" in related:
        post_response["thread"] = threadFunctions.details(id=post["thread"], related=[])
    return post

def posts_list(entity, params, identifier, related=[]):
    query = "SELECT id FROM Posts WHERE " + entity + " = %s "
    parameters = [identifier]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    post_ids = dbFunctions.select_query(query=query, params=parameters)
    post_list = []
    for id in post_ids:
        id = id[0]
        post_list.append(details(details_id=id, related=related))
    return post_list

def hide(post_id, status):
    dbFunctions.update_query("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (status, post_id, ))
    request = {
        "post": post_id
    }
    return request


def update(update_id, message):
    dbFunctions.update_query('UPDATE Posts SET message = %s WHERE id = %s', (message, update_id, ))
    return details(details_id=update_id, related=[])


def vote(vote_id, vote_type):
    if vote_type == -1:
        dbFunctions.change_query("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (vote_id, ))
    else:
        dbFunctions.change_query("UPDATE Posts SET likes=likes+1, points=points+1 where id = %s", (vote_id, ))
    return details(details_id=vote_id, related=[])

