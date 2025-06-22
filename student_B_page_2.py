import sqlite3

class ClimateMetricAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_metrics(self):
        return {
            "Rainfall": "Rainfall",
            "MaxTemp": "Maximum Temperature",
            "MinTemp": "Minimum Temperature",
            "SolarRadiation": "Solar Radiation",
            "AverageTemp": "Average Temperature"
        }

    def get_daily_metric_data(self, metric, station_start, station_end, date_start, date_end):
        value_expr = "(MaxTemp + MinTemp) / 2" if metric == "AverageTemp" else metric
        query = f"""
            SELECT Location, DMY, ROUND(CAST({value_expr} AS FLOAT), 2)
            FROM weather_data
            WHERE Location BETWEEN ? AND ?
              AND DMY BETWEEN ? AND ?
              AND {value_expr} IS NOT NULL
            ORDER BY DMY ASC
        """
        return self.execute_query(query, (station_start, station_end, date_start, date_end))

    def get_state_summary(self, metric, month, year):
        value_expr = "(MaxTemp + MinTemp) / 2" if metric == "AverageTemp" else metric
        query = f"""
            SELECT s.name, ROUND(SUM(CAST({value_expr} AS FLOAT)), 2)
            FROM weather_data w
            JOIN weather_station ws ON w.Location = ws.site_id
            JOIN state s ON ws.state_id = s.id
            WHERE SUBSTR(DMY, 4, 2) = ? AND SUBSTR(DMY, 7, 4) = ?
              AND {value_expr} IS NOT NULL
            GROUP BY s.name
            ORDER BY s.name
        """
        return self.execute_query(query, (month.zfill(2), year))


def generate_html_page(form_data, analyzer):
    metrics = analyzer.get_metrics()
    result_html = ""

    if form_data:
        try:
            metric = form_data.get("metric", ["Rainfall"])[0]
            station_start = int(form_data.get("station_start", ["3000"])[0])
            station_end = int(form_data.get("station_end", ["4000"])[0])
            date_start = form_data.get("start_date", ["1970-01-01"])[0]
            date_end = form_data.get("end_date", ["1970-01-03"])[0]
            summary_month = form_data.get("summary_month", ["05"])[0]
            summary_year = form_data.get("summary_year", ["2005"])[0]

            rows = analyzer.get_daily_metric_data(metric, station_start, station_end, date_start, date_end)
            unit = "mm" if metric == "Rainfall" else "°C"
            label = metrics[metric]

            table_rows = "".join(
                f"<tr><td>{sid}</td><td>{dmy}</td><td>{val:.2f} {unit}</td></tr>"
                for sid, dmy, val in rows
            )

            result_html += f"""
                <h2>Daily {label}</h2>
                <table border="1" cellpadding="5" style="background:#fff; width:100%;">
                    <thead>
                        <tr>
                            <th>Station ID</th>
                            <th>Date</th>
                            <th>{label}</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
            """

            summary = analyzer.get_state_summary(metric, summary_month, summary_year)
            summary_rows = "".join(
                f"<tr><td>{state}</td><td>{total:.2f} {unit}</td></tr>"
                for state, total in summary
            )
            result_html += f"""
                <h2>Summary: Total {label} for {summary_month}/{summary_year}</h2>
                <table border="1" cellpadding="5" style="background:#f4f4f4; width:60%;">
                    <thead><tr><th>State</th><th>Total</th></tr></thead>
                    <tbody>{summary_rows}</tbody>
                </table>
            """
        except Exception as e:
            result_html = f"<p class='error'>Error: {str(e)}</p>"

    metric_options = "".join(
        f'<option value="{k}">{v}</option>' for k, v in metrics.items()
    )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Climate Metric Viewer</title>
        <link rel="stylesheet" href="B_page2.css">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                padding: 40px;
            }}
            h1, h2 {{
                color: #2c3e50;
            }}
            form {{
                background: #fff;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            label {{
                display: inline-block;
                width: 180px;
                margin-top: 10px;
            }}
            input, select {{
                padding: 6px;
                margin: 8px 0;
                width: 200px;
            }}
            table {{
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ccc;
            }}
            th {{
                background-color: #e0e0e0;
            }}
            .topnav {{
                background-color: #333;
                overflow: hidden;
                margin-bottom: 30px;
            }}
            .nav-links a {{
                float: left;
                display: block;
                color: #f2f2f2;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }}
            .nav-links a:hover {{
                background-color: #ddd;
                color: black;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 0.9em;
                text-align: center;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="topnav">
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/mission">Our Mission</a>
                <a href="/weather-stations">Climate Change based on Weather Station</a>
                <a href="/metrics">Climate Change based on Climate Metric</a>
                <a href="/weather-stations-similar">Similar Station Metrics</a>
                <a href="/metrics-similar">Similar Climate Metrics</a>
            </div>
        </div>

        <h1>View Climate Metric by Station</h1>
        <form method="get">
            <label>Climate Metric:</label>
            <select name="metric">{metric_options}</select><br>

            <label>Start Station ID:</label>
            <input type="number" name="station_start" value="3000"><br>

            <label>End Station ID:</label>
            <input type="number" name="station_end" value="4000"><br>

            <label>Start Date:</label>
            <input type="date" name="start_date" value="1970-01-01"><br>

            <label>End Date:</label>
            <input type="date" name="end_date" value="1970-01-03"><br>

            <label>Summary Month:</label>
            <input type="text" name="summary_month" value="05"><br>

            <label>Summary Year:</label>
            <input type="text" name="summary_year" value="2005"><br>

            <input type="submit" value="Get Data">
        </form>

        <div class="results">
            {result_html}
        </div>

        <div class="footer">
            <p>Python Programming Studio Assignment - WORKING APPLICATION</p>
        </div>
    </body>
    </html>
    """

def get_page_html(form_data):
    analyzer = ClimateMetricAnalyzer("database/climate.db")
    return generate_html_page(form_data, analyzer)

