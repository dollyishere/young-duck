# api genre data change json

import requests
import json


TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_genre_datas():
    total_data = []

    # 1페이지부터 500페이지까지의 데이터를 가져옴.
    request_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=ko-KR'.format(TMDB_API_KEY)
    
    genres = requests.get(request_url).json()

    for genre in genres['genres']:
        data = {
            "model" : "movies.genre",
            'pk' : genre['id'],
            'fields' : {
                "name" : genre['name']
            }
        }
    
        total_data.append(data)       
    print(total_data)
    json_data = total_data

    with open("genre_list.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\t", ensure_ascii=False)


get_genre_datas()