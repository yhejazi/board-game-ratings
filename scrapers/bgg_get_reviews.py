import pandas as pd
import time
from urllib.request import urlopen
from reviews_helper import *


if __name__ == '__main__':
    # Get all game names and IDs
    # Retrieved from Beefsack's pull of BGG data on 11/13/2021
    link = "https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/2021-11-18.csv"
    f = urlopen(link)
    games = pd.read_csv(f)
    games.sort_values('Users rated', ascending=False, inplace=True)


    # Create reviews table
    sql_create_table_reviews = """ CREATE TABLE IF NOT EXISTS reviews(
                                    review_id integer PRIMARY KEY,
                                    user text NOT NULL,
                                    rating NOT NULL,
                                    comment text,              
                                    ID integer,
                                    FOREIGN KEY(ID) REFERENCES games(game_id));"""

    conn = create_con('reviews.db')
    del_all_records(conn)
    create_table(conn, sql_create_table_reviews)

    game_generator = make_batches(games)  # Slice this to limit num of games

    ### Each batch has 100 games. One page will have the first 100 ratings for
    ### every game in the batch. As we iterate through pages, the games with  
    ### less # of ratings will drop off later pages. 
    for batch in game_generator: 
        print('----- Getting batch ' , batch.start, ':', batch.stop, ' -----', sep='')
        games_in_batch = list(games['ID'][batch]) # Get list of game IDs

        # Get max number of pages for the game with the most pages in batch
        num_pages = get_num_pages(games_in_batch[0])
        print('Number of pages in batch:', num_pages)

        if num_pages > 0:
            for p in range(num_pages):
                try:
                    print('Getting page {}. Page has reviews for {} games'.format(p, len(games_in_batch)))
                    if not games_in_batch:
                        break

                    # Create url input of game IDs
                    ids = ','.join(str(g) for g in games_in_batch)
                    url_result = get_reviews(ids, p)

                    # Process results & remove games that have no more ratings 
                    remove_list = process_reviews(conn, url_result)
                    if len(remove_list) > 0:
                        print('Removing', len(remove_list), 'games...')
                    games_in_batch = [g for g in games_in_batch if g not in remove_list]
                    time.sleep(8)
                except Exception as e:
                    print('ERROR:', e)
                    time.sleep(30)
        
    print('Done scraping')

    print('Checking and cleaning data...')
    df = pd.read_sql_query("SELECT * FROM reviews", conn)
    conn.close()

    # Clean and merge game data
    df.rename(columns={'user':'game_id', 'rating':'user', 'comment':'rating', 'ID':'comment'}, inplace=True)
    df = df[['user', 'rating', 'comment', 'game_id']]
    df['game_id'] = df['game_id'].astype('int64')
    df = df.merge(games, on='game_id', how='left')

    # Keep only the first review from each user for each game
    print('Removing {} duplicate user reviews:'.format(df.duplicated(subset=['user','game_id']).sum()))
    df.drop_duplicates(subset=['user', 'game_id'], keep='first', inplace=True, ignore_index=True)

    df.to_csv('reviews.csv', index = False) 