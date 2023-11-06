import sqlite3

# Function to insert or update user information in the database
def put_to_db(users_id, users_name=None, registration=False):
    connection = None
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        if registration == False:
            sql = f"""
            INSERT INTO users(users_id, spins)
            VALUES("{users_id}", 1)
            """
        else:
            sql = f"""
            UPDATE users
            SET users_name="{users_name}", spins=1000
            WHERE users_id="{users_id}"
            """
        cursor.execute(sql)
        connection.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if connection:
            connection.close()

# Function to get the number of spins for a user
def how_many_spins(users_id):
    connection = None
    result = 0
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        sql = f"""
        SELECT spins
        FROM users
        WHERE users_id={users_id}
        """
        cursor.execute(sql)
        result = cursor.fetchone()[0]
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if connection:
            connection.close()
    return result

# Function to decrement a user's spin count
def minus_spin(users_id):
    count_of_spins = how_many_spins(users_id)
    if count_of_spins > 0:
        connection = None
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            sql = f"""
            UPDATE users
            SET spins={count_of_spins - 1}
            WHERE users_id={users_id}
            """
            cursor.execute(sql)
            connection.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            if connection:
                connection.close()
            return True
    return 'Не хватает спинов'

# Function to check if a user already exists in the database
def check_users(users_id):
    connection = None
    result = None
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        sql = f"""
        SELECT users_id
        FROM users
        WHERE users_id={users_id}
        """
        cursor.execute(sql)
        result = cursor.fetchone()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if connection:
            connection.close()
    return result
