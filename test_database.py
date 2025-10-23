import unittest
import os
import sys
import tempfile
import sqlite3

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from DAL import ProjectDAL


class TestDatabaseOperations(unittest.TestCase):
    """Test cases for database operations and data integrity"""
    
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
    
    def test_database_connection(self):
        """Test database connection works"""
        conn = ProjectDAL._get_connection()
        self.assertIsNotNone(conn)
        conn.close()
    
    def test_table_structure(self):
        """Test that projects table has correct structure"""
        conn = ProjectDAL._get_connection()
        c = conn.cursor()
        c.execute("PRAGMA table_info(projects)")
        columns = c.fetchall()
        conn.close()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'Title', 'Description', 'ImageFileName']
        
        for col in expected_columns:
            self.assertIn(col, column_names, f"Column {col} should exist")
    
    def test_initial_data_seeding(self):
        """Test that initial data is properly seeded"""
        projects = ProjectDAL.get_all_projects()
        
        # Should have 2 initial projects
        self.assertEqual(len(projects), 2)
        
        # Check first project (Fantasy Football)
        fantasy_project = projects[0]
        self.assertEqual(fantasy_project['Title'], 'Fantasy Football Predictions')
        self.assertIn('Python visualizations', fantasy_project['Description'])
        self.assertEqual(fantasy_project['ImageFileName'], 'Fantasy-football.png')
        
        # Check second project (Campus Cravings)
        campus_project = projects[1]
        self.assertEqual(campus_project['Title'], 'Campus Cravings')
        self.assertIn('Full‑stack web app', campus_project['Description'])
        self.assertEqual(campus_project['ImageFileName'], 'Campus-Cravings.png')
    
    def test_project_id_auto_increment(self):
        """Test that project IDs auto-increment properly"""
        # Add a new project
        ProjectDAL.add_new_project("Test Project 1", "Description 1", "image1.jpg")
        ProjectDAL.add_new_project("Test Project 2", "Description 2", "image2.jpg")
        
        projects = ProjectDAL.get_all_projects()
        
        # Should have 4 projects total (2 initial + 2 new)
        self.assertEqual(len(projects), 4)
        
        # Check that IDs are sequential (projects are returned in DESC order)
        ids = [p['id'] for p in projects]
        self.assertEqual(sorted(ids, reverse=True), ids)  # Should be in descending order
    
    def test_empty_title_handling(self):
        """Test handling of empty title"""
        # This should work (empty string is allowed by the database)
        ProjectDAL.add_new_project("", "Description", "image.jpg")
        projects = ProjectDAL.get_all_projects()
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects[0]['Title'], "")
    
    def test_special_characters_in_data(self):
        """Test handling of special characters in project data"""
        special_title = "Project with Special Chars: @#$%^&*()"
        special_description = "Description with émojis 🚀 and symbols & more!"
        special_image = "image-with-dashes_and.underscores.jpg"
        
        ProjectDAL.add_new_project(special_title, special_description, special_image)
        
        projects = ProjectDAL.get_all_projects()
        added_project = projects[0]
        
        self.assertEqual(added_project['Title'], special_title)
        self.assertEqual(added_project['Description'], special_description)
        self.assertEqual(added_project['ImageFileName'], special_image)
    
    def test_database_persistence(self):
        """Test that data persists between connections"""
        # Add a project
        ProjectDAL.add_new_project("Persistent Project", "Test persistence", "persist.jpg")
        
        # Create a new connection (simulating app restart)
        conn = ProjectDAL._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM projects")
        count = c.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 3)  # 2 initial + 1 added


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation and edge cases"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        ProjectDAL.DB_PATH = self.temp_db.name
        ProjectDAL.initialize_db()
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_long_strings(self):
        """Test handling of very long strings"""
        long_title = "A" * 1000
        long_description = "B" * 5000
        long_image = "C" * 500
        
        ProjectDAL.add_new_project(long_title, long_description, long_image)
        
        projects = ProjectDAL.get_all_projects()
        added_project = projects[0]
        
        self.assertEqual(added_project['Title'], long_title)
        self.assertEqual(added_project['Description'], long_description)
        self.assertEqual(added_project['ImageFileName'], long_image)
    
    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        unicode_title = "项目标题 🎯"
        unicode_description = "项目描述 with émojis and 中文"
        unicode_image = "图片-名称.png"
        
        ProjectDAL.add_new_project(unicode_title, unicode_description, unicode_image)
        
        projects = ProjectDAL.get_all_projects()
        added_project = projects[0]
        
        self.assertEqual(added_project['Title'], unicode_title)
        self.assertEqual(added_project['Description'], unicode_description)
        self.assertEqual(added_project['ImageFileName'], unicode_image)


if __name__ == '__main__':
    unittest.main()
