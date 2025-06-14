import sqlite3

def get_page_html(form_data):
    # Connect to the climate.db SQLite database
    conn = sqlite3.connect('database/climate.db')
    cursor = conn.cursor()


    # Fetch persona records
    cursor.execute("SELECT name, age, gender, ethnicity, body FROM personas")
    personas = cursor.fetchall()

    persona_cards_html = ""
    for i, persona in enumerate(personas):
        name, age, gender, ethnicity, body = persona
        image_filename = name.lower() + ".jpg"  # Assuming image filenames are lowercase first names

        persona_cards_html += f"""
        <div class="card">
            <img src="images/{image_filename}" alt="{name}" class="persona-img">
            <h2>{name} ({gender}, {age})</h2>
            <p><strong>Ethnicity:</strong> {ethnicity}</p>
            <p>{body}</p>
        </div>
        """

    # Fetch team member records
    cursor.execute("SELECT student_name, student_num FROM team_members")
    team_members = cursor.fetchall()

    team_members_html = "<ul>"
    for student_name, student_num in team_members:
        team_members_html += f"<li>{student_name}  ({student_num})</li>"
    team_members_html += "</ul>"

    # Close the database connection
    conn.close()

    # HTML for the page   
    page_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="B_page1.css">
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

        <div class="mission-background">
            <div class="mission-box">
                <h2>Mission Statement</h2>
                <p>
                    Our website aims to address the 'Anthropomorphic Climate Change' social challenge by serving as an accessible and informative platform that presents Australian climate data in a meaningful and unbiased manner. It aims to empower users to understand the long-term trends and effects of human-induced climate change within the Australian context.
                <br><br>
                    We approach this challenge from a social and educational perspective. Our goal is to promote climate literacy by presenting climate data, such as temperature, rainfall, humidity changes and more, through interactive and selective parameters that display the desired climate data in table form. These tools are designed to support our audience based on our personas (seen below).
                </p>
            </div>
        </div>

        <div class="persona-section">
            <div class="persona-row">
                {persona_cards_html}
            </div>
        </div>

        <div class="info-box">
            <h2>How our website can be used?</h2>
            <p>
                Our personas will use the website as a reliable, user-friendly platform to access, interpret, and apply Australian climate data for their personal, professional, and community needs and lives. The platform enables users to quickly find credible climate data and trends. Such information can help plan around climate variability, manage risk, and adapt to weather impacts in agriculture and business sectors.
            <br><br>
                The website is designed to cater to various levels of digital proficiency, offering summaries of weather data from over the years, presented clearly and respectfully for a wide audience.
            </p>
        </div>

        <div class="info-box">
            <h2>Team Members</h2>
            {team_members_html}
        </div>

        <div class="footer">
            <p>Python Programming Studio Assignment - WORKING APPLICATION</p>
            <p>Background Image Found: 
                <a href="https://unsplash.com/photos/a-view-of-a-mountain-range-from-a-distance-aiEByysNppw" target="_blank">
                Unsplash</a>
        </div>
    </body>
    </html>
    """

    return page_html
