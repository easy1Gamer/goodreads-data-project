import asyncio
import json
import logging
import random
import re
import time
from concurrent import futures
from datetime import datetime
import asyncpg
import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import socksio

#%%
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("threads.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# %%
proxies_list = ['45.147.246.91:64994',
                '146.19.10.130:64430', '5.189.250.74:62494', '62.76.226.218:63594',
                '194.87.166.63:64972', '172.252.133.172:62920', '172.252.159.56:62648',
                '91.212.82.62:63226', '45.149.83.99:63340', '146.19.15.61:62814',
                '146.19.47.15:64520', '46.3.149.155:64654', '5.189.250.100:62986',
                '172.252.133.74:62840']

authenticators = 'CBbdXZpB:17jb4sSC'
#%%
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0',
    'Accept': '*/*',
    "Accept-Language": "*",
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Refer': 'https://www.goodreads.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'X-Api-Key': 'da2-xpgsdydkbregjhpr6ejzqdhuwy'
}

# %%
async def get_rn_async_proxy(proxies_list, authenticators):
    curr_proxy = random.choice(proxies_list)
    logger.info(msg=curr_proxy)
    proxies = f'http://{authenticators}@{curr_proxy}'
    # proxies = {
    #     'http://': httpx.AsyncHTTPTransport(proxy=f'http://{authenticators}@{curr_proxy}'),
    #     'https://': httpx.AsyncHTTPTransport(proxy=f'http://{authenticators}@{curr_proxy}')
    # }
    return proxies


def get_rn_proxy(proxies_list, authenticators):
    curr_proxy = random.choice(proxies_list)
    # print(curr_proxy)
    proxies = f'http://{authenticators}@{curr_proxy}'

    return proxies


