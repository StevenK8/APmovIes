import main
import asyncio

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

async def test_post_comment()

    
asyncio.run(test_movie_rating())
asyncio.run(test_movie_rating_imdb())
asyncio.run(test_movie_rating_tmdb())
asyncio.run(test_movie_rating_metacritic())




