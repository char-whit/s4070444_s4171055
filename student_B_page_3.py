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
            <img src="tmp-image.png" class="top-image" alt="logo" width="75" height="75">
            My Website about climate change
        </h1>
</div>

    <div class="topnav">
        <a href="/">Home</a>
        <a href="/task-a-1">Task A</a>
        <a href="/task-b-1">Task B</a>
        <a href="#" style="float:right">Help</a>
    </div>

    

    <div class="content">
        <p>Subtask B-1</p>
    </div>

    <div class="footer">
        <p>COSC3106 - Programming Class 5</p>
    </div>

</body>
</html>    

    """
    return page_html
