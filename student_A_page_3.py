import pyhtml

def get_page_html(form_data):
    print("About to return Similarity Page...")
    db_path = "database/climate.db"

    # Fetch station names for dropdown
    stations = pyhtml.get_results_from_query(db_path, "SELECT DISTINCT name, site_id FROM weather_station ORDER BY name;")
    metrics = ['MaxTemp', 'MinTemp', 'Evaporation', 'Precipitation']  # Extend if needed

    # --- HTML start ---
    page_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Similar Weather Stations</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="header">
            <h1>Find Similar Weather Stations</h1>
        </div>

        <div class="topnav">
            <a href="/">Home</a>
            <a href="/mission">Mission Statement</a>
            <a href="/weather-stations">Weather Stations</a>
        </div>

        <div class="content">
            <form method="get" action="/weather-stations-similar">
                <label for="ref_station">Reference Station:</label>
                <select name="ref_station" id="ref_station">
    """
    for name, site_id in stations:
        selected = "selected" if form_data.get("ref_station", [""])[0] == str(site_id) else ""
        page_html += f'<option value="{site_id}" {selected}>{name}</option>'

    page_html += "</select><br><br>"

    # Year range selectors
    year_inputs = [("start1", "Start Year (Period 1)"), ("end1", "End Year (Period 1)"),
                   ("start2", "Start Year (Period 2)"), ("end2", "End Year (Period 2)")]
    for key, label in year_inputs:
        val = form_data.get(key, [""])[0]
        page_html += f'<label for="{key}">{label}:</label> '
        page_html += f'<input type="number" name="{key}" value="{val}"><br><br>'

    # Metric
    page_html += '<label for="metric">Metric:</label><select name="metric" id="metric">'
    for metric in metrics:
        selected = "selected" if form_data.get("metric", [""])[0] == metric else ""
        page_html += f'<option value="{metric}" {selected}>{metric}</option>'
    page_html += '</select><br><br>'

    # Number of similar stations
    k_val = form_data.get("top_k", ["3"])[0]
    page_html += f'<label for="top_k">How many similar stations?</label> '
    page_html += f'<input type="number" name="top_k" value="{k_val}" min="1"><br><br>'

    page_html += '<input type="submit" value="Find Similar Stations">'
    page_html += '</form>'

    # If form submitted, display results
    if "ref_station" in form_data:
        results = get_similar_stations(form_data, db_path)
        page_html += "<h2>Similar Weather Stations:</h2>"
        page_html += "<table class='styled-table'><thead><tr><th>Station</th><th>Period 1 Avg</th><th>Period 2 Avg</th><th>% Change</th><th>Difference from Ref</th></tr></thead><tbody>"
        for row in results:
            page_html += f"<tr><td>{row['name']}</td><td>{row['avg1']:.2f}</td><td>{row['avg2']:.2f}</td><td>{row['change']:.2f}%</td><td>{row['diff']:.2f}%</td></tr>"
        page_html += "</tbody></table>"

    page_html += "</div></body></html>"
    return page_html


def get_similar_stations(form_data, db_path):
    ref_station = int(form_data["ref_station"][0])
    start1, end1 = int(form_data["start1"][0]), int(form_data["end1"][0])
    start2, end2 = int(form_data["start2"][0]), int(form_data["end2"][0])
    metric = form_data["metric"][0]
    top_k = int(form_data["top_k"][0])

    # Helper SQL to compute averages per period per station
    sql = f"""
        WITH period_avgs AS (
            SELECT
                ws.name,
                wd.Location,
                AVG(CASE WHEN CAST(SUBSTR(wd.DMY, -4) AS INT) BETWEEN {start1} AND {end1} THEN wd.{metric} ELSE NULL END) AS avg1,
                AVG(CASE WHEN CAST(SUBSTR(wd.DMY, -4) AS INT) BETWEEN {start2} AND {end2} THEN wd.{metric} ELSE NULL END) AS avg2
            FROM weather_data wd
            JOIN weather_station ws ON wd.Location = ws.site_id
            WHERE wd.{metric} IS NOT NULL
            GROUP BY wd.Location
        ),
        changes AS (
            SELECT
                name,
                avg1,
                avg2,
                ((avg2 - avg1) / avg1) * 100.0 AS change
            FROM period_avgs
            WHERE avg1 IS NOT NULL AND avg2 IS NOT NULL
        ),
        ref_change AS (
            SELECT change FROM changes WHERE name = (SELECT name FROM weather_station WHERE site_id = {ref_station})
        )
        SELECT
            c.name, c.avg1, c.avg2, c.change,
            ABS(c.change - r.change) AS diff
        FROM changes c, ref_change r
        ORDER BY diff ASC
        LIMIT {top_k + 1};  -- includes the reference station itself
    """
    raw_results = pyhtml.get_results_from_query(db_path, sql)

    # Remove reference station from final list
    ref_name = pyhtml.get_results_from_query(db_path, f"SELECT name FROM weather_station WHERE site_id = {ref_station};")[0][0]
    final = []
    for row in raw_results:
        if row[0] != ref_name:
            final.append({
                "name": row[0],
                "avg1": row[1],
                "avg2": row[2],
                "change": row[3],
                "diff": row[4]
            })
    return final

