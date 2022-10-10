# more.hack4_solution

This is our solution for VTB moretech 4.0 data hackathon, data track.
We provide API that extracts trends from news and provides digests for roles such as businessmen and buhgalter (it can be scaled). 



We extracted 29k news from rbk.business, gazeta.ru, forbes.ru, kommersant.ru.

Task 1. Extracting trends.
Trend is by definition a topic which was not popular some time ago, but for the latest amount of time it's popularity increases. (Not to misunderstand with just always popular topics).
Therefore, our idea was following:
1. Firstly, we group news for determined periods of time (i.e. a month, a week, a day).
2. For each group we make embeddings for each news, make clasterisation, define biggest clusters and its centers.
3. The center clusters then are compared. If there is no cluster of "old" news around a cluster of "new" news, then it is a trend.
4. Extract the news, that match center clusters of trends.
5. Extract keywords from this news. 

Task 2. Making digests.
Our idea:
1. We parse data from unrelated to target professions sources.
2. We construct list of words and phrases that is supposed to be of interest to target roles.
3. We extract keywords from news and make their embeddings.
4. For each of the role words we choose 30 (or another amount) of closest keywords.
5. We calculate the most relevant news by number of its keywords that are close to the list of role words.

We used Scrapy for parsing, 'rubert-tiny' for embedding and keyword extraction, AgglomerativeClustering algorithm for clustering, FastAPI for API
