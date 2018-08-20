import socket
import static_funcs
import sqlite3
from passlib.hash import pbkdf2_sha256
import ast
import ftplib
import time
import threading
s = socket.socket()
host = socket.gethostname()
port = 1200
s.bind((host, port))
db = sqlite3.connect("database")
cur = db.cursor()


# aggregate sql functions used to get the amount of wins and losses for each user
def db_get_leaderboard():
    cur.execute("SELECT username, elo FROM user ORDER BY elo DESC")
    users = cur.fetchall()
    leaderboard_data = []
    for user in users:
        cur.execute("SELECT COUNT(result_id) FROM duel_results WHERE user_id1 ='"+str(user[0])+"'")
        wins = cur.fetchone()[0]
        cur.execute("SELECT COUNT(result_id) FROM duel_results WHERE user_id2 ='"+str(user[0])+"'")
        losses = cur.fetchone()[0]
        leaderboard_data.append([user[1], user[0], wins, losses])
    return str(leaderboard_data)


# runs a simple select query with specified fetch command
def db_select(exec, fetch):
    cur.execute(exec)
    if fetch == "one":
        return str(cur.fetchone())
    elif fetch == "all" or fetch == "all2":
        data = cur.fetchall()
        return str(data)


def db_login(user, passw):
    cur.execute("SELECT username FROM user")
    users = cur.fetchall()
    for i in users:
        # if username the user entered is in the list of usernames from the database, then check if the passwords match
        # otherwise, retunr none and the client will handle this as the username being incorrect
        if user == i[0]:
            cur.execute("SELECT * FROM user WHERE username = '" + str(i[0]) + "'")
            user_data = cur.fetchone()
            password = user_data[2]
            if pbkdf2_sha256.verify(passw, password):
                user_data = list(user_data)
                del user_data[2]
                # if the username is correct and the password input matches the password from the user record with the
                # same usernme as the one input, return the user data without the password.
                return "['user pass'," + str(user_data) + "]"
            else:
                # if the username is correct, however the passwords do not match, return user and the client will
                # handle this as the password being incorrect
                return "['user']"
    return "['none']"


def db_register(username, name, passw, email, school, postcode):
    cur.execute("SELECT username, email FROM user")
    users = cur.fetchall()
    print(users)
    print(username, name, passw, email, school)
    error_list = []
    for user in users:
        # checks if the email and username exist in the database already
        if user[0] == username:
            error_list.append("user")
        if user[1] == email:
            error_list.append("email")
    # checks if the school code is in the set valid school codes
    if school.upper() not in ["ZE4", "TE5"]:
        error_list.append("school")
    if len(error_list) == 0:
        # encrypt the password
        password = pbkdf2_sha256.hash(passw)
        # save all entered fields
        cur.execute("INSERT INTO user (username, password, name, email, school, admin_lvl, postcode, elo)"
                    "VALUES (?, ?, ?, ?, ?, 1, ?, 1000)", (username, password, name, email, school, postcode))
        db.commit()
        cur.execute("SELECT user_id FROM user WHERE username='" + str(username) + "'")
        user_id = cur.fetchone()
        session = ftplib.FTP("spackwell.hol.es", "u377515927.billymaths", "0rC?@q/nqmji7x@PxS")
        image = open("img\\profile_placeholder2.jpg", "rb")
        session.storbinary("STOR profile_pics/" + str(user_id[0]) + ".png", image)
        image.close()
    return str(error_list)


def db_save_results(user_id, time, correct, no_questions, topic, type, date):
    cur.execute("INSERT INTO work_results (user_id, time, correct, no_questions, topic, type, date)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, time, correct, no_questions, topic, str(type), date))
    db.commit()
    return "['none']"


def db_save_duel_results(user_id1, user_id2, time, no_questions, topic, type, date):
    cur.execute("INSERT INTO duel_results (user_id1, user_id2, time, no_questions, topic, type, date)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id1, user_id2, time, no_questions, topic, str(type), date))
    db.commit()
    return "['none']"


def db_update_elo(user_id, elo):
    cur.execute("UPDATE user SET elo = "+elo+" WHERE user_id = "+user_id)
    db.commit()
    return "['none']"


def connection_handler():
    s.listen(5)
    while True:
        connection, addr = s.accept()
        print("Connection established.", addr)
        connection.send(b"Connection established.")
        msgr = static_funcs.bytetostr(connection.recv(1024))
        print(msgr)
        if msgr == "Test":
            connection.send(b"y")
            msgr = ast.literal_eval(static_funcs.bytetostr(connection.recv(1024)))
            if msgr[0] == "select":
                connection.send(bytes(db_select(msgr[1], msgr[2]), "utf8"))
            elif msgr[0] == "login":
                connection.send(bytes(db_login(msgr[1], msgr[2]), "utf8"))
            elif msgr[0] == "register":
                connection.send(bytes(db_register(msgr[1], msgr[2], msgr[3], msgr[4], msgr[5], msgr[6]), "utf8"))
            elif msgr[0] == "save_work_results":
                connection.send(bytes(db_save_results(msgr[1], msgr[2], msgr[3], msgr[4], msgr[5], msgr[6], msgr[7]), "utf8"))
            elif msgr[0] == "save_duel_results":
                connection.send(bytes(db_save_duel_results(msgr[1], msgr[2], msgr[3], msgr[4], msgr[5], msgr[6], msgr[7]), "utf8"))
            elif msgr[0] == "update_elo":
                connection.send(bytes(db_update_elo(msgr[1], msgr[2]), "utf8"))
            elif msgr[0] == "leaderboard":
                connection.send(bytes(db_get_leaderboard(), "utf8"))
        else:
            connection.send(b"n")

connection_handler()
