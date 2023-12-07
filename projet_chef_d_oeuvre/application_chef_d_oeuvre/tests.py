import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

# Create your tests here.


# @pytest.fixture
# @pytest.mark.django_db  # Activer l'accès à la base de données pour cette fixture
# def user():
#     return User.objects.create_user(username='testuser', password='12345')


@pytest.fixture
@pytest.mark.django_db
def user():
    # Créer un utilisateur de test avec un first_name
    return User.objects.create_user(username='testuser', password='12345', first_name='Test')


@pytest.mark.django_db  # Activer l'accès à la base de données pour ce test
def test_user_login(user):
    client = Client()
    url = reverse('login')  # Assurez-vous que 'login' est le nom de l'URL de votre vue de connexion
    response = client.post(url, {'username': 'testuser', 'password': '12345', 'first_name': 'Test'})
    
    # Vérifiez si la connexion a réussi
    assert response.status_code == 302  # Généralement, une redirection après une connexion réussie
    assert '_auth_user_id' in client.session  # Vérifiez si l'ID utilisateur est dans la session


@pytest.mark.django_db
def test_unregistered_user_login():
    client = Client()
    url = reverse('login')  # Assurez-vous que 'login' est le nom de l'URL de votre vue de connexion
    response = client.post(url, {'username': 'fakeuser', 'password': 'fakepassword'})

    # Vérifiez si la connexion a échoué
    assert response.status_code != 302  # Une connexion réussie redirige généralement l'utilisateur
    assert '_auth_user_id' not in client.session  # L'ID utilisateur ne doit pas être dans la session


@pytest.mark.django_db
def test_index_view_with_authenticated_user(user):
    client = Client()
    client.login(username='testuser', password='12345')

    url = reverse('index')  # Assurez-vous que 'index' est le nom de l'URL de votre vue index
    response = client.get(url)

    # Vérifiez si le prénom de l'utilisateur est affiché
    assert response.status_code == 200
    assert 'Bonjour, Test !' in response.content.decode()
