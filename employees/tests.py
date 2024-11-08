from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Employee

class EmployeeViewSetTestCase(APITestCase):
    def setUp(self):
        # গ্রুপ তৈরি
        self.admin_group = Group.objects.create(name='Admin')
        self.manager_group = Group.objects.create(name='Manager')
        self.employee_group = Group.objects.create(name='Employee')

        # ইউজার তৈরি এবং গ্রুপে অ্যাড করা
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.groups.add(self.admin_group)

        self.manager_user = User.objects.create_user(username='manager', password='managerpassword')
        self.manager_user.groups.add(self.manager_group)

        self.employee_user = User.objects.create_user(username='employee', password='employeepassword')
        self.employee_user.groups.add(self.employee_group)

        # ক্লায়েন্ট তৈরি
        self.client = APIClient()

        # ডিফল্ট URL সেটআপ
        self.employee_list_url = reverse('employee-list')

    def test_employee_list_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_as_manager(self):
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_as_employee(self):
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_create_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "position": "Developer",
            "salary": "5000.00",
            "address": "123 Street",
            "user": self.admin_user.id
        }
        response = self.client.post(self.employee_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_create_as_manager(self):
        self.client.force_authenticate(user=self.manager_user)
        data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "position": "Manager",
            "salary": "6000.00",
            "address": "456 Avenue",
            "user": self.manager_user.id
        }
        response = self.client.post(self.employee_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Manager cannot create

    def test_employee_create_as_employee(self):
        self.client.force_authenticate(user=self.employee_user)
        data = {
            "name": "Sam Smith",
            "email": "sam@example.com",
            "position": "Employee",
            "salary": "4000.00",
            "address": "789 Road",
            "user": self.employee_user.id
        }
        response = self.client.post(self.employee_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Employee cannot create
