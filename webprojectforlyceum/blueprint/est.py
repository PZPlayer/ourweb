from requests import post, get, delete

print(post('http://localhost:8080/api/news', json={}).json())

print(post('http://localhost:8080/api/news',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:8080/api/news',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_private': False}).json())

print(get('http://localhost:8080/api/news').json())

print(get('http://localhost:8080/api/news/1').json())

print(get('http://localhost:8080/api/news/999').json())

print(delete('http://localhost:8080/api/news/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:8080/api/news/1').json())