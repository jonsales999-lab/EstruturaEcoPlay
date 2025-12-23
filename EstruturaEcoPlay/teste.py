import requests

# token obtido do login
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MCIsImV4cCI6MTc2NjYzNDkwMn0.0mMbSroFSHPgAZXQly-5J_AnUGPffQlWzRRW1Zpkk34"

# Envie os headers como um dicionário; o Authorization deve usar o esquema Bearer
headers = {
    "Authorization": f"Bearer {token}"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao.status_code)
try:
    print(requisicao.json())
except ValueError:
    print(requisicao.text)