"""
database.py
Gym Tracker Pro
Handles all database operations using SQLite3.
"""

import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.connection = None
        self.create_connection()
        self.create_tables()

    # --------------------------
    # Database Connection
    # --------------------------
    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Database Connected Successfully")
        except Error as e:
            print(e)

    # --------------------------
    # Create Tables
    # --------------------------
    def create_tables(self):

        cursor = self.connection.cursor()

        # Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE,
            password TEXT,
            age INTEGER,
            gender TEXT,
            height REAL,
            weight REAL
        )
        """)

        # Workout Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            duration INTEGER,
            calories REAL,
            workout_date TEXT
        )
        """)

        # Nutrition Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            meal TEXT,
            calories REAL,
            protein REAL,
            carbs REAL,
            fats REAL,
            meal_date TEXT
        )
        """)

        # Water Intake
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS water(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            glasses INTEGER,
            intake_date TEXT
        )
        """)

        # Sleep Tracker
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            hours REAL,
            sleep_date TEXT
        )
        """)

        # Goals
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            goal TEXT,
            target TEXT,
            status TEXT
        )
        """)

        # Personal Records
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            exercise TEXT,
            best_weight REAL,
            reps INTEGER
        )
        """)

        self.connection.commit()

    # --------------------------
    # User Functions
    # --------------------------
    def register_user(self, fullname, username, password,
                      age, gender, height, weight):

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
            INSERT INTO users(
            fullname,
            username,
            password,
            age,
            gender,
            height,
            weight
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                fullname,
                username,
                password,
                age,
                gender,
                height,
                weight
            ))

            self.connection.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        return cursor.fetchone()

    # --------------------------
    # Workout Functions
    # --------------------------
    def add_workout(self,
                    username,
                    exercise,
                    sets,
                    reps,
                    weight,
                    duration,
                    calories,
                    date):

        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO workouts(
        username,
        exercise,
        sets,
        reps,
        weight,
        duration,
        calories,
        workout_date
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            username,
            exercise,
            sets,
            reps,
            weight,
            duration,
            calories,
            date
        ))

        self.connection.commit()

    def get_workouts(self, username):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT * FROM workouts
        WHERE username=?
        ORDER BY id DESC
        """, (username,))

        return cursor.fetchall()

    def delete_workout(self, workout_id):

        cursor = self.connection.cursor()

        cursor.execute("""
        DELETE FROM workouts
        WHERE id=?
        """, (workout_id,))

        self.connection.commit()

    # --------------------------
    # Nutrition
    # --------------------------
    def add_meal(self,
                 username,
                 meal,
                 calories,
                 protein,
                 carbs,
                 fats,
                 date):

        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO nutrition(
        username,
        meal,
        calories,
        protein,
        carbs,
        fats,
        meal_date
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            username,
            meal,
            calories,
            protein,
            carbs,
            fats,
            date
        ))

        self.connection.commit()

    def get_meals(self, username):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT * FROM nutrition
        WHERE username=?
        ORDER BY id DESC
        """, (username,))

        return cursor.fetchall()

    # --------------------------
    # Water
    # --------------------------
    def add_water(self, username, glasses, date):

        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO water(
        username,
        glasses,
        intake_date
        )
        VALUES(?,?,?)
        """,
        (
            username,
            glasses,
            date
        ))

        self.connection.commit()

    # --------------------------
    # Sleep
    # --------------------------
    def add_sleep(self,
                  username,
                  hours,
                  date):

        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO sleep(
        username,
        hours,
        sleep_date
        )
        VALUES(?,?,?)
        """,
        (
            username,
            hours,
            date
        ))

        self.connection.commit()

    # --------------------------
    # Goals
    # --------------------------
    def add_goal(self,
                 username,
                 goal,
                 target,
                 status="Pending"):

        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO goals(
        username,
        goal,
        target,
        status
        )
        VALUES(?,?,?,?)
        """,
        (
            username,
            goal,
            target,
            status
        ))

        self.connection.commit()

    def get_goals(self, username):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT * FROM goals
        WHERE username=?
        """, (username,))

        return cursor.fetchall()

    # --------------------------
    # Dashboard Statistics
    # --------------------------
    def total_workouts(self, username):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM workouts
        WHERE username=?
        """, (username,))

        return cursor.fetchone()[0]

    def total_calories(self, username):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT SUM(calories)
        FROM workouts
        WHERE username=?
        """, (username,))

        result = cursor.fetchone()[0]

        if result is None:
            return 0

        return result

    def close(self):

        if self.connection:
            self.connection.close()


# --------------------------
# Test
# --------------------------

if __name__ == "__main__":

    db = Database()

    print("Database Ready")
