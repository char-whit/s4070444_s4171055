import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""
    <!DOCTYPE html>
    <html>

    <head>
        <!-- Include the external css file -->
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
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet pretium urna. Vivamus venenatis velit nec neque ultricies, eget elementum magna tristique. Quisque vehicula, risus eget aliquam placerat, purus leo tincidunt eros, eget luctus quam orci in velit. Praesent scelerisque tortor sed accumsan convallis.</p>
        </div>
    
        <div class="column middle">

        
            <h2> Weather Stations </h2>
    

                
    """
    sql_query = "select * from state;"
    #Run the query in sql_query and get the results
    results = pyhtml.get_results_from_query("database/climate.db",sql_query) 

    page_html += """
        <form action="/weather-stations" method="get">
            <label for="state">Choose a state:</label>
            <select id="state" name="state">
                <option value="">Select State</option>
    """
    
    #Adding STATE results to the select option
    for row in results:
        selected = ""
        # If form data exists, pre-select the chosen value
        if "state" in form_data and form_data["state"][0] == str(row[0]):
            selected = "selected"
        page_html += '<option value="'+str(row[0]) +'" '+selected+'>'+str(row[1])+'</option>'

    page_html += "</select> <br><br> "

     # --- 2. Latitude Range ---
    lat_start = form_data.get("lat_start", [""])[0]
    lat_end = form_data.get("lat_end", [""])[0]

    page_html += " <label for="'lat_start'">Latitude start:</label> "
    page_html += " <input type="'number'" step="'0.01'" id="'lat_start'" name="'lat_start'" value="+lat_start+"><br><br>"

    page_html += " <label for="'lat_end'">Latitude end:</label> "
    page_html += " <input type="'number'" step="'0.01'" id="'lat_end'" name="'lat_end'" value="+lat_end+"><br><br>"
    
    # --- 3. Order option ---
    page_html += "<label for="'var_order'">Order:</label> "
    page_html += "<select id="'var_order'" name="'var_order'">"
    page_html += "<option value="">...</option>"
    page_html += "<option value="'station'">station name</option>"
    page_html += "<option value="'region'">region</option>"
    page_html += "<option value="'latitude'">latitude</option>"
    page_html += "<option value="'longitude'">longitude</option>"
    page_html += "</select>"

    page_html += "<select id="'order'" name="'order'">"
    page_html += "<option value="">...</option>"
    page_html += "<option value="'ASC'">A..Z</option>"
    page_html += "<option value="'DESC'">Z..A</option>"

    
     # --- Submit Button ---
    page_html += '<input type="submit" value="Submit" />'
    page_html += "</form>"

    page_html+="""
        <div>
    """

    # If a selection was made, show it
     # --- Debug: Show Submitted Info ---
    if ("state") in form_data:
        page_html += "<h2>Submitted Data:</h2><ul>"
        for key, value in form_data.items():
            page_html += f"<li>{key}: {value}</li>"
        page_html += "</ul>"

        page_html += "<h2>"+getStateName(form_data["state"][0])+"</h2><ul>"
        page_html+= displayStateTable(form_data)

   
    """""
        </div>  <!-- End div results-->

     </div>  <!-- End column middle -->
    </div>   <!-- End row-->  
    
    </div>  <!-- end conent -->

    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>

</body>
</html>    

    """
    return page_html #end of main function

# function to retrieve StateName using the id
def getStateName(id):
    sql_query = "SELECT name FROM state WHERE state.id = " + str(id) + ";"
    #Run the query in sql_query and get the results
    results = pyhtml.get_results_from_query("database/climate.db",sql_query)
    for row in results:
        return row[0]

# function to generate HTML table to show weather station data considering user filters and order choices
# state, lat_start, lat_end, region, order_var, order
def displayStateTable(form_data):
    temp_html = ""
    print(form_data)
    if form_data: # the form data returns a dict of only filled in values e.g. {'state': ['8']}
        # gel all weather stations from a specific state (using state id)
        sql_query = build_query_weather_station(form_data)
                
        #Run the query in sql_query and get the results
        results = pyhtml.get_results_from_query("database/climate.db",sql_query)
                
        #Adding results to the web page without any beautification. Try turning it into a nice table!
        temp_html+="<table class="'styled-table'">"
        temp_html+="<thead><tr><th>Station name</th> <th>Region</th> <th> latitude : longitude</th></tr></thead>"

        for row in results:
            temp_html+="<tr><td>"+str(row[0])+"</td> <td>"+str(row[1])+"</td> <td>"+str(row[2])+" : "+str(row[3])+"</td></tr>"
        
        temp_html+="</table>"
    return temp_html


# create function to build query with options from the form data
def build_query_weather_station(form_data):
    base_query = """
        SELECT
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

    # --- Validate state ---
    if "state" in form_data:
        try:
            state_id = int(form_data["state"][0])
            conditions.append(f"state.id = {state_id}")
        except ValueError:
            pass

    # --- Validate Latitude Range ---
    if "lat_start" in form_data and "lat_end" in form_data:
        try:
            lat_start = float(form_data["lat_start"][0])
            lat_end = float(form_data["lat_end"][0])
            conditions.append(f"weather_station.latitude BETWEEN {lat_start} AND {lat_end}")
        except ValueError:
            pass

    # --- Optional: Sorting ---
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
            print(order_by)

    # --- Build WHERE clause if needed ---:
    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # --- Final SQL ---
    final_query = f"{base_query} {where_clause} {order_by};"
    return final_query