

def get_page_html(form_data):
    print("About to return page home page...")
    page_html ="""
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
                <div class="card">
                    <img src="images/image-person.jpg" alt="Persona 1" class="persona-img">
                    <h2>Persona 1</h2>
                    <p>London is the capital city of England.</p>
                    <p>London has over 9 million inhabitants.</p>
                </div>

                <div class="card">
                    <img src="images/image-person.jpg" alt="Persona 1" class="persona-img">
                    <h2>Persona 2</h2>
                    <p>Oslo is the capital city of Norway.</p>
                    <p>Oslo has over 700,000 inhabitants.</p>
                </div>

                <div class="card">
                    <img src="images/image-person.jpg" alt="Persona 1" class="persona-img">
                    <h2>Persona 3</h2>
                    <p>Rome is the capital city of Italy.</p>
                    <p>Rome has over 4 million inhabitants.</p>
                </div>   

                <div class="card">
                    <img src="images/image-person.jpg" alt="Persona 1" class="persona-img">
                    <h2>Persona 4</h2>
                    <p>Paris is the capital city of France.</p>
                    <p>Paris has over 2 million inhabitants.</p>
                </div>     
            </div>
        </div>
    
        <div class="info-box">
            <h2>How our website can be used?</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet pretium urna. Vivamus venenatis velit nec neque ultricies, eget elementum magna tristique. Quisque vehicula, risus eget aliquam placerat, purus leo tincidunt eros, eget luctus quam orci in velit. Praesent scelerisque tortor sed accumsan convallis.</p>
        </div>

    <div class="footer">
        <p>Python Programming Studio Assignment - WORKING APPLICATION</p>
    </div>

    </body>
    </html>    

    """
    return page_html
