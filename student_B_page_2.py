import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="A_page2.css">
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

        

        <h1>Climate change based on climate metric</h1>
        <p>is supposed to go here...</p>



        
    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>

    </body>
    </html>    

    """
    return page_html
