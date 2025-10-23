import os
import sqlite3


class ProjectDAL:
	DB_PATH = os.path.join(os.path.dirname(__file__), "projects.db")

	@staticmethod
	def _get_connection():
		conn = sqlite3.connect(ProjectDAL.DB_PATH)
		conn.row_factory = sqlite3.Row
		return conn

	@staticmethod
	def initialize_db():
		conn = ProjectDAL._get_connection()
		c = conn.cursor()
		c.execute(
			"""
			CREATE TABLE IF NOT EXISTS projects (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				Title TEXT NOT NULL,
				Description TEXT,
				ImageFileName TEXT
			);
			"""
		)
		# seed initial data if empty
		c.execute("SELECT COUNT(*) AS cnt FROM projects")
		row = c.fetchone()
		if row[0] == 0:
			initial_projects = [
				(
					"Campus Cravings",
					"Full‑stack web app connecting IU students with local restaurant deals.",
					"Campus-Cravings.png",
				),
				(
					"Fantasy Football Predictions",
					"Python visualizations forecasting fantasy performance from historical NFL data.",
					"Fantasy-football.png",
				),
			]
			c.executemany(
				"INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?)",
				initial_projects,
			)
		conn.commit()
		conn.close()

	@staticmethod
	def get_all_projects():
		conn = ProjectDAL._get_connection()
		c = conn.cursor()
		c.execute("SELECT id, Title, Description, ImageFileName FROM projects ORDER BY id DESC")
		rows = c.fetchall()
		projects = [dict(r) for r in rows]
		conn.close()
		return projects

	@staticmethod
	def add_new_project(title: str, description: str, image_filename: str):
		conn = ProjectDAL._get_connection()
		c = conn.cursor()
		c.execute(
			"INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?)",
			(title, description, image_filename),
		)
		conn.commit()
		conn.close()