# %%
class BookPage:
    @classmethod
    async def create(cls, book_index, curr_proxies, client):
        @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=0.5, max=5),
               retry=retry_if_exception_type(httpx.HTTPError), reraise=True)
        async def request():
                await asyncio.sleep(random.uniform(0.02, 0.09))
                html = (await client.get(f'https://www.goodreads.com/book/show/{book_index}', timeout=10)).text
                return html

        try:
            self = cls(await request(), book_index)
        except httpx.HTTPError:
            return None, book_index

        return self

    def __init__(self, html, book_index):
        self.book_index = book_index
        self.bs = BeautifulSoup(html, 'html.parser')

    def book_check(self):
        book_check = self.bs.find(class_='ErrorPage__title')
        return book_check

    def book_data(self):
        work_id = json.loads(self.bs.find('script', id='__NEXT_DATA__').get_text())
        work_id = work_id['props']['pageProps']['apolloState'].keys()
        for i in work_id:
            if 'Work:kca:' in i:
                work_id = i
        book_title = self.bs.find('h1', attrs={'class': 'Text Text__title1'}).get_text()
        author_name = self.bs.find('span', attrs={'class': 'ContributorLink__name'}).get_text()
        rating = float((self.bs.find('div', {'class': 'RatingStatistics__column'})).get_text().replace(',', '.'))
        rating_count = int(
            (re.match(r'[\d,]*', self.bs.find('span', {'data-testid': 'ratingsCount'}).get_text())[0]).replace(',', ''))
        reviews_count = int(
            (re.match(r'[\d,]*', self.bs.find('span', {'data-testid': 'reviewsCount'}).get_text())[0]).replace(',', ''))
        genres = self.bs.find('script', id='__NEXT_DATA__')
        genres_list = []
        if genres is not None:
            genres = json.loads(genres.get_text())
            genres = genres['props']['pageProps']['apolloState']
            for j in genres.keys():
                if 'Book:kca://book/amzn1.gr.book.v1' in j:
                    if 'bookGenres' in genres[j]:
                        for k in genres[j]['bookGenres']:
                            genres_list.append(k['genre']['name'])
        five_stars = int(
            (re.match(r'^[\d,]*', self.bs.find('div', {'data-testid': 'labelTotal-5'}).get_text()).group()).replace(',',
                                                                                                                    ''))
        four_stars = int(
            (re.match(r'^[\d,]*', self.bs.find('div', {'data-testid': 'labelTotal-4'}).get_text()).group()).replace(',',
                                                                                                                    ''))
        three_stars = int(
            (re.match(r'^[\d,]*', self.bs.find('div', {'data-testid': 'labelTotal-3'}).get_text()).group()).replace(',',
                                                                                                                    ''))
        two_stars = int(
            (re.match(r'^[\d,]*', self.bs.find('div', {'data-testid': 'labelTotal-2'}).get_text()).group()).replace(',',
                                                                                                                    ''))
        one_star = int(
            (re.match(r'^[\d,]*', self.bs.find('div', {'data-testid': 'labelTotal-1'}).get_text()).group()).replace(',',
                                                                                                                    ''))
        return [work_id, book_title, author_name, rating, rating_count, reviews_count, five_stars, four_stars, three_stars,
                two_stars, one_star, genres_list]

    def series(self):
        series_name = self.bs.find('h3', attrs={'class': 'Text Text__title3 Text__italic Text__regular Text__subdued'})
        if series_name is not None:
            series_name = series_name.get_text()
        # series_link = self.bs.find('h3', attrs={'class': 'Text Text__title3 Text__italic Text__regular Text__subdued'})
        # if series_link is not None:
        #     series_link = series_link.find('a').attrs['href']
        return series_name

    def description_data(self):
        description = self.bs.find('div', class_='DetailsLayoutRightParagraph__widthConstrained')
        if description is not None:
            description = description.get_text()
        return description

    def pages_date_data(self):
        nb_pages = self.bs.find('p', {'data-testid': 'pagesFormat'})
        if nb_pages is not None:
            try:
                nb_pages = int(re.match(r'^\d+', nb_pages.get_text()).group())
            except AttributeError:
                nb_pages = None
        published = self.bs.find('p', {'data-testid': 'publicationInfo'})
        if published is not None:
            published = re.sub('(First published )|(Published )', '', published.get_text())
            try:
                published = datetime.strptime(published, '%B %d, %Y')
            except:
                published = None
        return [nb_pages, published]

    def awards_data(self):
        awards = self.bs.find('script', id='__NEXT_DATA__')
        if awards is not None:
            awards = json.loads(awards.get_text())
            awards = awards['props']['pageProps']['apolloState']
            for j in awards.keys():
                if 'Work:kca' in j:
                    award_list = []
                    for award in awards[j]['details']['awardsWon']:
                        award_list.append(award['name'])
                    return award_list
        return [None]


# %%
async def review_downloader(response, book_index):
    print(book_index)
    conn = await asyncpg.connect(database='goodreads_db', user='postgres', password='root', host='localhost')
    try:
        for i in response['data']['getReviews']['edges']:
            await conn.execute('insert into review_data(book_index, review_rating, review) values ($1, $2, $3);',
           book_index, i['node']['rating'], i['node']['text'])
    except asyncpg.exceptions.UniqueViolationError as e:
        print(e)
    await conn.close()


