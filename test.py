import main
import asyncio

import configparser
CONFIG_PATH = './config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)



async def test_movie_rating():
    avatar = await main.get_movie_rating_api("Avatar")
    assert 0 <= avatar["rating"] <= float('inf')
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_imdb():
    avatar = await main.get_movie_rating_imdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_tmdb():
    avatar = await main.get_movie_rating_tmdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_metacritic():
    avatar = await main.get_movie_rating_metacritic("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert isinstance(avatar["original_title"], str)

async def test_post_comment():
    postResult = await main.post_comment("4a5fb1e7-9002-11ec-92c2-7c0507cfc855", "Avatar", "commentaire", 10)
    assert postResult["comment"] == "commentaire"
    assert postResult["rate"] == 10


    
asyncio.run(test_movie_rating())
asyncio.run(test_movie_rating_imdb())
asyncio.run(test_movie_rating_tmdb())
asyncio.run(test_movie_rating_metacritic())
asyncio.run(test_post_comment())




