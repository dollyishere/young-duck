# Final Project

# 목차

1. 프로젝트 목표 소개
2. 팀원 정보 및 업무 분담 내역
3. 사용한 개발 도구 및 라이브러리
4. 데이터베이스 모델링(ERD), Fixture, URL, View
5. 목표 서비스 구현 및 실제 구현 정도
6. 서비스 대표 기능 설명
7. 각 apps 및 기능에 대한 설명
8. 영화 추천 알고리즘 설명
9. 프로젝트 후기

## 1. 프로젝트 목표 소개

알고리즘을 기반으로 한 영화 추천 서비스

(SSAFY 8기 1학기 최종 프로젝트)

## 2. 팀원 정보 및 업무 분담 내역

* Frontend: 유한별
  * html, css, js을 비롯한 전반적인 FE 관련 업무 수행
  * 사이트 및 로고 디자인 담당
  * 사이트 기능 구상, 목록 정리 및 작성
* Backend: 임주연
  * BD 및 프로젝트 app, model 구조 설계
  * Django를 통한 기능 구현, python과 API를 통한 데이터 파싱 등 전반적인 BE 관련 업무 수행
  * README를 비롯하여 대부분의 기록을 담당

## 3. 사용한 개발 도구 및 라이브러리

* Main(필수 개발 환경 관련)
  * Python 3.9+
  * Django 3.2.x
  * Vanilla JS
* 사용 도구
  * Visual Studio Code
  * Chrome Brower
