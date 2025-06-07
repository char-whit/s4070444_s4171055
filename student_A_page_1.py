import pyhtml

def get_page_html(form_data):
    print("Returning landing page...")
    page_html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Climate Change in Australia</title>
        <link rel="stylesheet" href="style_landing_page.css">
        
            
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
