# coding=utf-8
__author__ = 'deyl94'

import dbFunctions

def save_user(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = dbFunctions.select_query('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                           (email, ))
        if len(user) == 0:
            dbFunctions.change_query(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = dbFunctions.select_query(
            'SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, )
        )
    except Exception as e:
        raise Exception(e.message)
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response

def details(email):
    user = dbFunctions.select_query(
        'SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, )
    )
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }

    user_response["followers"] = followers(email, "follower")
    user_response["following"] = followers(email, "followee")

    subs_list = []
    subscriptions = dbFunctions.select_query(
        'SELECT thread FROM Subscriptions WHERE user = %s', (email, )
    )
    for i in subscriptions:
        subs_list.append(i[0])
    user_response["subscriptions"] = subs_list
    return user_response

def followers(email, type):
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    f_list = dbFunctions.select_query(
        "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type +
        " WHERE " + where + " = %s ", (email, )
    )
    l = []
    for el in f_list:
        l.append(el[0])
    return l

def add_follow(email1, email2):
    follower = dbFunctions.select_query(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follower) == 0:
        dbFunctions.change_query('INSERT INTO Followers (follower, followee) VALUES (%s, %s)', (email1, email2, ))

    user = details(email1)
    return user

def followers_list(email, type, params):
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    query = "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type + \
            " WHERE " + where + " = %s "
    if "since_id" in params:
        query += " AND Users.id >= " + str(params["since_id"])
    if "order" in params:
        query += " ORDER BY Users.name " + params["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    followers_id = dbFunctions.select_query(query=query, params=(email, ))

    list_f = []
    for id in followers_id:
        id = id[0]
        list_f.append(details(email=id))

    return list_f

def remove_follow(email1, email2):
    follows = dbFunctions.select_query(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follows) != 0:
        dbFunctions.change_query(
            'DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
        )
    else:
        raise Exception("Упс!")

    return details(email1)

def update_user(email, about, name):
    dbFunctions.change_query('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
                           (email, about, name, email, ))
    return details(email)

