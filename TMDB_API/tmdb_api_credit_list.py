import requests
import json

TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_credit_datas():
    credit_list = []
    for i in credit_dict:
        # 'https://www.themoviedb.org/person/{}'.format(person.pk) 사용하면 인물 소개로 이동 가능
        request_url = 'https://api.themoviedb.org/3/person/{}?api_key={}&language=ko-KR'.format(i, TMDB_API_KEY)
        person = requests.get(request_url).json()

        if person['profile_path'] == None:
            person['profile_path'] = ''

        # if person['birthday'] == None:
        #     person['birthday'] = null

        data = {
            'model' : 'movies.people',
            'pk' : person['id'],
            'fields' : {
                'name' : person['name'],
                'birthday' : person['birthday'],
                'known_for_department' : person['known_for_department'],
                'popularity' : person['popularity'],
                'profile_path' : person['profile_path'],
                'click_count' : 0,
                }
            }
        credit_list.append(data)

    with open("credit_list.json", "w", encoding="utf-8") as w:
        json.dump(credit_list, w, indent="\t", ensure_ascii=False)


credit_json = open('credit.json', encoding='utf-8')
credit_dict = json.load(credit_json)


get_credit_datas()