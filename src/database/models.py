from src.database.connection import DatabaseConnection
from mysql.connector import Error

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection().get_connection()

    def create_tables(self):
        try:
            with self.db.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT NOT NULL UNIQUE,
                        username VARCHAR(255),
                        full_name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS requests (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        category VARCHAR(50) NOT NULL,
                        subcategory VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
            self.db.commit()
        except Error as e:
            print(f"Error creating tables: {e}")

    def create_user_if_not_exists(self, user_id: int, username: str, full_name: str):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    "INSERT IGNORE INTO users (user_id, username, full_name) VALUES (%s, %s, %s)",
                    (user_id, username, full_name)
                )
            self.db.commit()
        except Error as e:
            print(f"Error creating user: {e}")

    def log_request(self, user_id: int, category: str, subcategory: str = None):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO requests (user_id, category, subcategory) VALUES (%s, %s, %s)",
                    (user_id, category, subcategory)
                )
            self.db.commit()
        except Error as e:
            print(f"Error logging request: {e}")