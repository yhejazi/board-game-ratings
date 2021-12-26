import math
import urllib.request
import xmltodict
import sqlite3
from sqlite3 import Error
import traceback

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

def create_reviews(conn, reviews):
    sql = """ INSERT INTO reviews(user, rating, comment, ID)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    for review in reviews:
        cur.execute(sql,review)
    cur.execute(sql, review) # review
    conn.commit()

def del_all_records(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS reviews")
    conn.commit()

def make_batches(games):
    """Takes in a list of games; returns a generator of slices needed in 
    batches of 100"""
    if len(games) < 100:
        yield slice(0, len(games))
    else:
        num_batches = len(games) // 100
        for b in range(num_batches):
            result = slice(b * 100, (b+1) * 100)
            yield result
        # Get remainder using the last b
        yield slice((b+1) * 100, len(games) + 1)

def get_num_pages(game_id):
    """Takes in a game id; returns the total number of pages of ratings for
    that game"""
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?id=' + str(game_id) + '&ratingcomments=1'
    u = urllib.request.urlopen(url).read()
    doc = xmltodict.parse(u)
    num_pages = math.ceil(int(doc['items']['item']['comments']['@totalitems'])/100) + 1
    return num_pages

def get_reviews(ids, p): 
    """Takes in a list of ids and a page number, returns list of dictionaries 
    of the ratings"""
    # given a url of an object and a page, return list of dicts with the comments
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?id=' + ids + '&ratingcomments=1' + '&&page=' + str(p)
    u = urllib.request.urlopen(url).read()
    doc = xmltodict.parse(u)
    return doc 

def process_reviews(conn, url_result):
    """Takes in a database connection and XML result; gets ratings from the XML 
    and stores in the databse. Then returns a list of games that have no reviews 
    left to parse"""
    remove_list = []
    # For each game g in the batch
    for g in url_result['items']['item']:
        if not isinstance(g, str):
            # If there are reviews for the game
            if 'comment' in g['comments'].keys():
                try:
                    reviews = [(g['@id'],) + tuple(review.values()) for review in g['comments']['comment']]         
                    create_reviews(conn, reviews)
                except Exception as e:
                    print(e, traceback.format_exc())
            else:
                # No more reviews for that game. Add to remove list
                remove_list.append(int(g['@id']))
    return remove_list