* 사용한 API
  * TMDB API
    * [TMDB API offical site](https://developers.themoviedb.org/3/getting-started/introductionhttps:/)
* django & python 관련 라이브러리
  * Pillow (django 이미지 관리 툴)
  * requests (API 요청)
  * colorthief (movie backdrop 이미지 색깔 팔레트 추출)
    * [official github](https://https://github.com/fengsp/color-thief-py)
    * [how to use?](https://stackoverflow.com/questions/13811483/getting-dominant-color-of-an-image)
* 사용한 이미지 출처
  * icon default image : flaticon
    * [flaticon-free-stickers](https://www.flaticon.com/free-stickers/emoji?k=1668995263574&log-in=googlehttps:/)
  * book cover default image: pixabay
    * [pixabay](https://pixabay.com/ko/https:/)

## 4. 데이터베이스 모델링(ERD), Fixture, URL, View

### - 데이터베이스 모델링(ERD)

![ERD](./README_img/ERD.png)

### - Fixture

* DB 내에서 사용되는 fixture 파일은 movies 앱 내에 위치합니다.
* fixture data의 load는 반드시 모델 정의(makemigrations) 및 migrate 이후에 직접 진행합니다.
* 이하의 순서대로 loaddata를 진행합니다(genre_list.json과 credit_list.json의 순서는 바뀌어도 무방함).

  1. `python manage.py loaddata genre_list.json`(model genre)
  2. `python manage.py loaddata credit_list.json`(model people)
  3. `python manage.py loaddata movie_list.json`(model movie)

### - URL

##### (1) movies


| URL 패턴                    | 역할                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------ |
| /movies/<movie_pk>/         | 단일 영화 상세 페이지 조회                                                   |
| /movies/person/<person_pk>/ | 인물 상세 페이지 조회                                                        |
| /movies/recommended/        | 추천 영화 페이지 조회                                                        |
| /movies/search/             | 키워드 기반 영화 관련 정보(movie, people, genre, book) 검색 결과 페이지 조회 |
| /movies/search/             | 영화 디테일 페이지에서 카드 생성 시, 테마북 검색 및 선택 페이지 조회         |

##### (2) books


| URL 패턴                                  | 역할                                                                                                                                               |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| /books/                                   | 사용자 본인 및 다른 사용자가 제작한 테마북 목록 페이지 조회 ⇒ 메인화면으로서, home과 같은 역할 수행(로그인한 사용자가 가장 먼저 보게 되는 페이지) |
| /books/create/                            | 새로운 테마북 생성 페이지 조회 & 단일 테마북 데이터 저장                                                                                           |
| /books/<book_pk>/detail/                  | 단일 테마북 상세 페이지 조회                                                                                                                       |
| /books/<book_pk>/update/                  | 테마북 데이터 수정 페이지 조회 & 단일 테마북 데이터 수정                                                                                           |
| /books/<book_pk>/delete/                  | 단일 테마북 데이터 삭제                                                                                                                            |
| /books/<book_pk>/like/                    | 단일 테마북 데이터 삭제                                                                                                                            |
| /books/cards/create/<book_pk>/<movie_pk>/ | 새로운 카드 생성 페이지 조회 & 단일 카드 데이터 저장                                                                                               |
| /books/cards/<card_pk>/                   | 단일 카드 상세 페이지 조회                                                                                                                         |
| /books/cards/<card_pk>/update/            | 카드 데이터 수정 페이지 조회 & 단일 카드 데이터 수정                                                                                               |
| /books/cards/<card_pk>/delete/            | 단일 카드 데이터 삭제                                                                                                                              |
| /books/<book_pk>/select/                  | 카드 생성 혹은 테마북에 기존 카드 추가 시, 카드를 만들기를 원하는 영화 검색 및 선택 페이지 조회                                                    |
| /books/<book_pk>/steal/                   | 다른 유저가 생성한 테마북과 그 하위 카드 데이터를 바탕으로 내 테마북 & 카드를 생성                                                                 |

##### (3) accounts


| URL 패턴                                       | 역할                                                                  |
| ------------------------------------------------ | ----------------------------------------------------------------------- |
| /accounts/signup/                              | 회원 생성 페이지 조회 & 단일 회원 데이터 생성 (회원 가입)             |
| /accounts/login/                               | 로그인 페이지 조회 & 세션 데이터 생성 및 저장 (로그인)                |
| /accounts/logout/                              | 세션 데이터 삭제 (로그아웃)조회                                       |
| /accounts/delete/                              | 단일 회원 데이터 삭제 (회원탈퇴)                                      |
| /accounts/password/                            | 비밀번호 수정 페이지 조회 & 단일 비밀번호 데이터 수정 (비밀번호 변경) |
| /accounts/search/                              | 사용자 검색 페이지 조회                                               |
| /accounts/[str:username](str:username)/        | 단일 사용자 상세 조회 페이지 (프로필 조회) ⇒ detail                  |
| /accounts/[str:username](str:username)/update/ | 단일 사용자 프로필 수정 페이지 조회                                   |
| /accounts/<user_pk>/follows/                   | 단일 사용자 팔로우 기능(비동기)                                       |

### - View

##### (1) movies


| **View 함수명** | **역할**                                                                        | **허용 HTTP Method** |
| :---------------- | :-------------------------------------------------------------------------------- | ---------------------- |
| detail          | 단일 영화 상세 페이지 조회                                                      | GET                  |
| detail_person   | 단일 인물 상세 페이지 조회                                                      | GET                  |
| recommended     | 알고리즘 기반 추천 영화 페이지 조회                                             | GET                  |
| search          | 영화 검색 페이지 조회                                                           | GET                  |
| select_book     | 영화 상세 페이지에서 카드 생성 시, 카드를 만들기 원하는 테마북 선택 페이지 조회 | GET                  |

##### (2) books


| **View 함수명** | **역할**                                                                         | **허용 HTTP Method** |
| :---------------- | :--------------------------------------------------------------------------------- | ---------------------- |
| index           | 테마북 목록 페이지 조회(home)                                                    | GET                  |
| create          | 새로운 테마북 생성 페이지 조회 & 단일 테마북 데이터 저장                         | GET & POST           |
| detail          | 단일 테마북 상세 페이지 조회                                                     | GET                  |
| update          | 단일 테마북 데이터 수정 페이지 조회 & 단일 테마북 데이터 수정                    | GET & POST           |
| delete          | 단일 테마북 데이터 삭제                                                          | POST                 |
| like            | 단일 테마북 좋아요 & 좋아요 취소 기능(비동기)                                    | POST                 |
| create_card     | 새로운 카드 생성 페이지 조회 & 단일 카드 데이터 저장                             | GET & POST           |
| detail_card     | 단일 카드 상세 페이지 조회                                                       | GET                  |
| update_card     | 단일 카드 데이터 수정 페이지 조회 & 단일 카드 데이터 수정                        | GET & POST           |
| delete_card     | 단일 카드 데이터 수정 페이지 조회 & 단일 카드 데이터 수정                        | POST                 |
| select_movie    | 테마북 상세 페이지에서 카드 제작 시, 원하는 영화 검색 및 선택                    | GET & POST           |
| steal_book      | 다른 유저가 생성한 테마북과 그 하위 카드 데이터를 바탕으로 내 테마북&카드를 생성 | POST                 |

##### (3) accounts


| **View 함수명** | **역할**                                                              | **허용 HTTP Method** |
| :---------------- | :---------------------------------------------------------------------- | ---------------------- |
| signup          | 회원 생성 페이지 조회 & 단일 회원 데이터 생성 (회원 가입)             | GET                  |
| login           | 로그인 페이지 조회 & 세션 데이터 생성 및 저장 (로그인)                | GET & POST           |
| logout          | 세션 데이터 삭제 (로그아웃)                                           | POST                 |
| update          | 회원 수정 페이지 조회 & 단일 회원 데이터 수정 (회원 정보 수정)        | GET & POST           |
| delete          | 단일 회원 데이터 삭제 (회원탈퇴)                                      | POST                 |
| change_password | 비밀번호 수정 페이지 조회 & 단일 비밀번호 데이터 수정 (비밀번호 변경) | GET & POST           |
| profile         | 사용자 상세 조회 페이지 (프로필 조회)                                 | GET                  |
| update_profile  | 사용자 프로필 수정 페이지 조회 및 단일 사용자 프로필 수정             | GET & POST           |
| follow          | 사용자 팔로우 기능                                                    | POST                 |
| search          | 사용자 검색 기능                                                      | GET & POST           |
