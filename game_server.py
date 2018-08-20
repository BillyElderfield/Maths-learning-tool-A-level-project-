import socket
import sqlite3
import static_funcs
import ast
import threading
import random
import math
s = socket.socket()
host = socket.gethostname()
port = 1201
s.bind((host, port))
db = sqlite3.connect("database")
cur = db.cursor()
connections = []


def game(data, uid2, con1, con2):
    print(str(data) + str(uid2) + str(con1), str(con2))
    if data[1] == "fractions":
        questions = set_frac_numbers(int(data[2]))
    elif data[1] == "quadratics":
        questions = set_quad_numbers(int(data[2]), data[3])
    con1.send(bytes(str([uid2, questions]), "utf8"))
    con2.send(bytes(str([data[0], questions]), "utf8"))
    while True:
        msgr1 = static_funcs.bytetostr(con1.recv(1024))
        con2.send(bytes(msgr1, "utf8"))
        msgr2 = static_funcs.bytetostr(con2.recv(1024))
        con1.send(bytes(msgr2, "utf8"))
        if msgr1 == data[2]:
            con1.send(bytes("end", "utf8"))
            break
        elif msgr2 == data[2]:
            con2.send(bytes("end", "utf8"))
            break


def set_quad_numbers(qn, types):
    questions = []
    # if factorising an expanding selected
    if types[0] == 1 and types[1] == 1:
        for i in range(round((int(qn) / 2))):
            simple_numbers = False
            while True:
                q1 = random.randint(1, 4)
                q2 = random.randint(1, 10)
                q3 = random.randint(1, 20)
                try:
                    if math.sqrt((q2 ** 2) - (4 * q1 * q3)) % 1 == 0:
                        ac = q1 * q3
                        ac_factors = static_funcs.get_factors(ac)
                        for pair in ac_factors:
                            if pair[0] + pair[1] == q2:
                                valid_pair = pair
                                simple_numbers = True
                                break
                        if simple_numbers:
                            break
                except:
                    pass
            questions.append([q1, q2, q3, valid_pair])
        for i in range(round((int(qn) / 2)) + 1):
            q1 = random.randint(1, 4)
            q2 = random.randint(1, 10)
            q3 = random.randint(1, 4)
            q4 = random.randint(1, 10)
            questions.append([q1, q2, q3, q4])
    # if just factorising
    elif types[0] == 1:
        for i in range(qn):
            simple_numbers = False
            while True:
                # Generate random numbers for values.
                q1 = random.randint(1, 4)
                q2 = random.randint(1, 10)
                q3 = random.randint(1, 20)
                try:
                    valid_pair = (0, 0)
                    if math.sqrt((q2 ** 2) - (4 * q1 * q3)) % 1 == 0:
                        ac = q1 * q3
                        ac_factors = static_funcs.get_factors(ac)
                        for pair in ac_factors:
                            if pair[0] + pair[1] == q2:
                                valid_pair = pair
                                simple_numbers = True
                                break
                        if simple_numbers:
                            break
                except:
                    pass
            questions.append([q1, q2, q3, valid_pair])
    # if just expanding
    else:
        for i in range(qn):
            q1 = random.randint(1, 4)
            q2 = random.randint(1, 10)
            q3 = random.randint(1, 4)
            q4 = random.randint(1, 10)
            questions.append([q1, q2, q3, q4])
    print(questions)
    return questions

def set_frac_numbers(qn):
    questions = []
    for i in range(qn):
        rand = random.randrange(1, 20)
        if rand <= 10:
            x1 = (str(random.randrange(1, 6)))
            x2 = (str(random.randrange(1, 6)))
            y1 = (str(random.randrange(1, 6)))
            y2 = (str(random.randrange(1, 6)))
        elif 10 < rand < 16:
            x1 = (str(random.randrange(1, 11)))
            x2 = (str(random.randrange(1, 11)))
            y1 = (str(random.randrange(1, 11)))
            y2 = (str(random.randrange(1, 11)))
        else:
            x1 = (str(random.randrange(1, 21)))
            x2 = (str(random.randrange(1, 21)))
            y1 = (str(random.randrange(1, 21)))
            y2 = (str(random.randrange(1, 21)))
        questions.append([x1, x2, y1, y2])
    return questions


def check_connection(con):
    s.setblocking(0)
    try:
        con.send(b"check")
        msgr = static_funcs.bytetostr(con.recv(1024))
        if msgr == "check":
            return True
        else:
            return False
    except Exception:
        return False


def matchmaking():
    s.listen(5)
    while True:
        connection, addr = s.accept()
        print("Connection established.", addr)
        connection.send(b"Connection established.")
        msgr = static_funcs.bytetostr(connection.recv(1024))
        if msgr == "Test":
            connection.send(b"y")
            game_found = False
            msgr = ast.literal_eval(static_funcs.bytetostr(connection.recv(1024)))
            dead_cons = []
            for i in connections:
                if check_connection(i[0][0]):
                    if msgr[1:] == i[1][0][1:]:
                        print("Match")
                        dead_cons.append(i)
                        game_found = True
                        threading._start_new_thread(game, (i[1][0], msgr[0], i[0][0], connection))
                        break
                else:
                    print("Dead connection found")
                    dead_cons.append(i)
            for i in dead_cons:
                connections.remove(i)
            s.setblocking(1)
            if not game_found:
                connection_data = [[connection], [msgr]]
                connections.append(connection_data)
            print("length of connections list: "+str(len(connections)))
        else:
            connection.send(b"n")


matchmaking()
