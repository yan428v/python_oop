from requests import get, post
from urllib import parse

posts = get(
    'https://jsonplaceholder.typicode.com/posts'
)
print(posts.json())

for i, post in enumerate(posts.json()):
    if i >= 5:
        break
    print(f"заголовок: {post['title']}\nтело {post['body']}\n")



town = str(input())

response = get(
    f'https://api.openweathermap.org/data/2.5/weather?q={town}&appid=d5a8c7f1475195aec2cd19c63dd2c5bf'
)

print(response.json())

data = {   "title": 'foo', "body": 'bar', 'userId': 1}

try:
    requests = post(
        'https://jsonplaceholder.typicode.com/posts',
        json=data,
        headers= {'Content-type': 'application/json; charset=UTF-8'}
    )

    if requests.status_code == 400:
            print("нет ответа от сервера")
    elif requests.status_code == 404:
        print("страница не найдена")
    else:
        print(requests.json())

except ConnectionError:
    print("ошибка подключения")
except TimeoutError:
    print('превышено время ожидания')


