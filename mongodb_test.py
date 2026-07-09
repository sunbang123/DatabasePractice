import requests
from pymongo import MongoClient

ACCESS_TOKEN = ":) 비밀이용"

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017")
db = client["movie_db"]          # 데이터베이스 이름 (없으면 자동 생성됨)
collection = db["top_rated_movies"]  # 컬렉션 이름 (없으면 자동 생성됨)


def get_runtime_and_certification(movie_id):
    detail_res = requests.get(f"{BASE_URL}/movie/{movie_id}", headers=HEADERS, params={"language": "ko-KR"})
    detail = detail_res.json()
    runtime_minutes = detail.get("runtime")

    cert_res = requests.get(f"{BASE_URL}/movie/{movie_id}/release_dates", headers=HEADERS)
    cert_data = cert_res.json()

    pg_level = None
    for entry in cert_data.get("results", []):
        if entry["iso_3166_1"] == "US":
            for release in entry["release_dates"]:
                if release.get("certification"):
                    pg_level = release["certification"]
                    break
            break

    return runtime_minutes, pg_level


def insert_all():
    all_movies = []

    for page in range(1, 6):
        res = requests.get(
            f"{BASE_URL}/movie/top_rated",
            headers=HEADERS,
            params={"language": "ko-KR", "page": page}
        )
        data = res.json()
        movies = data.get("results", [])
        all_movies.extend(movies)

    print(f"총 {len(all_movies)}개 영화 수집")

    for movie in all_movies:
        title = movie["title"]

        release_date = movie.get("release_date")
        if not release_date:
            continue
        released_year = int(release_date.split("-")[0])

        running_time_minutes, pg_level = get_runtime_and_certification(movie["id"])

        if running_time_minutes is None:
            running_time_minutes = 0
        if pg_level is None:
            pg_level = "정보없음"

        movie_doc = {
            "tmdb_id": movie["id"],
            "title": title,
            "released_year": released_year,
            "running_time_minutes": running_time_minutes,
            "pg_level": pg_level,
            "vote_average": movie.get("vote_average"),
        }

        # tmdb_id 기준으로 있으면 업데이트, 없으면 새로 삽입 (중복 저장 방지)
        collection.update_one(
            {"tmdb_id": movie["id"]},
            {"$set": movie_doc},
            upsert=True
        )

        print("저장 완료", title, released_year, running_time_minutes, pg_level)

    print(f"\n총 {collection.count_documents({})}개 문서가 DB에 저장되어 있습니다.")


if __name__ == '__main__':
    insert_all()