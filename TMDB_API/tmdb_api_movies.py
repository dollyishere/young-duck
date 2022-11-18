# # api movie_id(popular, top_rated) data change json
import requests
import json


TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_movie_datas():
    total_data = []
    cnt = 0

    # 1페이지부터 500페이지까지의 데이터를 가져옴.
    for i in range(1, 10):
        
        request_url = 'https://api.themoviedb.org/3/movie/popular?api_key={}&language=ko-KR&page={}'.format(TMDB_API_KEY, i)
        
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('release_date', ''):
                cnt += 1
                data = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids']
                }

                # Movie 모델 필드명에 맞추어 데이터를 저장함.
                credit_request_url = 'https://api.themoviedb.org/3/movie/{}/credits?api_key={}&language=ko-KR'.format(movie['id'],TMDB_API_KEY)

                credits = requests.get(credit_request_url).json()
                
                if len(credits['cast']) > 0:
                    cast_list = []
                    for cast in credits['cast']:
                        cast_list.append(cast['id'])
                    data['cast'] = cast_list
                
                if len(credits['crew']) > 0:
                    crew_list = []
                    for crew in credits['crew']:
                        crew_list.append(crew['id'])
                data['crew'] = crew_list
                
            total_data.append(data)

    json_data = {
        total_data
    }

    with open("movie_data.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\t", ensure_ascii=False)


get_movie_datas()