import mysql.connector
import os

print(
    "DB Config: ",
    os.getenv("DB_HOST", "-"),
    os.getenv("DB_USER", "-"),
    os.getenv("DB_PASSWORD", "-"),
    os.getenv("DB_NAME", "-"),
)

# Fetch database credentials from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "rootpassword"),
    "database": os.getenv("DB_NAME", "attendance_db"),
}


def get_db_connection():
    """Establish a database connection."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def init_db():
    """Initialize database and create tables if not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_db")
    cursor.execute("USE attendance_db")

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT NOT NULL,
        date DATE NOT NULL,
        status ENUM('Present', 'Absent') DEFAULT 'Present',
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()
