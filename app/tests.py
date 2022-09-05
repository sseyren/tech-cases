from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate, RequestsClient, APIRequestFactory

from .models import Company, CompanyType
from .views import CompanyFollowView, FollowingCompanyListView

User = get_user_model()


class GeneralTestCase(TestCase):

    def setUp(self):
        c1 = Company(name="Turkish Airlines", type=CompanyType.CORP, country='TR')
        c2 = Company(name="The Boring Company", type=CompanyType.CORP, country='US')
        c3 = Company(name="Özgür Yazılım Derneği", type=CompanyType.SCO, country='TR')
        c4 = Company(name="Serhat Danışmanlık", type=CompanyType.SOLE, country='GE')
        c1.save(), c2.save(), c3.save(), c4.save()
        self.companies = [c1, c2, c3, c4]

        u1 = User(username="user1")
        u2 = User(username="user2")
        u1.save(), u2.save()
        self.users = [u1, u2]

        self.client = RequestsClient()

    def test_list_companies(self):
        resp = self.client.get('http://test/api/company/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        content = resp.json()
        self.assertEqual(len(content), 4)

    def test_create_company(self):
        resp = self.client.post('http://test/api/company/',
                                {'name': 'test', 'type': 'asdf', 'country': 'TR'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post('http://test/api/company/',
                                {'name': 'test', 'type': 'sme', 'country': 'TR'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 5)

    def test_update_company(self):
        company = self.companies[3]
        resp = self.client.patch('http://test/api/company/4/',
                                 {'country': 'ASDF'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.patch('http://test/api/company/4/',
                                 {'country': 'TR'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        company.refresh_from_db()
        self.assertEqual(company.country.code, 'TR')

    def test_delete_company(self):
        company = self.companies[3]
        resp = self.client.delete('http://test/api/company/31/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.delete('http://test/api/company/4/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Company.DoesNotExist):
            company.refresh_from_db()

    def test_auth_views(self):
        resp = self.client.get('http://test/api/company/4/follow/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        resp = self.client.get('http://test/api/company/followings/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_company(self):
        user = self.users[0]
        factory = APIRequestFactory()

        # initially this should be False
        req = factory.get('/api/company/1/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['follow'], False)

        # user decides to follow a company
        req = factory.post('/api/company/1/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # this should be True now
        req = factory.get('/api/company/1/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['follow'], True)

        # but for another company still False
        req = factory.get('/api/company/2/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=2)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['follow'], False)

        # user unfollows this company
        req = factory.delete('/api/company/1/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # this should be False now
        req = factory.get('/api/company/1/follow/')
        force_authenticate(req, user=user)
        resp = CompanyFollowView.as_view()(req, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['follow'], False)

    def test_follow_list(self):
        factory = APIRequestFactory()
        self.companies[0].likes.add(self.users[0])
        self.companies[1].likes.add(self.users[0])
        self.companies[2].likes.add(self.users[0])
        self.companies[3].likes.add(self.users[1])

        # user[0] has 3
        req = factory.get('/api/company/followings/')
        force_authenticate(req, user=self.users[0])
        resp = FollowingCompanyListView.as_view()(req)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 3)

        # user[1] has 1
        req = factory.get('/api/company/followings/')
        force_authenticate(req, user=self.users[1])
        resp = FollowingCompanyListView.as_view()(req)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

        # new user has nothing
        new_user = User(username="new-user")
        new_user.save()
        req = factory.get('/api/company/followings/')
        force_authenticate(req, user=new_user)
        resp = FollowingCompanyListView.as_view()(req)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)
