__author__ = 'deyl94'

import dbFunctions
import userFunctions
import forumFunctions

def trigger(id, isClosed):
    dbFunctions.update_query("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))
    response = {
        "thread": id
    }
    return response

def new_thread(forum, title, isClosed, user, date, message, slug, optional):
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = dbFunctions.select_query(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(thread) == 0:
        dbFunctions.change_query('INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
                               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (forum, title, isClosed, user, date, message, slug, isDeleted, ))
        thread = dbFunctions.select_query(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
    }
    return response

def details(id, related):
    thread = dbFunctions.select_query(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )

    thread = thread[0]
    thread_response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    if "user" in related:
        thread_response["user"] = userFunctions.details(thread["user"])
    if "forum" in related:
        thread_response["forum"] = forumFunctions.details(short_name=thread["forum"], related=[])

    return thread_response

def threads_list(entity, identifier, related, params):
    query = "SELECT id FROM Threads WHERE " + entity + " = %s "
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

    thread_ids = dbFunctions.select_query(query=query, params=parameters)
    thread_l = []

    for id in thread_ids:
        id = id[0]
        thread_l.append(details(id=id, related=related))

    return thread_l

def hide(thread_id, status):
    dbFunctions.update_query(
        'UPDATE Threads SET isDeleted = %s WHERE id = %s', (status, thread_id, )
    )
    response = {
        "thread": thread_id
    }
    return response

def add_subscribe(email, thread_id):
    subscription = dbFunctions.select_query(
        'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        dbFunctions.change_query(
            'INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, )
        )
        subscription = dbFunctions.select_query(
            'select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
        )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def delete_subscription(email, thread_id):
    subscription = dbFunctions.select_query(
        'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    dbFunctions.change_query(
        'DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response

def update_thread(id, slug, message):
    dbFunctions.change_query(
        'UPDATE Threads SET slug = %s, message = %s WHERE id = %s', (slug, message, id, )
    )
    return details(id=id, related=[])

def vote(id, vote):
    if vote == -1:
        dbFunctions.change_query(
            'UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s', (id, )
        )
    else:
        dbFunctions.change_query(
            'UPDATE Threads SET likes=likes+1, points=points+1 where id = %s', (id, )
        )

    return details(id=id, related=[])