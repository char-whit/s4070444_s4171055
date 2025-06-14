import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="A_page2.css">
    </head>
    <body>
        <div class="topnav">
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/mission">Our mission</a>
                <a href="/weather-stations">Climate change based on weather station</a>
                <a href="/metrics">Climate change based on climate metric</a>
                <a href="/weather-stations-similar">Similar station metrics</a>
                <a href="/metrics-similar">Similar climate metrics</a>
            </div>
        </div>

        <div class="content">
            <div class="row">
                <div class="column side">
                    <h2>Info</h2>
                    <p>Use the filters below to explore weather station data across Australia. You can select a state, narrow results by latitude range, and choose a climate summary metric such as MaxTemp. The table will display matching weather stations and a regional summary based on your selections.</p>
                </div>
                <div class="column middle">
                    <h2>Weather Stations</h2>
    """

    # Get states from database
    sql_query = "SELECT * FROM state;"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)

    # Create form
    page_html += """
        <form action="/weather-stations" method="get">
            <label for="state">Choose a state:</label>
            <select id="state" name="state">
                <option value="">Select State</option>
    """

    for row in results:
        selected = "selected" if "state" in form_data and form_data["state"][0] == str(row[0]) else ""
        page_html += f'<option value="{row[0]}" {selected}>{row[1]}</option>'

    lat_start = form_data.get("lat_start", [""])[0]
    lat_end = form_data.get("lat_end", [""])[0]
    summary_metric = form_data.get("summary_metric", ["MaxTemp"])[0]

    page_html += f"""
        </select><br><br>
        <label for="lat_start">Latitude start:</label>
        <input type="number" step="1" id="lat_start" name="lat_start" value="{lat_start}"><br><br>
        <label for="lat_end">Latitude end:</label>
        <input type="number" step="1" id="lat_end" name="lat_end" value="{lat_end}"><br><br>

        <label for="summary_metric">Summary Metric:</label>
        <select id="summary_metric" name="summary_metric">
    """

    metrics = ["MaxTemp", "MinTemp", "Precipitation", "Evaporation", "Sunshine"]
    for metric in metrics:
        selected = "selected" if summary_metric == metric else ""
        page_html += f'<option value="{metric}" {selected}>{metric}</option>'

    page_html += """
        </select><br><br>
        <label for="var_order">Order by:</label>
        <select id="var_order" name="var_order">
            <option value="">...</option>
            <option value="station">station name</option>
            <option value="region">region</option>
            <option value="latitude">latitude</option>
        </select>

        <select id="order" name="order">
            <option value="">...</option>
            <option value="ASC">A..Z</option>
            <option value="DESC">Z..A</option>
        </select>

        <input type="submit" value="Submit">
    </form>
    <div>
    """

    if "state" in form_data:
        state_name = getStateName(form_data["state"][0])
        page_html += f"<h2>{state_name}</h2>"
        page_html += displayStateTable(form_data)

    page_html += """
                </div>
            </div>
        </div>
    </div>

<footer style="background-color: #2c3e50; color: white; padding: 40px 20px 20px; text-align: center; font-size: 16px; margin-top: 80px; border-top: 3px solid #4CAF50;">
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 15px;">
        <a href="/" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Home</a>
        <a href="/mission" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Our Mission</a>
        <a href="/weather-stations" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Weather Station Data</a>
        <a href="/metrics" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Climate Metric Data</a>
        <a href="/weather-stations-similar" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Similar Station Metrics</a>
        <a href="/metrics-similar" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Similar Climate Metrics</a>
    </div>
    <p style="font-size: 14px; color: #ccc; margin-top: 10px;">© 2025 Climate Change in Australia | Data from the Australian Bureau of Meteorology</p>
</footer>
    </body>
    </html>
    """
    return page_html

def getStateName(id):
    sql_query = f"SELECT name FROM state WHERE id = {id}"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)
    return results[0][0] if results else ""

def displayStateTable(form_data):
    if not form_data:
        return ""

    summary_metric = form_data.get("summary_metric", ["MaxTemp"])[0]
    allowed_metrics = ["MaxTemp", "MinTemp", "Precipitation", "Evaporation", "Sunshine"]
    if summary_metric not in allowed_metrics:
        summary_metric = "MaxTemp"

    sql_query_stations = f"""
        SELECT 
            weather_station.site_id as site,
            weather_station.name,
            region.name as region,
            weather_station.latitude
        FROM weather_station
        JOIN region ON weather_station.region_id = region.id
        WHERE weather_station.state_id = {form_data["state"][0]}
    """

    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            sql_query_stations += f" AND weather_station.latitude BETWEEN {lat_start} AND {lat_end}"
        except ValueError:
            pass

    if "var_order" in form_data and "order" in form_data:
        sort_fields = {
            "station": "weather_station.name",
            "region": "region.name",
            "latitude": "weather_station.latitude"
        }
        if form_data["var_order"][0] in sort_fields:
            direction = form_data["order"][0] if form_data["order"][0] in ["ASC", "DESC"] else "ASC"
            sql_query_stations += f" ORDER BY {sort_fields[form_data['var_order'][0]]} {direction}"

    sql_query_summary = f"""
        SELECT 
            region.name as region,
            COUNT(DISTINCT weather_station.site_id) as station_count,
            AVG(weather_data.{summary_metric}) as avg_value
        FROM region
        JOIN weather_station ON region.id = weather_station.region_id
        LEFT JOIN weather_data ON weather_station.site_id = weather_data.location
        WHERE weather_station.state_id = {form_data["state"][0]}
    """

    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            sql_query_summary += f" AND weather_station.latitude BETWEEN {lat_start} AND {lat_end}"
        except ValueError:
            pass

    sql_query_summary += " GROUP BY region.name"

    station_results = pyhtml.get_results_from_query("database/climate.db", sql_query_stations)
    summary_results = pyhtml.get_results_from_query("database/climate.db", sql_query_summary)

    table1_html = """
        <h3>Weather Station Details</h3>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Site</th>
                    <th>Name</th>
                    <th>Region</th>
                    <th>Latitude</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in station_results:
        table1_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]:.2f}</td>
            </tr>
        """

    table1_html += "</tbody></table>"

    table2_html = f"""
        <h3>Regional Summary</h3>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Number Weather Stations</th>
                    <th>Average {summary_metric}</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in summary_results:
        avg_value = 'N/A' if row[2] is None else f"{float(row[2]):.1f}"
        table2_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{avg_value}</td>
            </tr>
        """

    table2_html += "</tbody></table>"

    return table1_html + table2_html

