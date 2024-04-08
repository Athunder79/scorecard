from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase,RequestFactory
from django.urls import reverse
from .models import Clubs, Round, Course, Hole, Shot
from .forms import ShotForm, RoundForm, HoleForm
from .views import start_round, scorecard, end_of_shot
from unittest.mock import patch

class StartRoundViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('start-round'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + '?next=' + reverse('start-round')) 

    def test_no_clubs_added(self):
        response = self.client.get(reverse('start-round'))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, reverse('clubs')) 

    def test_form_submission_valid(self):
        Clubs.objects.create(user=self.user, club_name='Test Club')
        course = Course.objects.create(name='Test Course')
        form_data = {'course': course.id}
        response = self.client.post(reverse('start-round'), form_data)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, reverse('hole-details', args=[course.id, Round.objects.first().id])) 

    def test_round_already_started(self):
        Clubs.objects.create(user=self.user, club_name='Test Club')
        course = Course.objects.create(name='Test Course')
        round = Round.objects.create(user=self.user, course=course)
        form_data = {'course': course.id}
        response = self.client.post(reverse('start-round'), form_data)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, reverse('hole-details', args=[course.id, round.id]))
    

class HoleDetailsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        self.club = Clubs.objects.create(user=self.user, club_name='Test Club')
        self.course = Course.objects.create(name='Test Course')
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(course=self.course, round=self.round, hole_num=1, hole_par=4, hole_distance=400)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('hole-details', args=[self.course.id, self.round.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + '?next=' + reverse('hole-details', args=[self.course.id, self.round.id])) 

    def test_invalid_course_id(self):
        response = self.client.get(reverse('hole-details', args=[self.course.id + 1, self.round.id]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_round_id(self):
        response = self.client.get(reverse('hole-details', args=[self.course.id, self.round.id + 1]))
        self.assertEqual(response.status_code, 404)

    def test_form_submission_valid(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': 400}
        response = self.client.post(reverse('hole-details', args=[self.course.id, self.round.id]), form_data)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, reverse('scorecard', args=[self.hole.id])) 

    def test_form_submission_invalid(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': 'invalid'}
        response = self.client.post(reverse('hole-details', args=[self.course.id, self.round.id]), form_data)
        self.assertEqual(response.status_code, 200) 


    def test_form_submission_invalid_negative(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': -1}


class ScorecardViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)

    def test_scorecard_view(self):
        url = reverse('scorecard', kwargs={'hole_id': self.hole.id})
        request = self.factory.get(url)
        request.user = self.user
        response = scorecard(request, hole_id=self.hole.id)
        self.assertEqual(response.status_code, 200)


class finishShotViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user',)
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)
        self.club = Clubs.objects.create(user=self.user, club_name='Test Club')
        self.shot = Shot.objects.create(user=self.user, club=self.club, course=self.course, round=self.round, hole=self.hole, shot_num_per_hole=1, latitude=40.7128, longitude=-74.0060, end_latitude=40.7128, end_longitude=-74.0060, shot_distance=150)

    def test_finish_shot_view(self):
        url = reverse('end-of-shot', kwargs={'course_id': self.course.id, 'round_id': self.round.id, 'hole_id': self.hole.id})
        request = self.factory.get(url)
        request.user = self.user
        response = end_of_shot(request, hole_id=self.hole.id, course_id=self.course.id, round_id=self.round)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('scorecard', args=[self.hole.id]))

class ShotModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)
        self.club = Clubs.objects.create(user=self.user, club_name='Test Club')
        self.shot = Shot.objects.create(user=self.user, club=self.club, course=self.course, round=self.round, hole=self.hole, shot_num_per_hole=1, latitude=40.7128, longitude=-74.0060, end_latitude=40.7128, end_longitude=-74.0060, shot_distance=150)

    def test_shot_model(self):
        self.assertEqual(self.shot.user, self.user)
        self.assertEqual(self.shot.club, self.club)
        self.assertEqual(self.shot.course, self.course)
        self.assertEqual(self.shot.round, self.round)
        self.assertEqual(self.shot.hole, self.hole)
        self.assertEqual(self.shot.shot_num_per_hole, 1)
        self.assertEqual(self.shot.latitude, 40.7128)
        self.assertEqual(self.shot.longitude, -74.0060)
        self.assertEqual(self.shot.end_latitude, 40.7128)
        self.assertEqual(self.shot.end_longitude, -74.0060)
        self.assertEqual(self.shot.shot_distance, 150)
        self.assertEqual(self.shot.created_at, self.shot.created_at)

class HoleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)

    def test_hole_model(self):
        self.assertEqual(self.hole.round, self.round)
        self.assertEqual(self.hole.hole_num, 1)
        self.assertEqual(self.hole.hole_par, 4)
        self.assertEqual(self.hole.hole_distance, 350)
        self.assertEqual(str(self.hole), 'Test Course - Hole 1')

class RoundModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)

    def test_round_model(self):
        self.assertEqual(self.round.user, self.user)
        self.assertEqual(self.round.course, self.course)
        self.assertEqual(self.round.round_completed, False)
        self.assertEqual(str(self.round), str(self.round.round_date))

class ClubsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.club = Clubs.objects.create(user=self.user, club_name='Test Club')

    def test_club_model(self):
        self.assertEqual(self.club.user, self.user)
        self.assertEqual(self.club.club_name, 'Test Club')
        self.assertEqual(str(self.club), 'Test Club')

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)

    def test_course_model(self):
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.address, 'Test Address')
        self.assertEqual(self.course.rating, 4.5)
        self.assertEqual(self.course.latitude, 40.7128)
        self.assertEqual(self.course.longitude, -74.0060)
        self.assertEqual(str(self.course), 'Test Course')
        self.assertEqual(self.course.__str__(), 'Test Course')

class ShotFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)
        self.club = Clubs.objects.create(user=self.user, club_name='Test Club')

    def test_shot_form_valid(self):
        form_data = {'club': self.club.id, 'latitude': 40.7128, 'longitude': -74.0060}
        form = ShotForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_shot_form_invalid(self):
        form_data = {'club': self.club.id, 'latitude': 40.7128, 'longitude': 'invalid'}
        form = ShotForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

class RoundFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)

    def test_round_form_valid(self):
        form_data = {'course': self.course}
        form = RoundForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)


    def test_round_form_invalid(self):
        form_data = {'course': 'invalid'}
        form = RoundForm(data=form_data)
        self.assertFalse(form.is_valid())

class HoleFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.course = Course.objects.create(name='Test Course', address='Test Address', rating=4.5, latitude=40.7128, longitude=-74.0060)
        self.round = Round.objects.create(user=self.user, course=self.course)
        self.hole = Hole.objects.create(round=self.round, hole_num=1, hole_par=4, hole_distance=350, course=self.course)

    def test_hole_form_valid(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': 350}
        form = HoleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_hole_form_invalid(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': 'invalid'}
        form = HoleForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hole_form_invalid_negative(self):
        form_data = {'hole_num': 1, 'hole_par': 4, 'hole_distance': -1}
        form = HoleForm(data=form_data)
        self.assertFalse(form.is_valid())

