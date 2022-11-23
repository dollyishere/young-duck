# 데이터를 받아 json 파일에 저장하는 코드

import requests
import json

# API 키 변수형태로 저장
TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_movies_id_datas():
    total_data = []


    # popular
    for i in range(1, 150):
        request_url = 'https://api.themoviedb.org/3/movie/popular?api_key={}&language=ko-KR&page={}'.format(TMDB_API_KEY, i)
        
        popular_movies = requests.get(request_url).json()

        for popular_movie in popular_movies['results']:
            if popular_movie.get('release_date', ''):
                total_data.append(popular_movie['id'])

    # top_rated
    for i in range(1, 150):
        request_url = 'https://api.themoviedb.org/3/movie/popular?api_key={}&language=ko-KR&page={}'.format(TMDB_API_KEY, i)

        top_rated_movies = requests.get(request_url).json()

        for top_rated_movie in top_rated_movies['results']:
            if top_rated_movie.get('release_date', ''):
                # 만약 id가 중복될 경우(같은 영화가 있을 경우)를 if문으로 검증한 후 추가해줌
                if top_rated_movie['id'] not in total_data:
                    total_data.append(top_rated_movie['id'])
        
    json_data = {
        "name": "movie id list",
        "data": total_data
    }

    with open("movie_id_list.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\t", ensure_ascii=False)


get_movies_id_datas()