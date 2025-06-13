import sqlite3

class ClimateMetricAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_all_metrics(self):
        return ["Precipitation", "MaxTemp", "MinTemp", "Evaporation", "Sunshine"]

    def get_total_for_period(self, metric, start_year, end_year):
        query = f"""
            SELECT ROUND(SUM(CAST({metric} AS FLOAT)), 2)
            FROM weather_data
            WHERE CAST(SUBSTR(DMY, 7, 4) AS INTEGER) BETWEEN ? AND ?
            AND {metric} IS NOT NULL;
        """
        result = self.execute_query(query, (start_year, end_year))
        return result[0][0] if result and result[0][0] is not None else 0.0


def generate_similarity_html(form_data, analyzer):
    metric_options = analyzer.get_all_metrics()
    result_html = ""

    if form_data:
        try:
            ref_metric = form_data.get("reference_metric", ["Precipitation"])[0]
            period1_start = int(form_data.get("period1_start", ["2005"])[0])
            period1_end = int(form_data.get("period1_end", ["2009"])[0])
            period2_start = int(form_data.get("period2_start", ["2010"])[0])
            period2_end = int(form_data.get("period2_end", ["2015"])[0])
            num_results = int(form_data.get("num_results", ["3"])[0])

            changes = []
            ref_total1 = analyzer.get_total_for_period(ref_metric, period1_start, period1_end)
            ref_total2 = analyzer.get_total_for_period(ref_metric, period2_start, period2_end)

            if ref_total1 == 0:
                return "<p>Reference metric has insufficient data in period 1.</p>"

            ref_change = round(((ref_total2 - ref_total1) / ref_total1) * 100, 2)

            for metric in metric_options:
                total1 = analyzer.get_total_for_period(metric, period1_start, period1_end)
                total2 = analyzer.get_total_for_period(metric, period2_start, period2_end)
                if total1 == 0:
                    continue
                change = round(((total2 - total1) / total1) * 100, 2)
                diff = round(change - ref_change, 2)
                changes.append((metric, total1, total2, change, diff))

            changes.sort(key=lambda x: abs(x[4]))

            reference_row = f"""
                <tr style="color:red;">
                    <td>{ref_metric}</td>
                    <td>{ref_total1}</td>
                    <td>{ref_total2}</td>
                    <td>{ref_change:+.2f}%</td>
                    <td>0.00% (selected)</td>
                </tr>
            """

            other_rows = ""
            count = 0
            for metric, t1, t2, change, diff in changes:
                if metric == ref_metric:
                    continue
                if count >= num_results:
                    break
                count += 1
                other_rows += f"""
                    <tr>
                        <td>{metric}</td>
                        <td>{t1}</td>
                        <td>{t2}</td>
                        <td>{change:+.2f}%</td>
                        <td>{diff:+.2f}%</td>
                    </tr>
                """

            result_html = f"""
                <h2>Similarity of Climate Metrics</h2>
                <p>Comparing {ref_metric} with other metrics over two periods:</p>
                <table border="1" cellpadding="5" style="background:white;">
                    <tr>
                        <th>Metric Name</th>
                        <th>Total ({period1_start}–{period1_end})</th>
                        <th>Total ({period2_start}–{period2_end})</th>
                        <th>% Change</th>
                        <th>Difference from {ref_metric}</th>
                    </tr>
                    {reference_row}
                    {other_rows}
                </table>
            """
        except Exception as e:
            result_html = f"<p>Error: {str(e)}</p>"

    metric_select_html = "".join([f'<option value="{m}">{m}</option>' for m in metric_options])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Climate Metric Similarity</title>
        <link rel="stylesheet" href="B_page3.css">
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

        <div class="container">
            <h1>Explore Similar Climate Metrics</h1>
            <form method="get">
                <label>Reference Metric:</label>
                <select name="reference_metric">{metric_select_html}</select><br><br>

                <label>Period 1 Start Year:</label>
                <input type="number" name="period1_start" value="2005">
                <label>End Year:</label>
                <input type="number" name="period1_end" value="2009"><br><br>

                <label>Period 2 Start Year:</label>
                <input type="number" name="period2_start" value="2010">
                <label>End Year:</label>
                <input type="number" name="period2_end" value="2015"><br><br>

                <label>Number of Similar Metrics:</label>
                <input type="number" name="num_results" value="3"><br><br>

                <input type="submit" value="Compare">
            </form>
            <hr>
            {result_html}
        </div>

        <div class="footer">
            <p>Python Programming Studio Assignment - WORKING APPLICATION</p>
        </div>
    </body>
    </html>
    """


# Entry function
def get_page_html(form_data):
    analyzer = ClimateMetricAnalyzer("database/climate.db")
    return generate_similarity_html(form_data, analyzer)
