from datetime import date
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
    assert isinstance(postResult["comment"],str)
    assert 0 <= postResult["rate"] <= float('inf') 





#On peut récupérer les notes de films depuis imdb, tmdb, metacritic ...
# ... la moyenne des 3 et voir les tops sans être connecté
print(main.get_movie_rating_imdb("Cars"))
print(main.get_movie_rating_tmdb("Cars"))
print(main.get_movie_rating_metacritic("Cars"))
print(main.get_movie_rating_api("Cars"))
print(main.get_top_rating())

#On créé un user --> renvoie son apikey
apikey = asyncio.run(main.create_user("test"))

#le user commente 2 films : Avatar et Cars
#Il commente 3 fois avatar : une fois avec la note de 5.5, 
#une autre fois avec la note de 11 puis avec la note de 7
#11 ça ne passe pas car c'est supérieur à 10
#Le 5.5 est écrasé par le 7 (détection du même user même film)
asyncio.run(main.post_comment(apikey,"Avatar", 5.5, "film très cool"))
asyncio.run(main.post_comment(apikey,"Avatar", 11, "film très cool"))
asyncio.run(main.post_comment(apikey,"Avatar", 7, "film très cool"))
asyncio.run(main.post_comment(apikey,"Cars", 8, "J'ai adoré"))

#Il commente un film qui n'existe pas
asyncio.run(main.post_comment(apikey,"gfgfgfgfgfgf", 5.5, "film très cool"))
#Il récupère SES commentaires et on remarque qu'il n'y a que le dernier comm Avatar et le comm Cars
print(main.get_mycomments(apikey))


#Il regarde tous les commentaires du film Avatar: il y en a un autre qui ne lui appartient pas
print(asyncio.run(main.get_comments("Avatar")))

#Il supprime son commentaire
#asyncio.run(main.delete_comment(apikey,"Cars"))

#On supprime le user
asyncio.run(main.delete_user(apikey))










    
#asyncio.run(test_movie_rating())
#asyncio.run(test_movie_rating_imdb())
#asyncio.run(test_movie_rating_tmdb())
#asyncio.run(test_movie_rating_metacritic())
#asyncio.run(test_post_comment())




