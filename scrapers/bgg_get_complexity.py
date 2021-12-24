import pandas as pd 
import time
from urllib.request import urlopen
from complexity_helper import *


if __name__ == '__main__':
    # Get all game names and IDs
    # Retrieved from Beefsack's pull of BGG data on 11/18/2021
    link = "https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/2021-11-18.csv"
    f = urlopen(link)
    games = pd.read_csv(f)
    games.sort_values('Users rated', ascending=False, inplace=True)

    # Create games table
    sql_create_table_complexity = """ CREATE TABLE IF NOT EXISTS complexity(
                                    game_id integer PRIMARY KEY,
                                    complexity decimal
                                    );
                                    """
    
    conn = create_con('reviews.db')
    del_all_records(conn)
    create_table(conn, sql_create_table_complexity)

    ids = games['ID']
    id_count = 0
    print('Total number of games: {}'.format(len(ids)))
    for id in ids: 
            try:
                if (id_count%100 == 0): 
                    print('Getting {} - {} games'.format(id_count, id_count + 99))                 
                insert_list = get_complexity(id)
                create_complexity(conn, insert_list)
                id_count += 1
            except Exception as e:
                print('ERROR:', e)
                time.sleep(10)
        
    print('Done scraping')

    # Write data to csv file
    complexities = pd.read_sql_query("SELECT * FROM complexity", conn)
    conn.close()
    complexities.to_csv('complexity.csv', index = False) 