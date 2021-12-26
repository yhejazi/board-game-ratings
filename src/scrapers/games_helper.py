import urllib.request
import xmltodict
import sqlite3
from sqlite3 import Error

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
    cur.execute("DROP TABLE IF EXISTS games")
    conn.commit()

def create_games(conn, insert_list):
    sql = """ INSERT INTO games(game_id, name, description, year_published, min_players, 
            max_players, playing_time, min_playtime, max_playtime, min_age, category, 
            mechanic, family, implementation, expansion, designer, artist, publisher)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, insert_list)
    conn.commit()


def get_game_info(id): 
    """"""
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?id=' + str(id)
    u = urllib.request.urlopen(url).read()
    doc = xmltodict.parse(u)
    item = doc['items']['item']
    
    name_str = item['name']
    if(type(name_str) == list):
        name_str = name_str[0]
    name = name_str['@value']
    
    description = item['description']
    year_published = item['yearpublished']['@value']
    min_players = item['minplayers']['@value']
    max_players = item['maxplayers']['@value']
    playing_time = item['playingtime']['@value']
    min_playtime = item['minplaytime']['@value']
    max_playtime = item['maxplaytime']['@value']
    min_age = item['minage']['@value']

    # Get info from links
    link_info = {}
    link_info = {'boardgamecategory': [], 
                'boardgamemechanic': [], 
                'boardgamefamily': [], 
                'boardgameimplementation': [], 
                'boardgameexpansion': [], 
                'boardgamedesigner': [], 
                'boardgameartist': [], 
                'boardgamepublisher': [], 
                'boardgameintegration': [], 
                'boardgamecompilation': []}

    for link in item['link']:
        col = link['@type']
        link_info[col].append(link['@value'])
  
    # Join column values into one string
    for k in link_info.keys():
        link_info[k] = ', '.join(link_info[k])

    return [id, name, description, year_published, min_players, max_players, playing_time, 
            min_playtime, max_playtime, min_age, link_info['boardgamecategory'], link_info['boardgamemechanic'], 
            link_info['boardgamefamily'], link_info['boardgameimplementation'], link_info['boardgameexpansion'], 
            link_info['boardgamedesigner'], link_info['boardgameartist'], link_info['boardgamepublisher']]






