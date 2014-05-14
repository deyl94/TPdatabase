# coding=utf-8
__author__ = 'deyl94'

import dbFunctions
import userFunctions

def new_forum(name, short_name, user):
    """
    Создание нового форума
    """
    dbFunctions.exist(entity="Users", identifier="email", value=user)
    forum = dbFunctions.select_query(
        'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        dbFunctions.change_query('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)',
                               (name, short_name, user, ))
        forum = dbFunctions.select_query(
            'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
        )

    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response

def forum_details(short_name, related):
    """
    Подробности о форуме
    """
    forum = dbFunctions.select_query(
        'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        raise ("Нет форума с именем=" + short_name)

    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }

    if "user" in related:
        response["user"] = userFunctions.details(forum["user"])
    return forum


def list_users(short_name, optional):
    """

    """
    query = "SELECT distinct email FROM Users JOIN Posts ON Posts.user = Users.email " \
            " JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        query += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    users = dbFunctions.select_query(query, (short_name, ))
    list_u = []
    for user in users:
        user = user[0]
        list_u.append(users.details(user))
    return list_u