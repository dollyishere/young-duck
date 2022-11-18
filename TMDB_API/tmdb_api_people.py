# api people data change json
import requests
import json


TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_people_datas():
    total_data = []
    people_id_data = []

    # 1페이지부터 500페이지까지의 데이터를 가져옴.
    for i in range(1, 300):
        request_url = 'https://api.themoviedb.org/3/person/popular?api_key={}&language=ko-KR&page={}'.format(TMDB_API_KEY, i)
    
        people = requests.get(request_url).json()
        
        for person in people["results"]:
            data = {
                "model" : "movies.people",
                'pk' : person['id'],
                'fields' : {
                    "name" : person['name'],
                    "popularity" : person["popularity"],
                }
            }
        
            total_data.append(data)
            people_id_data.append(person["id"])       

    json_data = total_data

    people_id_data = {
        "name" : "people id list",
        "data" : people_id_data,
    }

    with open("people_list.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\t", ensure_ascii=False)
    
    with open("people_id_list.json", "w", encoding="utf-8") as w:
        json.dump(people_id_data, w, indent="\t", ensure_ascii=False)


get_people_datas()