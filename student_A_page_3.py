import pyhtml

def get_page_html(form_data):
    print("About to return Similarity Page...")
    db_path = "database/climate.db"

    # Dropdown options
    stations = pyhtml.get_results_from_query(db_path, "SELECT DISTINCT name, site_id FROM weather_station ORDER BY name;")
    metrics = ['MaxTemp', 'MinTemp', 'Rainfall']

    page_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Find Similar Weather Stations</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }
            .header {
                background-color: #fff;
                padding: 20px;
                text-align: center;
            }
            .topnav {
                background-color: #333;
                overflow: hidden;
                margin-bottom: 20px;
            }
            .topnav a {
                float: left;
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                font-size: 17px;
            }
            .topnav a:hover {
                background-color: #ddd;
                color: black;
            }
            .content {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            label {
                font-weight: bold;
                margin-bottom: 5px;
            }
            select, input {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                width: 100%;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: auto;
            }
            .styled-table {
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
            }
            .styled-table thead tr {
                background-color: #009879;
                color: white;
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
        </style>
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
    """

    # Reference Station dropdown
    page_html += '<label for="ref_station">Reference Station:</label>'
    page_html += '<select name="ref_station" id="ref_station">'
    for name, site_id in stations:
        selected = "selected" if form_data.get("ref_station", [""])[0] == str(site_id) else ""
        page_html += f'<option value="{site_id}" {selected}>{name}</option>'
    page_html += '</select><br>'

    # Year inputs
    year_inputs = [
        ("start1", "Start Year (Period 1)"),
        ("end1", "End Year (Period 1)"),
        ("start2", "Start Year (Period 2)"),
        ("end2", "End Year (Period 2)")
    ]
    for key, label in year_inputs:
        val = form_data.get(key, [""])[0] or ("2005" if "start1" in key else 
                                             "2009" if "end1" in key else
                                             "2010" if "start2" in key else "2015")
        page_html += f'<label for="{key}">{label}:</label>'
        page_html += f'<input type="number" name="{key}" id="{key}" value="{val}"><br>'

    # Metric selection
    selected_metric = form_data.get("metric", ["MaxTemp"])[0]
    page_html += '<label for="metric">Climate Metric:</label>'
    page_html += '<select name="metric" id="metric">'
    for metric in metrics:
        selected = "selected" if selected_metric == metric else ""
        page_html += f'<option value="{metric}" {selected}>{metric}</option>'
    page_html += '</select><br>'

    # Top K input
    k_val = form_data.get("top_k", ["3"])[0]
    page_html += '<label for="top_k">How many similar stations?</label>'
    page_html += f'<input type="number" name="top_k" id="top_k" value="{k_val}" min="1"><br>'

    page_html += '<input type="submit" value="Find Similar Stations">'
    page_html += '</form>'

    # Results table
    if "ref_station" in form_data:
        results = get_similar_stations(form_data, db_path)
        metric_col = selected_metric

        # Reference row
        ref_station = int(form_data["ref_station"][0])
        ref_details = pyhtml.get_results_from_query(db_path, f"""
            WITH period_avgs AS (
                SELECT
                    ws.name,
                    ROUND(AVG(CASE 
                        WHEN CAST(strftime('%Y', date(substr(wd.DMY, 7, 4) || '-' || 
                                                      substr(wd.DMY, 4, 2) || '-' || 
                                                      substr(wd.DMY, 1, 2))) AS INTEGER) 
                        BETWEEN {form_data['start1'][0]} AND {form_data['end1'][0]} 
                        THEN wd.{metric_col} END), 1) AS avg1,
                    ROUND(AVG(CASE 
                        WHEN CAST(strftime('%Y', date(substr(wd.DMY, 7, 4) || '-' || 
                                                      substr(wd.DMY, 4, 2) || '-' || 
                                                      substr(wd.DMY, 1, 2))) AS INTEGER) 
                        BETWEEN {form_data['start2'][0]} AND {form_data['end2'][0]} 
                        THEN wd.{metric_col} END), 1) AS avg2
                FROM weather_data wd
                JOIN weather_station ws ON wd.Location = ws.site_id
                WHERE ws.site_id = {ref_station}
                GROUP BY ws.name
            )
            SELECT
                name,
                avg1,
                avg2,
                ROUND(((avg2 - avg1) / avg1) * 100.0, 2) AS change
            FROM period_avgs;
        """)

        page_html += "<h2>Similar Weather Stations:</h2>"
        page_html += """
        <table class='styled-table'>
            <thead>
                <tr>
                    <th>Station</th>
                    <th>Period 1 Avg</th>
                    <th>Period 2 Avg</th>
                    <th>% Change</th>
                    <th>Difference from Ref</th>
                </tr>
            </thead>
            <tbody>
        """

        if ref_details:
            ref_name, avg1, avg2, change = ref_details[0]
            page_html += f"""
                <tr>
                    <td>{ref_name} (selected)</td>
                    <td>{avg1:.1f}</td>
                    <td>{avg2:.1f}</td>
                    <td>{'+' if change >= 0 else ''}{change:.2f}%</td>
                    <td>0.00%</td>
                </tr>
            """

        for row in results:
            change_sign = '+' if row['change'] >= 0 else ''
            diff_sign = '+' if row['diff'] >= 0 else ''
            page_html += f"""
                <tr>
                    <td>{row['name']}</td>
                    <td>{row['avg1']:.1f}</td>
                    <td>{row['avg2']:.1f}</td>
                    <td>{change_sign}{row['change']:.2f}%</td>
                    <td>{diff_sign}{row['diff']:.2f}%</td>
                </tr>
            """

        page_html += "</tbody></table>"
    else:
        page_html += "<p>No results found. Please try different parameters.</p>"

    page_html += "</div></body></html>"
    return page_html


def get_similar_stations(form_data, db_path):
    try:
        ref_station = int(form_data["ref_station"][0])
        start1 = int(form_data["start1"][0])
        end1 = int(form_data["end1"][0])
        start2 = int(form_data["start2"][0])
        end2 = int(form_data["end2"][0])
        top_k = int(form_data["top_k"][0])
        metric_col = form_data.get("metric", ["MaxTemp"])[0]

        sql = f"""
            WITH period_avgs AS (
                SELECT
                    ws.name,
                    ws.site_id,
                    ROUND(AVG(CASE 
                        WHEN CAST(strftime('%Y', date(substr(wd.DMY, 7, 4) || '-' || 
                                                      substr(wd.DMY, 4, 2) || '-' || 
                                                      substr(wd.DMY, 1, 2))) AS INTEGER) 
                        BETWEEN {start1} AND {end1} 
                        THEN wd.{metric_col} END), 1) AS avg1,
                    ROUND(AVG(CASE 
                        WHEN CAST(strftime('%Y', date(substr(wd.DMY, 7, 4) || '-' || 
                                                      substr(wd.DMY, 4, 2) || '-' || 
                                                      substr(wd.DMY, 1, 2))) AS INTEGER) 
                        BETWEEN {start2} AND {end2} 
                        THEN wd.{metric_col} END), 1) AS avg2
                FROM weather_data wd
                JOIN weather_station ws ON wd.Location = ws.site_id
                WHERE wd.{metric_col} IS NOT NULL
                GROUP BY ws.site_id
            ),
            changes AS (
                SELECT
                    name,
                    site_id,
                    avg1,
                    avg2,
                    ROUND(((avg2 - avg1) / avg1) * 100.0, 2) AS change
                FROM period_avgs
                WHERE avg1 IS NOT NULL AND avg2 IS NOT NULL AND avg1 != 0
            ),
            ref_change AS (
                SELECT change FROM changes WHERE site_id = {ref_station}
            )
            SELECT
                c.name,
                c.site_id,
                c.avg1,
                c.avg2,
                c.change,
                ROUND(c.change - r.change, 2) AS diff
            FROM changes c, ref_change r
            WHERE c.site_id != {ref_station}
            ORDER BY ABS(diff)
            LIMIT {top_k};
        """

        results = pyhtml.get_results_from_query(db_path, sql)
        return [{
            "name": row[0],
            "avg1": row[2],
            "avg2": row[3],
            "change": row[4],
            "diff": row[5]
        } for row in results]

    except Exception as e:
        print(f"Error in get_similar_stations: {str(e)}")
        return []






