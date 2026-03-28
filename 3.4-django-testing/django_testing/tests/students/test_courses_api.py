import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student

@pytest.fixture
def api_client():
    """Фикстура для API-клиента DRF."""
    return APIClient()

@pytest.fixture
def course_factory():
    """Фабрика для создания курсов."""
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    """Фабрика для создания студентов."""
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory

@pytest.mark.django_db
class TestCourseAPI:

    def test_retrieve_course(self, api_client, course_factory):
        """Проверка получения первого курса (retrieve-логика)."""
        course = course_factory()
        url = f'/api/v1/courses/{course.id}/'
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['id'] == course.id
        assert response.data['name'] == course.name

    def test_list_courses(self, api_client, course_factory):
        """Проверка получения списка курсов (list-логика)."""
        courses = course_factory(_quantity=3)
        url = '/api/v1/courses/'
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 3
        course_ids = [course['id'] for course in response.data]
        for course in courses:
            assert course.id in course_ids

    def test_filter_courses_by_id(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по id."""
        courses = course_factory(_quantity=3)
        target_course = courses[0]
        url = '/api/v1/courses/'
        response = api_client.get(url, data={'id': [target_course.id]})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == target_course.id

    def test_filter_courses_by_name(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по name (точное совпадение)."""
        target_name = 'Python-разработка'
        course1 = course_factory(name=target_name)
        course2 = course_factory(name='Java-разработка')
        course3 = course_factory(name='JavaScript-разработка')

        url = '/api/v1/courses/'
        response = api_client.get(url, data={'name': target_name})

        assert response.status_code == 200, f"Статус: {response.status_code}, данные: {response.data}"

        filtered_courses = [
            course for course in response.data
            if course['name'] == target_name
        ]
        assert len(filtered_courses) >= 1, (
            f"Ожидался курс с точным именем '{target_name}', но найдено: {len(filtered_courses)}. Все курсы: {response.data}"
        )

    def test_create_course_success(self, api_client):
        """Тест успешного создания курса."""
        url = '/api/v1/courses/'
        course_data = {
            'name': 'Новый курс по тестированию',
            'students': []
        }
        response = api_client.post(url, course_data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == course_data['name']
        assert isinstance(response.data['students'], list)

    def test_update_course_success(self, api_client, course_factory, student_factory):
        """Тест успешного обновления курса."""
        course = course_factory()
        student = student_factory()

        url = f'/api/v1/courses/{course.id}/'
        update_data = {
            'name': 'Обновлённое название курса',
            'students': [student.id]
        }

        response = api_client.put(url, update_data, format='json')
        assert response.status_code == 200, f"Статус: {response.status_code}, ответ: {response.data}"
        assert response.data['name'] == update_data['name'], f"Ожидали имя '{update_data['name']}', получили '{response.data['name']}'"

        course.refresh_from_db()
        students_in_course = list(course.students.all())
        assert student in students_in_course, (
            f"Студент с ID {student.id} не был добавлен к курсу. "
            f"Текущие студенты: {[s.id for s in students_in_course]}"
        )

    def test_delete_course_success(self, api_client, course_factory):
        """Тест успешного удаления курса."""
        course = course_factory()
        url = f'/api/v1/courses/{course.id}/'
        response = api_client.delete(url)
        assert response.status_code == 204
        with pytest.raises(Course.DoesNotExist):
            Course.objects.get(id=course.id)
