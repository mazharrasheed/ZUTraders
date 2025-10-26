
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib import messages
from django.test import TestCase, Client
from django.test import TestCase, RequestFactory
from django.urls import reverse
from home.models import Category
from home.forms import CategoryForm

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from home.views.category import add_category

class CategoryModelTestCase(TestCase):
    def setUp(self):
        # Create a sample category for testing
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        """
        Test whether a category is created correctly.
        """
        # Retrieve the category from the database
        category = Category.objects.get(name='Test Category')

        # Check if the retrieved category matches the created category
        self.assertEqual(category.name, 'Test Category')
        self.assertFalse(category.is_deleted)  # Check that is_deleted is False by default

    def test_category_deletion(self):
        """
        Test whether a category is deleted correctly.
        """
        # Delete the category
        self.category.delete()

        # Check if the category is deleted by verifying it doesn't exist in the database
        self.assertFalse(Category.objects.filter(name='Test Category').exists())

    def test_category_str_method(self):
        """
        Test the __str__ method of the Category model.
        """
        # Check if the string representation of the category is correct
        self.assertEqual(str(self.category), 'Test Category')


class CategoryFormTestCase(TestCase):
    def test_category_form_valid(self):
        """
        Test whether the CategoryForm is valid with valid data.
        """
        # Define valid form data
        form_data = {'name': 'Test Category'}

        # Create form instance with valid data
        form = CategoryForm(data=form_data)

        # Check if form is valid
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        """
        Test whether the CategoryForm is invalid with invalid data.
        """
        # Define invalid form data (missing name field)
        form_data = {}

        # Create form instance with invalid data
        form = CategoryForm(data=form_data)

        # Check if form is not valid
        self.assertFalse(form.is_valid())

    def test_category_form_save(self):
        """
        Test whether the CategoryForm saves data correctly.
        """
        # Define form data
        form_data = {'name': 'Test Category'}

        # Create form instance with form data
        form = CategoryForm(data=form_data)

        # Check if form is valid before saving
        self.assertTrue(form.is_valid())

        # Save the form
        category = form.save()

        # Retrieve the saved category from the database
        saved_category = Category.objects.get(name='Test Category')

        # Check if the saved category matches the form data
        self.assertEqual(category, saved_category)


class AddCategoryTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

        # Create a category for testing
        self.category_data = {'name': 'Test Category'}
        self.category = Category.objects.create(**self.category_data)

        # Create a client to simulate HTTP requests
        self.client = Client()

    
    def test_add_category_authenticated_valid_post(self):
        # Log in the test user
        self.client.login(username='testuser', password='password123')

        # Prepare POST data
        post_data = {'name': 'New Category'}

        # Send POST request to add_category view
        response = self.client.post(reverse('category'), post_data, follow=True)

        # Check if category is added successfully
        self.assertEqual(response.status_code, 200)  # Expecting successful response

        # Check if the category is in the database
        self.assertTrue(Category.objects.filter(name='New Category').exists())

        # Check if success message is sent
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Category Added successfully !!")
                                          

    def test_add_category_unauthenticated(self):
        # Send GET request to add_category view
        response = self.client.get(reverse('category'))

        # Check if response is a redirect to signin page
        self.assertRedirects(response, reverse('signin'))

    

    # Write similar test cases for other scenarios (invalid post, get request, unauthenticated user)
    # ...


 

# Edit Category


    def test_edit_category_authenticated_valid_post(self):
        # Log in the test user
        self.client.login(username='testuser', password='password123')

        # Prepare POST data
        post_data = {'name': 'Updated Category'}

        # Send POST request to edit_category view
        url = reverse('editcategory', kwargs={'id': self.category.id})
        response = self.client.post(url, post_data, follow=True)

        # Check if category is updated successfully
        self.assertEqual(response.status_code, 200)  # Expecting successful response

        # Check if the category is updated in the database
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

        # Check if success message is sent
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Category Updated successfully !!")

    # Write similar test cases for other scenarios (invalid post, get request, unauthenticated user)
    # ...

    def test_edit_category_authenticated_invalid_post(self):
        # Log in the test user
        self.client.login(username='testuser', password='password123')

        # Prepare invalid POST data
        post_data = {'name': ''}  # Empty name, which is invalid

        # Send POST request to edit_category view
        url = reverse('editcategory', kwargs={'id': self.category.id})
        response = self.client.post(url, post_data, follow=True)

        # Ensure response is a redirect (status code 302)
        # self.assertEqual(response.status_code, 302)

        # Check if the form errors are present in the response context
        form_errors = response.context.get('form').errors
        self.assertTrue(form_errors)
        self.assertIn('name', form_errors)
        self.assertEqual(form_errors['name'], ['This field is required.'])

    def test_edit_category_authenticated_get_request(self):
        # Log in the test user
        self.client.login(username='testuser', password='password123')

        # Send GET request to edit_category view
        url = reverse('editcategory', kwargs={'id': self.category.id})
        response = self.client.get(url, follow=True)

        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the form is rendered with the category data
        self.assertContains(response, 'Test Category')  # Ensure original category name is present in the response

    def test_edit_category_unauthenticated_user(self):
        
        # Send GET request to edit_category view without logging in
        url = reverse('editcategory', kwargs={'id': self.category.id})
        response = self.client.get(url)
        # Check if response status code is 302 (redirect to sign-in page)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if user is redirected to sign-in page
        self.assertRedirects(response, '/signin/')  # Adjust URL as per your project's setup
  

    def test_delete_category_authenticated_user(self):
        # Authenticate the user
        self.client.login(username='testuser', password='password123')

        # Send POST request to delete_category view
        url = reverse('deletecategory', kwargs={'id': self.category.id})
        response = self.client.post(url)

        # Check if category is deleted
        self.assertFalse(Category.objects.filter(id=self.category.id, is_deleted=False).exists())

        # Check if success message is sent
        messages_text = [message.message for message in messages.get_messages(response.wsgi_request)]
        self.assertIn('Category Deleted successfully !!', messages_text)

        # Check if user is redirected to 'category' page
        self.assertRedirects(response, reverse('category'))

    def test_delete_category_unauthenticated_user(self):
        # Send POST request to delete_category view without logging in
        url = reverse('deletecategory', kwargs={'id': self.category.id})
        response = self.client.post(url)

        # Check if category is not deleted
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

        # Check if user is redirected to 'signin' page
        self.assertRedirects(response, reverse('signin'))