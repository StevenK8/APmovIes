import main
import asyncio

import configparser
CONFIG_PATH = './config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)



async def test_movie_rating():
    avatar = main.get_movie_rating_api("Avatar")
    assert 0 <= avatar["rating"] <= float('inf')
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_imdb():
    avatar = main.get_movie_rating_imdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_tmdb():
    avatar = main.get_movie_rating_tmdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_metacritic():
    avatar = main.get_movie_rating_metacritic("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert isinstance(avatar["original_title"], str)

async def test_post_comment():
    postResult = await main.post_comment("4a5fb1e7-9002-11ec-92c2-7c0507cfc855", "Avatar", 10, "commentaire")
    assert isinstance(postResult["comment"],str)
    assert 0 <= postResult["rate"] <= float('inf') 
    
async def test_get_comments():
    comments = main.get_comments("4a5fb1e7-9002-11ec-92c2-7c0507cfc855")
    assert isinstance(comments, list)
    assert isinstance(comments[0]["comment"],str)
    assert 0 <= comments[0]["rate"] <= float('inf')
    
async def test_get_comments_movie():
    comments = main.get_comments_movie("Avatar")
    assert isinstance(comments, list)
    assert isinstance(comments[0]["comment"],str)
    assert 0 <= comments[0]["rate"] <= float('inf')


    
asyncio.run(test_movie_rating())
asyncio.run(test_movie_rating_imdb())
asyncio.run(test_movie_rating_tmdb())
asyncio.run(test_movie_rating_metacritic())
asyncio.run(test_post_comment())




