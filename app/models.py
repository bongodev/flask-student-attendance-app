from app.database import get_db_connection

def add_student(name):
    """Insert a new student and return their ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
    student_id = cursor.lastrowid  # Get last inserted student ID
    conn.commit()
    cursor.close()
    conn.close()
    return student_id

def mark_attendance(student_id, date, status="Present"):
    """Mark attendance for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO attendance (student_id, date, status) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (student_id, date, status))

    conn.commit()
    cursor.close()
    conn.close()

def get_attendance():
    """Fetch attendance records."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id AS student_id, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def get_attendance_stats(start_date, end_date):
    """Fetch total Present vs Absent count for a date range."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM attendance
        WHERE date BETWEEN %s AND %s
        GROUP BY status
    """, (start_date, end_date))

    data = {row["status"]: row["count"] for row in cursor.fetchall()}
    cursor.close()
    conn.close()

    return {"Present": data.get("Present", 0), "Absent": data.get("Absent", 0)}

def get_student_attendance(name, start_date, end_date):
    """Fetch Present vs Absent count for a particular student."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.status, COUNT(*) as count
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE s.name = %s AND a.date BETWEEN %s AND %s
        GROUP BY a.status
    """, (name, start_date, end_date))

    data = {row["status"]: row["count"] for row in cursor.fetchall()}
    cursor.close()
    conn.close()

    return {"Student": name, "Present": data.get("Present", 0), "Absent": data.get("Absent", 0)}
