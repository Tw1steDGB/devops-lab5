from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'no.such.user@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {'name': 'Sergey Sergeev', 'email': 's.s.sergeev@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)

    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 200
    assert response.json() == {'id': user_id, **new_user}

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json={'name': 'Other Name', 'email': users[1]['email']})
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}

    # существующий пользователь не изменился
    response = client.get("/api/v1/user", params={'email': users[1]['email']})
    assert response.json() == users[1]

def test_delete_user():
    '''Удаление пользователя'''
    new_user = {'name': 'Delete Me', 'email': 'delete.me@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201

    response = client.delete("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 204

    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 404
