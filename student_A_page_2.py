import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="style.css">
        <style>
            .styled-table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            .styled-table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }
            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
            }
            .styled-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>
                <img src="images/global-warming.png" class="top-image" alt="logo" width="75" height="75">
                My Website about climate change
            </h1>
        </div>

        <div class="topnav">
            <a href="/">Home</a>
            <a href="/mission">Mission Statement</a>
            <div class="dropdown">
                <button class="dropbtn">Weather Stations <i class="fa fa-caret-down"></i></button>
                <div class="dropdown-content">
                    <a href="/weather-stations">Climate Information</a>
                    <a href="/weather-stations-similar">Similar stations</a>
                </div>
            </div>
            <a href="#" style="float:right">Help</a>
        </div>

        <div class="content">
            <div class="row">
                <div class="column side">
                    <h2>Column</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
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

    # Add state options
    for row in results:
        selected = "selected" if "state" in form_data and form_data["state"][0] == str(row[0]) else ""
        page_html += f'<option value="{row[0]}" {selected}>{row[1]}</option>'

    # Add latitude inputs
    lat_start = form_data.get("lat_start", [""])[0]
    lat_end = form_data.get("lat_end", [""])[0]

    page_html += f"""
        </select><br><br>
        <label for="lat_start">Latitude start:</label>
        <input type="number" step="0.01" id="lat_start" name="lat_start" value="{lat_start}"><br><br>
        <label for="lat_end">Latitude end:</label>
        <input type="number" step="0.01" id="lat_end" name="lat_end" value="{lat_end}"><br><br>
    """

    # Add ordering options
    page_html += """
        <label for="var_order">Order:</label>
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

    # Display results if state is selected
    if "state" in form_data:
        state_name = getStateName(form_data["state"][0])
        page_html += f"<h2>{state_name}</h2>"
        page_html += displayStateTable(form_data)

    # Close all divs and add footer
    page_html += """
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>
    </body>
    </html>
    """
    return page_html

def getStateName(id):
    sql_query = f"SELECT name FROM state WHERE state.id = {id}"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)
    return results[0][0] if results else ""

def displayStateTable(form_data):
    if not form_data:
        return ""

    # Query for Table 1 - Weather Station Details
    sql_query_stations = """
        SELECT 
            weather_station.site_id as site,
            weather_station.name,
            region.name as region,
            weather_station.latitude
        FROM weather_station
        JOIN region ON weather_station.region_id = region.id
        WHERE weather_station.state_id = """ + form_data["state"][0]

    # Add latitude filter if provided
    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            sql_query_stations += f" AND weather_station.latitude BETWEEN {lat_start} AND {lat_end}"
        except ValueError:
            pass

    # Add ordering if provided
    if "var_order" in form_data and "order" in form_data:
        sort_fields = {
            "station": "weather_station.name",
            "region": "region.name",
            "latitude": "weather_station.latitude"
        }
        if form_data["var_order"][0] in sort_fields:
            direction = form_data["order"][0] if form_data["order"][0] in ["ASC", "DESC"] else "ASC"
            sql_query_stations += f" ORDER BY {sort_fields[form_data['var_order'][0]]} {direction}"

    # Query for Table 2 - Regional Summary

    # Query for Table 2 - Regional Summary
    sql_query_summary = """
        SELECT 
            region.name as region,
            COUNT(DISTINCT weather_station.site_id) as station_count,
            AVG(weather_data.MaxTemp) as avg_max_temp
        FROM region
        JOIN weather_station ON region.id = weather_station.region_id
        LEFT JOIN weather_data ON weather_station.site_id = weather_data.location
        WHERE weather_station.state_id = """ + form_data["state"][0]

    # Add latitude filter to summary if provided
    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            sql_query_summary += f" AND weather_station.latitude BETWEEN {lat_start} AND {lat_end}"
        except ValueError:
            pass

    sql_query_summary += " GROUP BY region.name"

    # Get results for both tables
    station_results = pyhtml.get_results_from_query("database/climate.db", sql_query_stations)
    summary_results = pyhtml.get_results_from_query("database/climate.db", sql_query_summary)

    # Build HTML for Table 1
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

    # Build HTML for Table 2
    table2_html = """
        <h3>Regional Summary</h3>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Number Weather Stations</th>
                    <th>Average Max Temperature</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in summary_results:
        avg_temp = 'N/A' if row[2] is None else f"{float(row[2]):.1f}"
        table2_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{avg_temp}</td>
            </tr>
        """

    table2_html += "</tbody></table>"

    return table1_html + table2_html

def build_query_weather_station(form_data):
    base_query = """
        SELECT
            weather_station.name AS station_name,
            region.name AS region_name,
            weather_station.latitude,
            weather_station.longitude
        FROM weather_station
        JOIN region ON weather_station.region_id = region.id
        JOIN state ON weather_station.state_id = state.id
    """
    
    conditions = []
    
    # Add state condition
    if "state" in form_data:
        try:
            state_id = int(form_data["state"][0])
            conditions.append(f"state.id = {state_id}")
        except ValueError:
            pass

    # Add latitude range condition
    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            conditions.append(f"weather_station.latitude BETWEEN {lat_start} AND {lat_end}")
        except ValueError:
            pass

    # Add ordering
    order_by = ""
    if "var_order" in form_data:
        sort_fields = {
            "latitude": "weather_station.latitude",
            "station": "weather_station.name",
            "region": "region.name"
        }
        user_choice = form_data["var_order"][0]
        if user_choice in sort_fields:
            direction = form_data.get("order", ["ASC"])[0].upper()
            if direction not in ["ASC", "DESC"]:
                direction = "ASC"
            order_by = f"ORDER BY {sort_fields[user_choice]} {direction}"

    # Combine query parts
    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    final_query = f"{base_query} {where_clause} {order_by};"
    
    return final_query
