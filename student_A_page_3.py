import sqlite3

class WeatherStationAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_stations(self):
        return self.execute_query("SELECT DISTINCT site_id, name FROM weather_station ORDER BY name;")

    def get_station_name(self, station_id):
        result = self.execute_query("SELECT name FROM weather_station WHERE site_id = ?;", (station_id,))
        return result[0][0] if result else "Unknown Station"

    def get_average_by_period(self, period, metric):
        start_year, end_year = map(int, period.split("-"))
        value_expr = "(MaxTemp + MinTemp)/2" if metric == "AverageTemp" else metric
        query = f"""
            SELECT Location, ROUND(AVG(CAST({value_expr} AS FLOAT)), 2)
            FROM weather_data
            WHERE CAST(SUBSTR(DMY, 7, 4) AS INTEGER) BETWEEN {start_year} AND {end_year}
            AND {value_expr} IS NOT NULL
            GROUP BY Location;
        """
        result = self.execute_query(query)
        return dict(result)

    def get_station_data(self, station_id, period, metric):
        start_year, end_year = map(int, period.split("-"))
        value_expr = "(MaxTemp + MinTemp)/2" if metric == "AverageTemp" else metric
        query = f"""
            SELECT COUNT({value_expr}), ROUND(AVG(CAST({value_expr} AS FLOAT)), 2)
            FROM weather_data
            WHERE Location = ?
            AND CAST(SUBSTR(DMY, 7, 4) AS INTEGER) BETWEEN ? AND ?
            AND {value_expr} IS NOT NULL;
        """
        result = self.execute_query(query, (station_id, start_year, end_year))
        count, avg = result[0] if result else (0, None)
        return avg if count >= 50 else None


