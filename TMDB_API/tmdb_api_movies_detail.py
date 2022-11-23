# # api movie_detail data change json
import requests
from pprint import pprint
import json

TMDB_API_KEY = '851d868671f3d56e21c372701537e231'

def get_movie_datas(movie_list, people_id_list):
    total_data = []
    credit_data = []

    for i in range(len(movie_list)):
        movie = movie_list[i]

        movie_detail_request_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=ko-KR'.format( movie, TMDB_API_KEY)
        
        movie_detail = requests.get(movie_detail_request_url).json()
        
        # 만약 movie_detail['backdrop_path'], movie_detail['poster_path']이 null일시, ''를 대신 넣어줌
        if movie_detail['backdrop_path'] == None:
            movie_detail['backdrop_path'] = ''
        
        if movie_detail['poster_path'] == None:
            movie_detail['poster_path'] = ''

        # 해당 데이터를 집어넣을 모델의 형식에 맞춰 제작
        # model 및 pk(해당 영화의 id로 지정해 향후 쉽게 참조할 수 있게 함), 그리고 fields를 지정해줌
        data = {
            'model' : 'movies.movie',
            'pk' : movie_detail['id'],
            'fields' : {
                'title': movie_detail['title'],
                'released_date': movie_detail['release_date'],
                'popularity': movie_detail['popularity'],
                'vote_average': movie_detail['vote_average'],
                'vote_count': movie_detail['vote_count'],
                'homepage' : movie_detail['homepage'],
                'runtime' : movie_detail['runtime'],
                'status' : movie_detail['status'],
                # 'production_companies': movie_detail['production_companies'][0]['name'],
                'overview': movie_detail['overview'],
                'poster_path': movie_detail['poster_path'],
                'backdrop_path' : movie_detail['backdrop_path'],
                'budget' : movie_detail['budget'],
                'video' : '',
                'director' : '',
                'click_count' : 0,
            }
        }

        # genre의 경우 다대다 관계 테이블이기에 id만 필요하지, name은 필요하지 않음으로 따로 저장해줌
        genre_list = []
        if len(movie_detail['genres']):
            for genre in movie_detail['genres']:
                genre_list.append(genre['id'])
        data['fields']['genres'] = genre_list

        # video api request
        movie_video_request_url = 'https://api.themoviedb.org/3/movie/{}/videos?api_key={}&language=ko-KR'.format(movie, TMDB_API_KEY)

        # 영화 video의 경우 맨 처음 영상이 official인 것으로 보임(official인지 여부는 True로 판단)
        # 만약 results의 len 값이 0이라면(즉, 영상이 존재하지 않는다면=> 유튜브 api로 대체해도 되지 않을까? 차후 생각), 그냥 ''만 넣어줄 예정(string 타입의 데이터이므로)

        movie_video = requests.get(movie_video_request_url).json()

        # 되도록 offical 동영상을 넣어주는 것이 좋을 것 같다고 생각하여 검증하는 시간을 가짐
        # 위에서 불러올 때 video 값이 true이면 video api를 호출하는 방식으로 호출 횟수를 최소화하려고 했으나,
        # 해당 movie_id로 video api를 호출하였을 때 명백히 video가 존재함에도 detail video는 false로 설정되어 있는 차이를 발견하여 그냥 모두 호출해보는 것으로 진행
        # for문을 통해 결과를 돌려본 후, 만약 오피셜 비디오가 등장하면 해당 키만 넣어주고 break로 for문을 종료함
        # 그러나 만약 official 비디오가 없을 시에는, 그냥 맨 처음 비디오를 넣어줌
        if len(movie_video['results']) == 0:
            pass
            
        else:
            for video in movie_video['results']:
                if video['official'] == True:
                    data['fields']['video'] = video['key']
                    break
                # 이때 오른쪽의 ['name']을 작성하지 않아서 케이스에 걸리지 않는 이슈 수정
                elif video['name'] == movie_video['results'][-1]['name']:
                    data['fields']['video'] = movie_video['results'][0]['key']

        # credit을 불러옴
        credit_request_url = 'https://api.themoviedb.org/3/movie/{}/credits?api_key={}&language=ko-KR'.format(movie,TMDB_API_KEY)

        credits = requests.get(credit_request_url).json()
        
        # 어디까지 자를지 조금 고민 중(이대로 하면 너무 길고, 사람 풀이 너무 많아짐)
        # 아니면 popular에서 데이터 받아온 후에 대조해서 만약 거기에 id가 없으면 빼는 쪽으로 갈까?
        people_list = []
        if len(credits['cast']) > 0:
            for cast in credits['cast']:
                # pprint(cast)
                # print(cast['id'])
                if (cast['id'] in people_id_list) and (cast['id'] not in people_list):
                    people_list.append(cast['id'])
        # print(people_list)
        
        if len(credits['crew']) > 0:
            for crew in credits['crew']:
                if (crew['department'] == 'Directing'):
                    data['fields']['director'] = crew['name']
                    if crew['id'] in people_id_list:
                        people_list.append(crew['id'])
                    break
                # if crew['id'] in people_id_list:
                #     people_list.append(crew['id'])

        data['fields']['people'] = people_list

        # total_data에 지금까지 만든 영화(1편) 데이터 추가
        # credit_data에는 people_list 내부 요소들을 extend를 이용해 저장
        total_data.append(data)
        credit_data.extend(people_list)

    # pprint(total_data)
    json_data = total_data
    credit = credit_data

    with open('movie_list.json', 'w', encoding='utf-8') as w:
        json.dump(json_data, w, indent='\t', ensure_ascii=False)
    
    with open('credit.json', 'w', encoding='utf-8') as w:
        json.dump(credit, w, indent='\t', ensure_ascii=False)

# 미리 구해놨던 movie_id_list json 파일을 해당 python 코드 내부에서 사용할 수 있도록 dict 형태로 load하는 작업을 거침
movie_json = open('movie_id_list.json', encoding='utf-8')
movie_dict = json.load(movie_json)

people_json = open('people_id_list.json', encoding='utf-8')
people_dict = json.load(people_json)

get_movie_datas(movie_dict['data'], people_dict['data'])