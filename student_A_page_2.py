import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html = """
    <!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" href="style.css">
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
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet pretium urna.</p>
        </div>

        <div class="column middle">
            <h2>Weather Stations</h2>
    """

    sql_query = "SELECT * FROM state;"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)

    page_html += """
        <form action="/weather-stations" method="get">
            <label for="state">Choose a state:</label>
            <select id="state" name="state">
                <option value="">Select State</option>
    """

    for row in results:
        selected = ""
        if "state" in form_data and form_data["state"][0] == str(row[0]):
            selected = "selected"
        page_html += f'<option value="{row[0]}" {selected}>{row[1]}</option>'

    page_html += "</select> <br><br>"

    lat_start = form_data.get("lat_start", [""])[0]
    lat_end = form_data.get("lat_end", [""])[0]

    page_html += f'<label for="lat_start">Latitude start:</label> '
    page_html += f'<input type="number" step="0.01" id="lat_start" name="lat_start" value="{lat_start}"><br><br>'

    page_html += f'<label for="lat_end">Latitude end:</label> '
    page_html += f'<input type="number" step="0.01" id="lat_end" name="lat_end" value="{lat_end}"><br><br>'

    page_html += '<label for="var_order">Order by:</label>'
    page_html += '<select id="var_order" name="var_order">'
    page_html += '<option value="">...</option>'
    page_html += '<option value="station">station name</option>'
    page_html += '<option value="region">region</option>'
    page_html += '<option value="latitude">latitude</option>'
    page_html += '<option value="longitude">longitude</option>'
    page_html += '</select>'

    page_html += '<select id="order" name="order">'
    page_html += '<option value="">...</option>'
    page_html += '<option value="ASC">A..Z</option>'
    page_html += '<option value="DESC">Z..A</option>'
    page_html += '</select>'

    page_html += '<input type="submit" value="Submit" />'
    page_html += '</form><div>'

    if "state" in form_data:
        page_html += "<h2>Submitted Data:</h2><ul>"
        for key, value in form_data.items():
            page_html += f"<li>{key}: {value}</li>"
        page_html += "</ul>"

        page_html += "<h2>" + getStateName(form_data["state"][0]) + "</h2><ul>"
        page_html += displayStateTable(form_data)

    page_html += """
        </div>  <!-- End div results-->
     </div>  <!-- End column middle -->
    </div>   <!-- End row-->  
    </div>  <!-- end content -->

    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>

    </body>
    </html>
    """
    return page_html


def getStateName(id):
    sql_query = "SELECT name FROM state WHERE state.id = " + str(id) + ";"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)
    for row in results:
        return row[0]


def displayStateTable(form_data):
    temp_html = ""
    if form_data:
        sql_query = build_query_weather_station(form_data)
        results = pyhtml.get_results_from_query("database/climate.db", sql_query)

        temp_html += "<table class='styled-table'>"
        temp_html += "<thead><tr><th>Station ID</th><th>Station name</th><th>Region</th><th>Latitude : Longitude</th></tr></thead>"

        for row in results:
            station_id = str(row[0])
            station_name = str(row[1])
            region_name = str(row[2])
            latitude = str(row[3])
            longitude = str(row[4])
            temp_html += f"<tr><td>{station_id}</td><td>{station_name}</td><td>{region_name}</td><td>{latitude} : {longitude}</td></tr>"

        temp_html += "</table>"
    return temp_html


def build_query_weather_station(form_data):
    base_query = """
        SELECT
            weather_station.site_id AS station_id,
            weather_station.name AS station_name,
            region.name AS region_name,
            weather_station.latitude,
            weather_station.longitude
        FROM
            weather_station
        JOIN region ON weather_station.region_id = region.id
        JOIN state ON weather_station.state_id = state.id
    """
    conditions = []
    order_by = ""

    if "state" in form_data:
        try:
            state_id = int(form_data["state"][0])
            conditions.append(f"state.id = {state_id}")
        except ValueError:
            pass

    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            conditions.append(f"weather_station.latitude BETWEEN {lat_start} AND {lat_end}")
        except ValueError:
            pass

    if "var_order" in form_data:
        sort_fields = {
            "latitude": "weather_station.latitude",
            "longitude": "weather_station.longitude",
            "station": "weather_station.name",
            "region": "region.name"
        }
        user_choice = form_data["var_order"][0]
        if user_choice in sort_fields:
            direction = "ASC"
            if "order" in form_data and form_data["order"][0].upper() in ["ASC", "DESC"]:
                direction = form_data["order"][0].upper()
            order_by = f"ORDER BY {sort_fields[user_choice]} {direction}"

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    final_query = f"{base_query} {where_clause} {order_by};"
    return final_query
