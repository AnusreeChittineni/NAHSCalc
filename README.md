# NAHS Calculators

## Project Overview

This project is a web-application that uses Python, Flask, HTML, JavaScript, and CSS.
The project itself consists of three main pages: the landing page, GPA Calculator, and Final Grade Calculator.
The main purpose of the project is to provide students at my school with an automated way to
calculate their potential GPA at the end of the trimester based on their current grades
and what grade they will need on the their final to get a certain Y1 grade.

## Project Inspiration

I took on this project because I have seen mutiple classmates attempt to calculate their GPAs, but do so
incorrectly. After proceeding to help those same classmates, I realized that our student body would benefit
from having an automated resource to complete these calculations for us. And although I know if I had adminstrative
access to our gradebook service, Powerschool, my project would be more user friendly, what I produced is a
great start. In addition to having the GPA calculator, I added a Final Grade Calculator that is geared specifically
towards my school's grading scale. Through this website students will be able to accurately determine what grades 
they will need to get in their classes to achieve their desired GPA.

## Code Explanation

The website works by having a HTML form on each page that houses a calculator. When submitted, the form information is
requested on the python file and used to calcuate the users potential GPA/Final Grade using some python calculations and our school's
GPA/Final Grade formula. The page GPA Calculator also has a link to another page that displays the school GPA scale. While the Final Grade
Calculator page has a link to a page that displays the Grade scale. Both scale charts are made using a SQLite Database, db.execute statements,
and Jinja to send the information to the HTML file.I used Boostrap and my own CSS file to style the website.