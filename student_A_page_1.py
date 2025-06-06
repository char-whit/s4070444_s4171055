import pyhtml

def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""
    <!DOCTYPE html>
<html>

<head>
    <!-- Include the external css file -->
    <link rel="stylesheet" href="style.css">
</head>

<body>

<div class="header">
        <h1>
            <img src="images/global-warming.png" class="top-image" alt="logo" width="75" height="75">
            My Website about climate change
        </h1>
</div>

    <div class="topnav">
        <a href="/">Home</a>
        <a href="/weather-stations">A task 2</a>
        <a href="/weather-stations-similar">A task 3</a>
        <a href="/mission">B task 1</a>
        <a href="/metrics">B task 2</a>
        <a href="/metrics-similar">B task 3</a>
         
        </div>
        <a href="#" style="float:right">Help</a>
    </div>

    

    <div class="content">

    <div class="row">
        <div class="column side">
            <h2>Column</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet pretium urna. Vivamus venenatis velit nec neque ultricies, eget elementum magna tristique. Quisque vehicula, risus eget aliquam placerat, purus leo tincidunt eros, eget luctus quam orci in velit. Praesent scelerisque tortor sed accumsan convallis.</p>
        </div>
    
        <div class="column middle">
            <div>
            <h2> Facts </h2>
                <div class="card">
                    <h2>London</h2>
                    <p>London is the capital city of England.</p>
                    <p>London has over 9 million inhabitants.</p>
                    </div>

                    <div class="card">
                    <h2>Oslo</h2>
                    <p>Oslo is the capital city of Norway.</p>
                    <p>Oslo has over 700,000 inhabitants.</p>
                    </div>

                    <div class="card">
                    <h2>Rome</h2>
                    <p>Rome is the capital city of Italy.</p>
                    <p>Rome has over 4 million inhabitants.</p>
                    </div>   

                    <div class="card">
                    <h2>Paris</h2>
                    <p>Paris is the capital city of France.</p>
                    <p>Paris has over 2 million inhabitants.</p>
                    </div>     
            </div>
            <div>
            <h2> Attributes </h2>
"""
    sql_query = "select * from attribute_list;"
    # page_html+= f"<h2>Result from \"{sql_query}\"</h2>"
            
    #Run the query in sql_query and get the results
    results = pyhtml.get_results_from_query("database/climate.db",sql_query)
            
    #Adding results to the web page without any beautification. Try turning it into a nice table!
    page_html+="<table class="'styled-table'">"
    page_html+="<thead><tr><th>Attibute name</th><th>Description</th></tr></thead>"

    for row in results:
        page_html+="<tr><td>"+str(row[0])+"</td> <td>"+str(row[1])+"</td></tr>"
    

    page_html+="</table>"

    page_html+="""
            </div>
        </div>
    
        <div class="column side">
            <h2>Column</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet pretium urna. Vivamus venenatis velit nec neque ultricies, eget elementum magna tristique. Quisque vehicula, risus eget aliquam placerat, purus leo tincidunt eros, eget luctus quam orci in velit. Praesent scelerisque tortor sed accumsan convallis.</p>
        </div>

    </div>    
    
    </div>

    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>

</body>
</html>    

    """
    return page_html
