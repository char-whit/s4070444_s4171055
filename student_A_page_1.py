import pyhtml

def get_page_html(form_data):
    print("Returning landing page...")
    page_html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Climate Change in Australia</title>
        <link rel="stylesheet" href="A_landing_page.css">
        
            
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

        <div class="hero">
            <h1>Investigating Climate Change in Australia</h1>
            <p>Track key environmental metrics and discover changes across regions</p>
            <div class="dropdown-hero">
    
    <div class="dropdown-content-hero">
        <a href="/weather-stations">Weather Station Data</a>
        <a href="/metrics">Climate Metric Data</a>
        <a href="/weather-stations-similar">Similar Station Metrics</a>
        <a href="/metrics-similar">Similar Climate Metrics</a>
    </div>
</div>

        </div>

        <div class="intro">
            <h2>Why This Matters</h2>
            <h4>Our planet is changing. Austalia's climate is changing.</h4>
            <p>This site helps you understand how by exploring data from 141 weather stations nationwide which a pleathora of weather data being recorded daily from 1970 to 2020.</p>
        </div>

        <div class="topics">
            <div class="topic-box">
                <div style="font-size:40px;">🌧️</div>
                <h3>Rainfall</h3>
                <p>TROUGHTON ISLAND recorded a staggering 367.3mm of rainfall on the 27th of January 1973</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">🌡️</div>
                <h3>Temperature</h3>
                <p>Broome airport's weather station has recorded an increase of average maximum temperature between the time period 2005-2009 (32 degrees) and 2010-2014 (32.7 degrees).</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">💧</div>
                <h3>Rainfall changes</h3>
                <p>Rainfall measured by the weatherstation at Perth airport has decreased by over 36% between 2005 to 2019.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">☀️</div>
                <h3>Minimum temperature changes temperature changes</h3>
                <p>Port Headland has seen a decrease of average minimum temperature by over 2% between 2010 to 2020.</p>
            </div>
            <div class="topic-box">
                <div style="font-size:40px;">🌫️</div>
                <h3>Weather Stations</h3>
                <p>There are multiple weather stations reccording comprehensive wather data in 9 states.</p>
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
<footer style="background-color: #2c3e50; color: white; padding: 40px 20px 20px; text-align: center; font-size: 16px; margin-top: 80px; border-top: 3px solid #4CAF50;">
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 15px;">
        <a href="/" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Home</a>
        <a href="/mission" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Our Mission</a>
        <a href="/weather-stations" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Weather Station Data</a>
        <a href="/metrics" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Climate Metric Data</a>
        <a href="/weather-stations-similar" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Similar Station Metrics</a>
        <a href="/metrics-similar" style="color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; transition: background-color 0.3s;">Similar Climate Metrics</a>
    </div>
    <p style="font-size: 14px; color: #ccc; margin-top: 10px;">© 2025 Climate Change in Australia | Data from the Australian Bureau of Meteorology</p>
</footer>

    </body>
    </html>
    """
    return page_html
