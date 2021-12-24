# User Satisfaction on Board Game Complexity
**Authors: Mohamed Elghetany, Yasmine Hejazi, Keith Hutton, Melissa McGee**

Our society is currently living in a board game renaissance. More than 5,000 new board games or expansions are released every year according to online resource Board Game Geek. With new games being created day after day, players are turning to explore more heavily-themed and complex innovations that can make games take hours and even days to play.

The board game industry has undergone a huge development over hundreds of years, and with that comes the birth of many new genres and mechanics that make board games more diverse and complex. With the knowledge of a constantly-developing and diversifying market, we understand that not all board game innovations are successful. As new categories, mechanics, and complexities are introduced, we want to understand what makes board games more enjoyable and what doesn’t. Specifically, we aim to answer the research question:

> How does a board game’s complexity affect its rating?

Newer board games bring in a wide range of complexity that didn't exist previously. We would like to explore the relationship of board game complexity and the user rating it receives because this information can allow us to understand how much complexity is good. As we continue to develop new games, our goal is to use this information to make decisions on the complexity level we design for to satisfy enthusiastic board game players.

## Data

Our analysis leverages data scraped from [BoardGameGeek.com](boardgamegeek.com), an online platform and community that aims to be the definitive source for board game/tabletop and card game content. Board Game Geek has an extensive database of more than 20,000 board games as well as an active community of users who discuss, buy, sell, trade and play board games. Each game has its own game entry with information about a game, user ratings, forums for discussion, and more.

Three different data sources are scraped from Board Game Geek to be utilized in our research: **reviews**, **games**, and **complexity**. Both the **reviews** dataset and the **games** dataset require a complete list of Board Game Geek board game IDs in order to fetch results through the XML API. 

We retrieve the list of game IDs through the [bgg-ranking-historicals](https://github.com/beefsack/bgg-ranking-historicals) GitHub repository by GitHub user [Beefsack](https://github.com/beefsack). Game IDs are scraped every day from Board Game Geek and added to this repository as CSV files. For this research iteration, we use the CSV file scraped on [November 18, 2021](https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/2021-11-18.csv) and utilize this information on the same day to scrape our own data.

**Reviews data**: XML data is retrieved and then scraped for each board game in batches of one hundred. Board Game Geek provides an XML API  called [BGG XML API2](https://boardgamegeek.com/wiki/page/BGG_XML_API2). We use our collection of board game IDs to fetch XML data that we then parse to gather information on username, rating, and comments. To treat dependency of reviews within each board game, we omit ratings that occur after the Board Game Geek user has already rated the game once. 

**Games data**: XML data is retrieved and then scraped for each board game individually. Using the same [BGG XML API2](https://boardgamegeek.com/wiki/page/BGG_XML_API2), we are able to use our collection of board game IDs to fetch XML data. We parse the XML data to gather information on each board game including board game name, year published, minimum and maximum number of players, minimum age, category, mechanics, and more. 

**Complexity data**: The complexity of each board game is polled from users as a 1-5 rating on every board game homepage. For each board game, we use the Board Game Geek JSON API to retrieve the ID of the complexity poll for that game ID. We then use the same JSON API to query the results of that poll, and calculate the votes into a single complexity score.

All data files can be found in **[this Google Drive folder](https://drive.google.com/drive/folders/1NSgDOdEe5r_3t-JFMOfK-xRT4ljuA-IH?usp=sharing)**.