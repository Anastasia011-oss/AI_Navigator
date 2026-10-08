import sqlite3
from datetime import datetime


DATABASE = "navigator.db"


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_type TEXT,
            start_point TEXT,
            finish_point TEXT,
            route TEXT,
            distance REAL,
            time REAL,
            traffic REAL,
            actual_time REAL,
            actual_distance REAL,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_route(
        user_name,
        user_type,
        start_point,
        finish_point,
        route,
        distance,
        time,
        traffic
):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    route_text = ",".join(route)

    cursor.execute("""
        INSERT INTO routes (
            user_name,
            user_type,
            start_point,
            finish_point,
            route,
            distance,
            time,
            traffic,
            actual_time,
            actual_distance,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        user_type,
        start_point,
        finish_point,
        route_text,
        distance,
        time,
        traffic,
        None,
        None,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_history():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_name,
            user_type,
            start_point,
            finish_point,
            route,
            distance,
            time,
            traffic,
            actual_time,
            actual_distance,
            created_at
        FROM routes
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def update_actual_result(
        route_id,
        actual_time,
        actual_distance
):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE routes
        SET actual_time = ?,
            actual_distance = ?
        WHERE id = ?
    """, (
        actual_time,
        actual_distance,
        route_id
    ))

    connection.commit()
    connection.close()


def get_route_statistics(
        start_point,
        finish_point
):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            route,
            COUNT(*),
            AVG(time),
            AVG(actual_time),
            AVG(distance),
            AVG(actual_distance)
        FROM routes
        WHERE start_point = ?
        AND finish_point = ?
        GROUP BY route
    """, (
        start_point,
        finish_point
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_user_statistics(
        user_name,
        start_point,
        finish_point
):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            route,
            COUNT(*),
            AVG(time),
            AVG(actual_time),
            AVG(distance),
            AVG(actual_distance)
        FROM routes
        WHERE user_name = ?
        AND start_point = ?
        AND finish_point = ?
        GROUP BY route
    """, (
        user_name,
        start_point,
        finish_point
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows