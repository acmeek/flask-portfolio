import unittest
import os
import sys
import tempfile
import sqlite3

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from DAL import ProjectDAL
from app import app


class TestProjectDAL(unittest.TestCase):
    """Test cases for ProjectDAL class"""
    
    def setUp(self):
        """Set up test database"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        ProjectDAL.DB_PATH = self.temp_db.name
        
        # Initialize the test database
        ProjectDAL.initialize_db()
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_initialize_db(self):
        """Test database initialization"""
        conn = ProjectDAL._get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        result = c.fetchone()
        conn.close()
        self.assertIsNotNone(result, "Projects table should be created")
    
    def test_add_new_project(self):
        """Test adding a new project"""
        title = "Test Project"
        description = "Test Description"
        image_filename = "test.jpg"
        
        ProjectDAL.add_new_project(title, description, image_filename)
        
        projects = ProjectDAL.get_all_projects()
        self.assertEqual(len(projects), 3)  # 2 initial + 1 new
        self.assertEqual(projects[0]['Title'], title)
        self.assertEqual(projects[0]['Description'], description)
        self.assertEqual(projects[0]['ImageFileName'], image_filename)
    
    def test_get_all_projects(self):
        """Test retrieving all projects"""
        projects = ProjectDAL.get_all_projects()
        self.assertEqual(len(projects), 2)  # Initial projects
        self.assertEqual(projects[0]['Title'], "Fantasy Football Predictions")
        self.assertEqual(projects[1]['Title'], "Campus Cravings")


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        """Set up test client"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        ProjectDAL.DB_PATH = self.temp_db.name
        
        # Initialize the test database
        ProjectDAL.initialize_db()
        
        # Create test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret'
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_index_page(self):
        """Test index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Andrew Meek', response.data)
    
    def test_about_page(self):
        """Test about page loads successfully"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
    
    def test_projects_page(self):
        """Test projects page loads successfully"""
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Campus Cravings', response.data)
        self.assertIn(b'Fantasy Football', response.data)
    
    def test_contact_page_get(self):
        """Test contact page GET request"""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'contact', response.data.lower())
    
    def test_resume_page(self):
        """Test resume page loads successfully"""
        response = self.client.get('/resume')
        self.assertEqual(response.status_code, 200)
    
    def test_new_project_form(self):
        """Test new project form page"""
        response = self.client.get('/projects/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'form', response.data.lower())


if __name__ == '__main__':
    unittest.main()
