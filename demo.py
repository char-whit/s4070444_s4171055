import pyhtml
import student_A_page_1
import student_A_page_2
import student_A_page_3
import student_B_page_1
import student_B_page_2
import student_B_page_3

pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"]        =student_A_page_1   #Page to show when someone accesses "http://localhost/"
pyhtml.MyRequestHandler.pages["/weather-stations"]=student_A_page_2   #Page to show when someone accesses "http://localhost/weather-stations"
pyhtml.MyRequestHandler.pages["/weather-stations-similar"]=student_A_page_3   #Page to show when someone accesses "http://localhost/weather-stations-similar"
pyhtml.MyRequestHandler.pages["/mission"]        =student_B_page_1   #Page to show when someone accesses "http://localhost/"
pyhtml.MyRequestHandler.pages["/metrics"]=student_B_page_2   #Page to show when someone accesses "http://localhost/metrics"
pyhtml.MyRequestHandler.pages["/metrics-similar"]=student_B_page_3   #Page to show when someone accesses "http://localhost/metrics-similar"


#Host the site!
pyhtml.host_site()