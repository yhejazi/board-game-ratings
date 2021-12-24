import pandas as pd
import time
from urllib.request import urlopen
from games_helper import *


if __name__ == '__main__':
    # Get all game names and IDs
    # Retrieved from Beefsack's pull of BGG data on 11/18/2021
    link = "https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/2021-11-18.csv"
    f = urlopen(link)
    games = pd.read_csv(f)
    games.sort_values('Users rated', ascending=False, inplace=True)

    # Create games table
    sql_create_table_games = """ CREATE TABLE IF NOT EXISTS games(
                                    game_id integer PRIMARY KEY,
                                    name text,
                                    description text,
                                    year_published integer,
                                    min_players integer,
                                    max_players integer, 
                                    playing_time integer,
                                    min_playtime integer,
                                    max_playtime integer,             
                                    min_age integer, 
                                    category text, 
                                    mechanic text, 
                                    family text, 
                                    implementation text,
                                    expansion text, 
                                    designer text, 
                                    artist text, 
                                    publisher text);"""
    
    conn = create_con('reviews.db')
    del_all_records(conn)
    create_table(conn, sql_create_table_games)

    ids = games['ID']
    id_count = 0
    print('Total number of games: {}'.format(len(ids)))
    for id in ids: 
            try:
                if (id_count%100 == 0): 
                    print('Getting {} - {} games'.format(id_count, id_count + 99))                 
                insert_list = get_game_info(id)
                create_games(conn, insert_list)
                id_count += 1
                time.sleep(2)
            except Exception as e:
                print('ERROR:', e)
                time.sleep(10)
        
    print('Done scraping')

    # Write data to csv file
    games = pd.read_sql_query("SELECT * FROM games", conn)
    conn.close()
    games.to_csv('games.csv', index = False) 