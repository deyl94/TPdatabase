# coding=utf-8
__author__ = 'deyl94'

import MySQLdb
from django.http import HttpResponse
import json

def connect():
    """
    Подключаемся к базе
    """
    host = "localhost"
    user = "root"
    password = ""
    db = "forumDB"
    return MySQLdb.connect(host, user, password, db, init_command='SET NAMES UTF8')

def select_query(query, parameters):
    """
    Выполнение SELECT запроса
    query - сам запрос
    parameters - параметры запроса
    Возвращает список строк
    """
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        cursor.close()
        db.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Ошибка во время SELECT запроса!")
    return result

def change_query(query, parameters):
    """
    Выполнение UPDATE, DELETE, INSERT запроса
    query - сам запрос
    parameters - параметры запроса
    Возвращает lastrowid
    """
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute(query, parameters)
        db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        db.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Ошибка во время UPDATE, DELETE, INSERT запроса!")
    return last_id

def clear(request):
    """
    Выполняет TRUNCATE таблиц базы forumDB
    """
    if request.method == "GET":
        try:
            db = connect()
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE Users")
            cursor.execute("TRUNCATE TABLE Forums")
            cursor.execute("TRUNCATE TABLE Threads")
            cursor.execute("TRUNCATE TABLE Posts")
            cursor.execute("TRUNCATE TABLE Followers")
            cursor.execute("TRUNCATE TABLE Subscriptions")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            cursor.close()
            db.close()
        except MySQLdb.Error:
            raise MySQLdb.Error("Ошибка во время TRUNCATE")
        return HttpResponse(json.dumps({"code": 0, "response": "TRUNCATE is success!"}), content_type='application/json')
    return HttpResponse(status = 400)