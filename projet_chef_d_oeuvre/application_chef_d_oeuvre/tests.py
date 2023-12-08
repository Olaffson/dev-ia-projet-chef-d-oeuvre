import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

# Create your tests here.


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


@pytest.mark.django_db
def test_logout_user(user):
    client = Client()
    client.login(username='testuser', password='12345')

    url = reverse('logout')  # Assurez-vous que 'logout' est le nom de l'URL de votre vue de déconnexion
    response = client.get(url)

    # Vérifiez si l'utilisateur est déconnecté et redirigé
    assert response.status_code == 302  # Redirection après déconnexion
    assert '_auth_user_id' not in client.session  # L'ID utilisateur ne doit pas être dans la session


@pytest.mark.django_db
def test_failed_login():
    client = Client()
    url = reverse('login')
    response = client.post(url, {'username': 'wronguser', 'password': 'wrongpass'})

    # Vérifiez si la connexion a échoué
    assert response.status_code == 200  # Pas de redirection, reste sur la page de connexion
    assert 'Identifiants invalides.' in response.content.decode()
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_signup_page():
    client = Client()
    url = reverse('signup')
    user_data = {
        'username': 'newuser',
        'password1': 'newpass123',
        'password2': 'newpass123',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com'
    }
    response = client.post(url, user_data)

    # Vérifiez si le nouvel utilisateur est créé et redirigé
    assert response.status_code == 302  # Redirection après une inscription réussie
    assert User.objects.filter(username='newuser').exists()  # L'utilisateur a été créé


@pytest.mark.django_db
def test_signup_page_failure():
    client = Client()
    url = reverse('signup')
    response = client.post(url, {'username': 'testuser', 'password1': 'short', 'password2': 'short'})

    # Assurez-vous que la réponse est celle attendue
    assert response.status_code == 200

    # Vérifiez si le formulaire retourné contient des erreurs
    assert 'form' in response.context
    form = response.context['form']
    assert form.errors  # Vérifiez que le formulaire contient des erreurs
