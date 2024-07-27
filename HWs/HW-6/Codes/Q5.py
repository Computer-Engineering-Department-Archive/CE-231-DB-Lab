import psycopg2

def session_1():
    try:
        conn = psycopg2.connect(
            database = "dblab",
            user = 'postgres',
            password = '1234',
            host = '127.0.0.1',
            port = '5432'
        )
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
            id INT PRIMARY KEY,
            name VARCHAR(50),
            balance DEC (10)
            );
        ''')
        cursor.execute('''INSERT INTO accounts (id, name, balance) VALUES (0, 'Keivan', 50);''')

        # data = cursor.fetchone()
        # print(data)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def session_2():
    try:
        conn = psycopg2.connect(
            database = "dblab",
            user = 'postgres',
            password = '1234',
            host = '127.0.0.1',
            port = '5432'
        )
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM accounts''')

        data = cursor.fetchone()
        print(data)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


if __name__ == '__main__':

    # Session 1: Create a table and insert a row
    session_1()

    # Session 2: Select all rows from the table
    session_2()