async def get_reviews(book_index):
    proxy = get_rn_proxy(proxies_list, authenticators)
    html = httpx.get(f'https://www.goodreads.com/book/show/{book_index}', timeout=10, proxy=proxy).text
    bs = BeautifulSoup(html, 'html.parser')
    work_id = json.loads(bs.find('script', id='__NEXT_DATA__').get_text())
    work_id = work_id['props']['pageProps']['apolloState'].keys()
    for i in work_id:
        if 'Work:kca:' in i:
            work_id = i

    body = {f"operationName": "getReviews", "variables": {"filters": {"resourceType": "WORK",
                                                                      "resourceId": f"{work_id[5:]}"},
                                                          "pagination": {"limit": 30}},
            "query": "query getReviews($filters: BookReviewsFilterInput!, $pagination: PaginationInput) {\n  getReviews(filters: $filters, pagination: $pagination) {\n    ...BookReviewsFragment\n    __typename\n  }\n}\n\nfragment BookReviewsFragment on BookReviewsConnection {\n  totalCount\n  edges {\n    node {\n      ...ReviewCardFragment\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    prevPageToken\n    nextPageToken\n    __typename\n  }\n  __typename\n}\n\nfragment ReviewCardFragment on Review {\n  __typename\n  id\n  creator {\n    ...ReviewerProfileFragment\n    __typename\n  }\n  recommendFor\n  updatedAt\n  createdAt\n  spoilerStatus\n  lastRevisionAt\n  text\n  rating\n  shelving {\n    shelf {\n      name\n      webUrl\n      __typename\n    }\n    taggings {\n      tag {\n        name\n        webUrl\n        __typename\n      }\n      __typename\n    }\n    webUrl\n    __typename\n  }\n  likeCount\n  viewerHasLiked\n  commentCount\n}\n\nfragment ReviewerProfileFragment on User {\n  id: legacyId\n  imageUrlSquare\n  isAuthor\n  ...SocialUserFragment\n  textReviewsCount\n  viewerRelationshipStatus {\n    isBlockedByViewer\n    __typename\n  }\n  name\n  webUrl\n  contributor {\n    id\n    works {\n      totalCount\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SocialUserFragment on User {\n  viewerRelationshipStatus {\n    isFollowing\n    isFriend\n    __typename\n  }\n  followersCount\n  __typename\n}\n"}

    # proxy = get_rn_async_proxy(proxies_list, authenticators)
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=0.5, max=5),
           retry=retry_if_exception_type(httpx.HTTPError), reraise=True)
    async def request(body):
        async with httpx.AsyncClient(mounts=get_rn_async_proxy(proxies_list, authenticators)) as client:
            response = json.loads(
            (await client.post('https://kxbwmqov6jgg3daaamb744ycu4.appsync-api.us-east-1.amazonaws.com/graphql',
                     json=body,
                     headers={'X-Api-Key': 'da2-xpgsdydkbregjhpr6ejzqdhuwy'}, timeout=10)).text)
        return response

    response = (await request(body))
    next_page_token = response['data']['getReviews']['pageInfo']['nextPageToken']

    asyncio.create_task(review_downloader(response, book_index))


    while next_page_token != '':
        print(next_page_token)
        body = {f"operationName": "getReviews", "variables": {"filters": {"resourceType": "WORK",
                                                                          "resourceId": f"{work_id[5:]}"},
                                                              "pagination": {"limit": 30}},
                "query": "query getReviews($filters: BookReviewsFilterInput!, $pagination: PaginationInput) {\n  getReviews(filters: $filters, pagination: $pagination) {\n    ...BookReviewsFragment\n    __typename\n  }\n}\n\nfragment BookReviewsFragment on BookReviewsConnection {\n  totalCount\n  edges {\n    node {\n      ...ReviewCardFragment\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    prevPageToken\n    nextPageToken\n    __typename\n  }\n  __typename\n}\n\nfragment ReviewCardFragment on Review {\n  __typename\n  id\n  creator {\n    ...ReviewerProfileFragment\n    __typename\n  }\n  recommendFor\n  updatedAt\n  createdAt\n  spoilerStatus\n  lastRevisionAt\n  text\n  rating\n  shelving {\n    shelf {\n      name\n      webUrl\n      __typename\n    }\n    taggings {\n      tag {\n        name\n        webUrl\n        __typename\n      }\n      __typename\n    }\n    webUrl\n    __typename\n  }\n  likeCount\n  viewerHasLiked\n  commentCount\n}\n\nfragment ReviewerProfileFragment on User {\n  id: legacyId\n  imageUrlSquare\n  isAuthor\n  ...SocialUserFragment\n  textReviewsCount\n  viewerRelationshipStatus {\n    isBlockedByViewer\n    __typename\n  }\n  name\n  webUrl\n  contributor {\n    id\n    works {\n      totalCount\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SocialUserFragment on User {\n  viewerRelationshipStatus {\n    isFollowing\n    isFriend\n    __typename\n  }\n  followersCount\n  __typename\n}\n"}

        if next_page_token is not None:
            body['variables']['pagination']['after'] = next_page_token

        response = await request(body)

        asyncio.create_task(review_downloader(response, book_index))
        next_page_token = response['data']['getReviews']['pageInfo']['nextPageToken']


