import base64
import hashlib
import re

import pandas as pd
from matplotlib import pyplot as plt

import conn


def generate_short_url(long_url):
    # Create an SHA-256 hash of the long URL
    hash_object = hashlib.sha256(long_url.encode())
    hash_bytes = hash_object.digest()
    # Encode to base64 and take the first 6 characters
    short_url = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')[:6]
    return short_url


def get_short_url(connection, long_url):
    cursor = connection.cursor()
    result = cursor.execute(
        "DECLARE @ShortURL NVARCHAR(6); EXEC urls.GetShortURL ?, @ShortURL OUTPUT; SELECT @ShortURL;",
        long_url).fetchone()
    return result[0] if result else None


def get_long_url(connection, short_url):
    cursor = connection.cursor()
    result = cursor.execute(
        "DECLARE @LongURL NVARCHAR(2048); EXEC urls.GetLongURL ?, @LongURL OUTPUT; SELECT @LongURL;",
        short_url).fetchone()
    return result[0] if result else None


def create_short_url(connection, long_url):
    short_url = generate_short_url(long_url)
    while not is_short_url_unique(connection, short_url):
        short_url = generate_short_url(long_url + short_url)  # Re-hash with the short URL to ensure uniqueness
    cursor = connection.cursor()
    cursor.execute("EXEC urls.InsertURLMapping ?, ?", long_url, short_url)
    connection.commit()
    return short_url


def is_short_url_unique(connection, short_url):
    cursor = connection.cursor()
    exists = cursor.execute("DECLARE @exists BIT; EXEC urls.CheckShortURL ?, @exists OUTPUT; SELECT @exists;",
                            short_url).fetchone()[0]
    return exists == 0


def record_visit(connection, short_url):
    cursor = connection.cursor()
    cursor.execute("EXEC urls.InsertVisit ?", short_url)
    connection.commit()


def is_valid_url(url):
    # Regular expression to validate a URL
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def handle_url(connection, long_url):
    if not is_valid_url(long_url):
        print(f"Invalid URL: {long_url}")
        return None

    short_url = get_short_url(connection, long_url)
    if short_url:
        record_visit(connection, short_url)
    else:
        short_url = create_short_url(connection, long_url)
    return short_url


def fetch_data(connection, procedure_name):
    cursor = connection.cursor()
    cursor.execute(f"EXEC {procedure_name}")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame.from_records(rows, columns=columns)


def plot_new_links_per_day(data):
    data.plot(x='Date', y='NewLinks', kind='bar', title='New Links Registered Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of New Links')
    plt.show()


def plot_visits_per_day(data):
    data.plot(x='Date', y='Visits', kind='bar', title='Visits Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Visits')
    plt.show()


def plot_top3_most_visited(data):
    data.plot(x='ShortURL', y='VisitCount', kind='bar', title='Top 3 Most Visited Short Links')
    plt.xlabel('Short URL')
    plt.ylabel('Number of Visits')
    plt.show()


def display_all_mappings_with_details(data):
    print(data)


def get_url_statistics(connection, short_url):
    cursor = connection.cursor()
    result = cursor.execute("""
        DECLARE @ShortURL NVARCHAR(6);
        SET @ShortURL = ?;
        SELECT LongURL, CreatedAt, 
               (SELECT COUNT(*) FROM urls.URLVisits WHERE ShortURL = @ShortURL) AS VisitCount
        FROM urls.URLMapping
        WHERE ShortURL = @ShortURL;
    """, short_url).fetchone()
    return {
        "long_url": result[0],
        "created_at": result[1].strftime('%Y-%m-%d %H:%M:%S'),
        "visit_count": result[2]
    } if result else None



# Triggers

def activate_trigger(connection, activate):
    try:
        cursor = connection.cursor()
        cursor.execute("EXEC urls.TogglePreventTableActionsTrigger ?", activate)
        connection.commit()
    except Exception as e:
        print("Error toggling trigger:", e)


def attempt_create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE urls.TestTable (ID INT PRIMARY KEY);")
        connection.commit()
    except Exception as e:
        print("Create table attempt failed:", e)


def attempt_alter_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE urls.URLMapping ADD TestColumn NVARCHAR(50);")
        connection.commit()
    except Exception as e:
        print("Alter table attempt failed:", e)


def attempt_drop_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE urls.URLMapping;")
        connection.commit()
    except Exception as e:
        print("Drop table attempt failed:", e)


def activate_logger_triggers(connection, activate):
    try:
        cursor = connection.cursor()
        cursor.execute("EXEC urls.ToggleLoggerTableTriggers ?", activate)
        connection.commit()
    except Exception as e:
        print("Error toggling logger triggers:", e)


def attempt_update_logger_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE urls.LoggerTable SET Details = 'Test' WHERE ID = 1;")
        connection.commit()
    except Exception as e:
        print("Update LoggerTable attempt failed:", e)


def attempt_delete_from_logger_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM urls.LoggerTable WHERE ID = 1;")
        connection.commit()
    except Exception as e:
        print("Delete from LoggerTable attempt failed:", e)


def attempt_alter_logger_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE urls.LoggerTable ADD TestColumn NVARCHAR(50);")
        connection.commit()
    except Exception as e:
        print("Alter LoggerTable attempt failed:", e)


def attempt_drop_logger_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE urls.LoggerTable;")
        connection.commit()
    except Exception as e:
        print("Drop LoggerTable attempt failed:", e)


def delete_expired_links(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("EXEC urls.DeleteExpiredLinks;")
        connection.commit()
    except Exception as e:
        print("Error deleting expired links:", e)


# Admin

def authenticate_user(username, password):
    connection = conn.connect()
    if not connection:
        return False, False

    cursor = connection.cursor()
    result = cursor.execute(
        "DECLARE @IsAuthenticated BIT, @IsAdmin BIT; EXEC urls.AuthenticateUser ?, ?, @IsAuthenticated OUTPUT, @IsAdmin OUTPUT; SELECT @IsAuthenticated, @IsAdmin;",
        username, password).fetchone()
    connection.close()
    return result[0] == 1, result[1] == 1


def create_user(username, password, is_admin):
    connection = conn.connect()
    if not connection:
        return False

    cursor = connection.cursor()
    print(username, password)
    cursor.execute("EXEC urls.CreateUser ?, ?, ?", username, password, is_admin)
    connection.commit()
    connection.close()
    return True
