import urllib.request
import sqlite3
from sqlite3 import Error
import json

def create_con(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


def del_all_records(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS complexity")
    conn.commit()

def create_complexity(conn, insert_list):
    sql = """ INSERT INTO complexity(game_id, complexity)
            VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, insert_list)
    conn.commit()

def get_complexity(id):
    poll_id = get_poll(id)
    score = get_results(poll_id)
    return [id, score]

def get_poll(id): 
    url = 'https://www.boardgamegeek.com/geekitempoll.php?action=view&itempolltype=boardgameweight&objecttype=thing&objectid=' + str(id)
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode())

    return data["poll"]["pollid"]

def get_results(poll_id):
    url = 'https://www.boardgamegeek.com/geekpoll.php?action=results&pollid=' + str(poll_id)
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode())

    complexity_sum = 0
    total_votes = int(data["pollquestions"][0]["results"]["voters"])
    if total_votes == 0: return 0

    for choice in data["pollquestions"][0]["results"]["results"]:
        number = int(choice["columnbody"][-2])
        votes = int(choice["votes"])

        complexity_sum += number * votes

    return round(complexity_sum / total_votes, 2)
