# api people data change json
import requests
import json


TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_people_datas():
    people_id_data = []


    for i in range(1, 300):
        request_url = 'https://api.themoviedb.org/3/person/popular?api_key={}&language=ko-KR&page={}'.format(TMDB_API_KEY, i)
    
        people = requests.get(request_url).json()
        
        for person in people["results"]:
            people_id_data.append(person["id"])       


    people_id_data = {
        "name" : "people id list",
        "data" : people_id_data,
    }

    
    with open("people_id_list.json", "w", encoding="utf-8") as w:
        json.dump(people_id_data, w, indent="\t", ensure_ascii=False)


get_people_datas()