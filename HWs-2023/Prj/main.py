from flask import Flask, request, jsonify, render_template, redirect, session, url_for
import utils
import conn

app = Flask(__name__)

# def main():
#     connection = CRUD.connect()
#     if connection:
#         # CRUD
#         # Insert URL mappings
#         short_url1 = utils.insert_url_mapping(connection, 'http://www.example.com/verylongurl1')
#         short_url2 = utils.insert_url_mapping(connection, 'http://www.example.com/verylongurl2')
#         print(f"Short URL for 'http://www.example.com/verylongurl1': {short_url1}")
#         print(f"Short URL for 'http://www.example.com/verylongurl2': {short_url2}")
#
#         # Read and display URL mappings
#         print("URL Mappings after insertion:")
#         rows = utils.read_url_mappings(connection)
#         for row in rows:
#             print(row)
#
#         # Update a URL mapping
#         utils.update_url_mapping(connection, short_url1, 'http://www.example.com/updatedlongurl1')
#
#         # Read and display URL mappings after update
#         print("URL Mappings after update:")
#         rows = utils.read_url_mappings(connection)
#         for row in rows:
#             print(row)
#
#         # Delete a URL mapping
#         utils.delete_url_mapping(connection, short_url2)
#
#         # Read and display URL mappings after deletion
#         print("URL Mappings after deletion:")
#         rows = utils.read_url_mappings(connection)
#         for row in rows:
#             print(row)
#
#         # DASHBOARD
#         long_url1 = 'https://google2.com'
#         long_url2 = 'https://apple2.com'
#
#         # Handle URLs
#         short_url1 = utils.handle_url(connection, long_url1)
#         short_url2 = utils.handle_url(connection, long_url2)
#
#         print(f"Short URL for '{long_url1}': {short_url1}")
#         print(f"Short URL for '{long_url2}': {short_url2}")
#
#         # Fetch and plot new links registered per day
#         new_links_data = utils.fetch_data(connection, 'urls.GetNewLinksPerDay')
#         utils.plot_new_links_per_day(new_links_data)
#
#         # Fetch and plot visits per day
#         visits_data = utils.fetch_data(connection, 'urls.GetVisitsPerDay')
#         utils.plot_visits_per_day(visits_data)
#
#         # Fetch and plot top 3 most visited short links
#         top3_data = utils.fetch_data(connection, 'urls.GetTop3MostVisited')
#         utils.plot_top3_most_visited(top3_data)
#
#         # Fetch and display all mappings with details
#         all_mappings_data = utils.fetch_data(connection, 'urls.GetAllMappingsWithDetails')
#         utils.display_all_mappings_with_details(all_mappings_data)
#
#         # Triggers
#
#         # Activate the trigger
#         utils.activate_trigger(connection, 1)
#
#         # Attempt table actions (should be prevented)
#         utils.attempt_create_table(connection)
#         utils.attempt_alter_table(connection)
#         utils.attempt_drop_table(connection)
#
#         # Deactivate the trigger
#         utils.activate_trigger(connection, 0)
#
#         # Attempt table actions (should be allowed)
#         utils.attempt_create_table(connection)
#
#         # Activate the logger table triggers
#         utils.activate_logger_triggers(connection, 1)
#
#         # Attempt actions on LoggerTable (should be prevented and logged)
#         utils.attempt_update_logger_table(connection)
#         utils.attempt_delete_from_logger_table(connection)
#         utils.attempt_alter_logger_table(connection)
#         utils.attempt_drop_logger_table(connection)
#
#         # Deactivate the logger table triggers
#         utils.activate_logger_triggers(connection, 0)
#
#         # Attempt actions on LoggerTable (should be allowed)
#         utils.attempt_update_logger_table(connection)
#         utils.attempt_delete_from_logger_table(connection)
#         utils.attempt_alter_logger_table(connection)
#         utils.attempt_drop_logger_table(connection)
#
#         utils.delete_expired_links(connection)
#
#         # Close the connection
#         connection.close()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({"error": "Missing 'long_url' parameter"}), 400

    connection = conn.connect()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    short_url = utils.handle_url(connection, long_url)
    if not short_url:
        connection.close()
        return jsonify({"error": "Invalid URL"}), 400

    connection.close()
    return jsonify({"short_url": short_url})


@app.route('/<short_url>')
def redirect_short_url(short_url):
    connection = conn.connect()
    if not connection:
        return "Failed to connect to the database", 500

    long_url = utils.get_long_url(connection, short_url)
    if long_url:
        utils.record_visit(connection, short_url)
        connection.close()
        return redirect(long_url)
    else:
        connection.close()
        return "URL not found", 404


@app.route('/api/url-stats', methods=['POST'])
def api_url_stats():
    data = request.json
    short_url = data.get('short_url')
    if not short_url:
        long_url = utils.get_long_url()
        if not long_url:
            return jsonify({"error": "Missing 'short_url' parameter"}), 400

        short_url = utils.get_short_url(conn.connect(), long_url)

    connection = conn.connect()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    stats = utils.get_url_statistics(connection, short_url)
    connection.close()

    if stats:
        return jsonify(stats)
    else:
        return jsonify({"error": "URL not found"}), 404


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/new-links')
def api_new_links():
    connection = conn.connect()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = connection.cursor()
    cursor.execute("EXEC urls.GetNewLinksPerDay")
    rows = cursor.fetchall()
    dates = [row[0].strftime('%Y-%m-%d') for row in rows]
    counts = [row[1] for row in rows]
    connection.close()

    return jsonify({"dates": dates, "counts": counts})


@app.route('/api/visits')
def api_visits():
    connection = conn.connect()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = connection.cursor()
    cursor.execute("EXEC urls.GetVisitsPerDay")
    rows = cursor.fetchall()
    dates = [row[0].strftime('%Y-%m-%d') for row in rows]
    counts = [row[1] for row in rows]
    connection.close()

    return jsonify({"dates": dates, "counts": counts})


@app.route('/api/top-links')
def api_top_links():
    connection = conn.connect()
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = connection.cursor()
    cursor.execute("EXEC urls.GetTop3MostVisited")
    rows = cursor.fetchall()
    links = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    connection.close()

    return jsonify({"links": links, "counts": counts})


if __name__ == "__main__":
    app.run(debug=True)
