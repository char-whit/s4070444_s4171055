import pyhtml

def get_page_html(form_data):
    print("Returning landing page...")
    page_html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Climate Change in Australia</title>
        <link rel="stylesheet" href="style.css">
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                margin: 0;
                background-color: #f9f9f9;
                color: #333;
            }

.topnav {
    display: flex;
    justify-content: center;  /* center the content horizontally */
    align-items: center;
    background-color: #2c3e50;
    padding: 10px 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    gap: 15px;  /* spacing between links */
}

            .topnav .nav-links {
                display: flex;
                gap: 15px;
            }

            .topnav a {
                color: white;
                text-decoration: none;
                padding: 8px 14px;
                border-radius: 5px;
                transition: background-color 0.3s;
                font-size: 16px;
            }

            .topnav a:hover {
                background-color: #4CAF50;
            }

            .hero {
                background: url('images/weatherstation.png') center/cover no-repeat;
                color: white;
                padding: 120px 20px;
                text-align: center;
            }

            .hero h1 {
                font-size: 60px;
                margin-bottom: 20px;
            }

            .hero p {
                font-size: 24px;
                margin-bottom: 30px;
            }

            .hero a {
                display: inline-block;
                background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4));
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 18px;
            }

            .intro {
                text-align: center;
                padding: 80px 20px;
                background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4));
                color: white;
            }

            .topics {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 25px;
                padding: 40px;
            }

            .topic-box {
                background-color: #e6f2ff;
                padding: 25px;
                border-radius: 15px;
                width: 220px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.2s ease;
            }

            .topic-box:hover {
                transform: scale(1.05);
            }

            .topic-box h3 {
                margin: 10px 0;
                font-size: 20px;
            }

            .carousel-container {
                position: relative;
                width: 85%;
                margin: 60px auto 0 auto;
                background: #fff;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }

            .carousel-slide {
                display: none;
                padding: 10px;
            }

            .carousel-slide.active {
                display: block;
                animation: fade 0.5s;
            }

            @keyframes fade {
                from {opacity: 0.4;}
                to {opacity: 1;}
            }

            .carousel-buttons {
                margin-top: 15px;
            }

            .carousel-buttons button {
                padding: 10px 20px;
                margin: 5px;
                font-size: 16px;
                border: none;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>

        <div class="topnav">
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/weather-stations">A task 2</a>
                <a href="/ap2">A task 2.2</a>
                <a href="/weather-stations-similar">A task 3</a>
                <a href="/mission">B task 1</a>
                <a href="/metrics">B task 2</a>
                <a href="/metrics-similar">B task 3</a>
            </div>
            <a href="#">Help</a>
        </div>

        <div class="hero">
            <h1>Investigating Climate Change in Australia</h1>
            <p>Track key environmental metrics and discover changes across regions</p>
            <a href="/weather-stations">Explore Weather Data</a>
        </div>

        <div class="intro">
            <h2>Why This Matters</h2>
            <p>Our planet is changing. This site helps you understand how by exploring real-world weather station data across Australia.</p>
        </div>

        <div class="topics">
            <div class="topic-box">
                <div style="font-size:40px;">🌧️</div>
                <h3>Rainfall</h3>
                <p>Track seasonal rainfall patterns and shifts over time.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">🌡️</div>
                <h3>Temperature</h3>
                <p>Analyze extreme temperature changes and trends.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">💧</div>
                <h3>Humidity</h3>
                <p>Measure moisture levels across various regions.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">☀️</div>
                <h3>Sunshine</h3>
                <p>See how hours of sunlight have fluctuated.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">🌫️</div>
                <h3>Evaporation</h3>
                <p>Observe how water evaporates from land and soil.</p>
            </div>
        </div>

        <div class="carousel-container">
            <h2>Climate Metric Descriptions</h2>
    """

    sql_query = "SELECT * FROM attribute_list;"
    results = pyhtml.get_results_from_query("database/climate.db", sql_query)

    for i, row in enumerate(results):
        active_class = "active" if i == 0 else ""
        page_html += f"""
            <div class="carousel-slide {active_class}">
                <h3>{row[0]}</h3>
                <p>{row[1]}</p>
            </div>
        """

    page_html += """
            <div class="carousel-buttons">
                <button onclick="prevSlide()">&#8592; Prev</button>
                <button onclick="nextSlide()">Next &#8594;</button>
            </div>
        </div>

        <script>
            let currentSlide = 0;
            const slides = document.querySelectorAll(".carousel-slide");

            function showSlide(index) {
                slides.forEach((slide, i) => {
                    slide.classList.remove("active");
                    if (i === index) slide.classList.add("active");
                });
            }

            function nextSlide() {
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }

            function prevSlide() {
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                showSlide(currentSlide);
            }

            setInterval(() => {
                nextSlide();
            }, 5000);

            showSlide(currentSlide);
        </script>

    </body>
    </html>
    """
    return page_html