def generate_html_page(form_data, analyzer):
    stations = analyzer.get_stations()
    station_options = "".join([f'<option value="{sid}">{name}</option>' for sid, name in stations])
    metric_options = {
        "MaxTemp": "Max Temperature",
        "MinTemp": "Min Temperature",
        "Rainfall": "Rainfall",
        "AverageTemp": "Average Temperature"
    }
    result_html = ""

    if form_data:
        try:
            station_id = form_data.get("station", [""])[0]
            metric = form_data.get("metric", ["MaxTemp"])[0]
            p1_start = int(form_data.get("period1_start", ["2005"])[0])
            p1_end = int(form_data.get("period1_end", ["2009"])[0])
            p2_start = int(form_data.get("period2_start", ["2010"])[0])
            p2_end = int(form_data.get("period2_end", ["2014"])[0])
            num_results = int(form_data.get("num_results", ["3"])[0])

            period1 = f"{p1_start}-{p1_end}"
            period2 = f"{p2_start}-{p2_end}"

            ref_name = analyzer.get_station_name(station_id)
            ref_avg1 = analyzer.get_station_data(station_id, period1, metric)
            ref_avg2 = analyzer.get_station_data(station_id, period2, metric)

            if ref_avg1 is None or ref_avg2 is None:
                avg1 = analyzer.get_average_by_period(period1, metric)
                avg2 = analyzer.get_average_by_period(period2, metric)

                invalid_rows = ""
                all_sites = set(site for site, _ in stations)
                missing_sites = all_sites - (set(avg1.keys()) & set(avg2.keys()))
                for site in missing_sites:
                    name = analyzer.get_station_name(site)
                    reason = []
                    if site not in avg1:
                        reason.append("Missing in Period 1")
                    if site not in avg2:
                        reason.append("Missing in Period 2")
                    reason_str = ", ".join(reason)
                    invalid_rows += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{reason_str}</td>
                        </tr>
                    """

                invalid_table = ""
                if invalid_rows:
                    invalid_table = f"""
                        <h3>Stations with Insufficient Data</h3>
                        <p><small>These stations had fewer than 50 valid records in one or both time periods.</small></p>
                        <table border="1" cellpadding="5" style="background:#fff;">
                            <tr>
                                <th>Station</th>
                                <th>Issue</th>
                            </tr>
                            {invalid_rows}
                        </table>
                    """

                result_html = f"""
                    <h2>Insufficient Data</h2>
                    <p>The selected reference station <strong>{ref_name}</strong> does not have enough data for the chosen time periods.</p>
                    <p>Please try a different station or select different start and end years with more available records.</p>
                    <p><small>Note: A minimum of 50 valid records per period is required for comparison.</small></p>
                    {invalid_table}
                """
                return wrap_page(result_html, station_options, metric_options)

            avg1 = analyzer.get_average_by_period(period1, metric)
            avg2 = analyzer.get_average_by_period(period2, metric)

            avg1[station_id] = ref_avg1
            avg2[station_id] = ref_avg2

            ref_change = round(((ref_avg2 - ref_avg1) / ref_avg1) * 100, 2)

            percent_changes = {}
            for site in set(avg1) & set(avg2):
                if avg1[site] != 0:
                    change = ((avg2[site] - avg1[site]) / avg1[site]) * 100
                    percent_changes[site] = round(change, 2)

            percent_changes[station_id] = ref_change

            similarity_list = [
                (site, change, round(change - ref_change, 2), avg1.get(site), avg2.get(site))
                for site, change in percent_changes.items()
            ]
            similarity_list.sort(key=lambda x: abs(x[2]))
            similarity_list = [entry for entry in similarity_list if str(entry[0]) != str(station_id)]

            unit = "mm" if metric == "Rainfall" else "degrees C"
            metric_label = metric_options[metric]

            reference_row = f"""
                <tr class="selected-station">
                    <td><span style="color: red;"><em>{ref_name}</em></span></td>
                    <td><span style="color: red;"><em>{f"{ref_avg1:.2f} {unit}"}</em></span></td>
                    <td><span style="color: red;"><em>{f"{ref_avg2:.2f} {unit}"}</em></span></td>
                    <td><span style="color: red;"><em>{f"{ref_change:.2f}%"}</em></span></td>
                    <td><span style="color: red;"><em>+0.00% (selected)</em></span></td>
                </tr>
            """

            other_rows = ""
            count = 0
            for site, change, diff, a1, a2 in similarity_list:
                if count >= num_results:
                    break
                count += 1
                name = analyzer.get_station_name(site)
                other_rows += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{f"{a1:.2f} {unit}" if a1 is not None else "N/A"}</td>
                        <td>{f"{a2:.2f} {unit}" if a2 is not None else "N/A"}</td>
                        <td>{f"{change:.2f}%" if change is not None else "N/A"}</td>
                        <td>{f"{diff:+.2f}%" if diff is not None else "N/A"}</td>
                    </tr>
                """

            table_rows = reference_row + other_rows
            result_html = f"""
                <h2>Top {num_results} Similar Stations to {ref_name}</h2>
                <p>Comparing {metric_label} changes from {p1_start} to {p1_end} and {p2_start} to {p2_end}</p>
                <p><small><em>If results for {ref_name} display N/A there is insufficient data collected. Results only shown for stations with at least 50 valid records per period.</em></small></p>
                <table border="1" cellpadding="5" style="background:white;">
                    <tr>
                        <th>Station</th>
                        <th>{p1_start}-{p1_end}</th>
                        <th>{p2_start}-{p2_end}</th>
                        <th>% Change</th>
                        <th>% Diff from {ref_name}</th>
                    </tr>
                    {table_rows}
                </table>
            """

            # Add invalid stations table below results
            invalid_rows = ""
            all_sites = set(site for site, _ in stations)
            missing_sites = all_sites - (set(avg1.keys()) & set(avg2.keys()))
            for site in missing_sites:
                name = analyzer.get_station_name(site)
                reason = []
                if site not in avg1:
                    reason.append("Missing in Period 1")
                if site not in avg2:
                    reason.append("Missing in Period 2")
                reason_str = ", ".join(reason)
                invalid_rows += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{reason_str}</td>
                    </tr>
                """
            if invalid_rows:
                result_html += f"""
                    <h3>Stations with Insufficient Data</h3>
                    <p><small>These stations had fewer than 50 valid records in one or both time periods.</small></p>
                    <table border="1" cellpadding="5" style="background:#fff;">
                        <tr>
                            <th>Station</th>
                            <th>Issue</th>
                        </tr>
                        {invalid_rows}
                    </table>
                """

        except Exception as e:
            result_html = f"<p class='error'>Error: {str(e)}</p>"

    return wrap_page(result_html, station_options, metric_options)


def wrap_page(content, station_options, metric_options):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Station Similarity</title>
        <link rel="stylesheet" href="A_page3.css">
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

        <h1>Compare Weather Station Climate Trends</h1>
        <h4>Select a weather station of your choice and analyse its change over a specified period of time.</h4>

        <form method="get">
            <label>Reference Station:</label>
            <select name="station">{station_options}</select><br><br>
            <label>Climate Metric:</label>
            <select name="metric">
                {''.join([f'<option value="{k}">{v}</option>' for k, v in metric_options.items()])}
            </select><br><br>
            <label>Period 1 Start Year:</label><input type="number" name="period1_start" value="2005">
            <label>End Year:</label><input type="number" name="period1_end" value="2009"><br><br>
            <label>Period 2 Start Year:</label><input type="number" name="period2_start" value="2010">
            <label>End Year:</label><input type="number" name="period2_end" value="2014"><br><br>
            <label>Number of Similar Results:</label>
            <input type="number" name="num_results" value="3" min="1" max="10"><br><br>
            <input type="submit" value="Compare">
        </form>

        <div class="results">
            {content}
        </div>
    </body>
    </html>
    """


def get_page_html(form_data):
    analyzer = WeatherStationAnalyzer("database/climate.db")
    return generate_html_page(form_data, analyzer)