# %%
async def book_downloader(bookpage: BookPage, conn):
    if bookpage.book_check() is not None:
        logger.info(msg=f'{bookpage.book_index} book is empty')
    else:
        try:
            data = bookpage.book_data()
            await conn.execute('insert into book_data (site_index, work_id, book_name, author, rating, nb_ratings, nb_reviews, nb_5_stars, nb_4_stars, nb_3_stars, nb_2_stars, nb_1_stars, genres, series_name, description, nb_pages, publication_date, awards) '
                               'values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, ($13), $14, $15, $16, $17, ($18));',
                               bookpage.book_index, data[0], data[1], data[2],
                               data[3],
                               data[4],
                               data[5], data[6], data[7],
                               data[8],
                               data[9],
                               data[10], data[11], bookpage.series(),
                               bookpage.description_data(),
                               bookpage.pages_date_data()[0], bookpage.pages_date_data()[1], bookpage.awards_data())
            logger.info(msg=f'{bookpage.book_index} was downloaded successfully')
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f'Book_index: {bookpage.book_index} | Postgres DB error: | {e}')
        except AttributeError as ae:
            logger.error(f'{ae} | {bookpage.book_index}')
        except Exception as e1:
            logger.error(f'Book_index: {bookpage.book_index}| Неизвестная ошибка: | {e1}')



async def db_insert_book(x1, x2):
    lost_books = []
    for i in range(x1, x2 + 1, 50):
        proxy = await get_rn_async_proxy(proxies_list, authenticators)
        async with httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(proxy=proxy), follow_redirects=True,
                                     headers=headers) as client:
            coros = [BookPage.create(j, proxy, client) for j in range(i, i + (min(50, x2 + 1 - i)))]
            for coro in asyncio.as_completed(coros):
                bookpage = await coro
                if isinstance(bookpage, tuple):
                    lost_books.append(bookpage[1])
                    logger.info(msg=f'Request problem with book {bookpage[1]}')
                    continue

                conn = await asyncpg.connect(database='goodreads_db', user='postgres', password='root', host='localhost',
                                             max_cacheable_statement_size=0, max_cached_statement_lifetime=0)
                # async with asyncpg.connect(database='goodreads_db', user='postgres', password='root', host='localhost',
                #                              max_cacheable_statement_size=0, max_cached_statement_lifetime=0) as conn:
                await book_downloader(bookpage, conn)
                await conn.close()
    logger.info(lost_books)

# %%
def books_downloader(index_tuple: tuple[int]):
    asyncio.run(db_insert_book(index_tuple[0], index_tuple[1]))

def extract_books(indexes_list: list[tuple[int, int]]):
    start_time = time.time()
    with futures.ThreadPoolExecutor() as executor:
        executor.map(books_downloader, indexes_list)
    print(f'Execution time: {time.time() - start_time}')

#%%
def reviews_downloader(index: int):
    asyncio.run(get_reviews(index))

def extract_reviews(index_list: [int]):
    start_time = time.time()
    with futures.ThreadPoolExecutor() as executor:
        executor.map(reviews_downloader, index_list)
    print(f'Execution time: {time.time() - start_time}')

#%%
from math import ceil
def tupler(x1, x2, n):
    tuples = []
    step = ceil((x2 - x1) / n)
    for i in range(n):
        tuples.append((x1, x1 + step))
        x1 += step
    return tuples

#%%
# extract_reviews([69, 29])


#%%
extract_books(tupler(4_500_000, 4_900_000 , 10))

