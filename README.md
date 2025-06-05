Readme

The NASA Asteroids projects shows which asteroid has approached earth and if they are hazardous or non hazardous.

First, an API key is fetched from the NASA website and using that I have taken 10000 data from it.

After that I have made a connection from python jupyter notebook to MySQL using pymysql and have created a database and two tables in it namely asteroids and close_approach.
The asteroids table contains information such as :
id
name
absolute_magnitude_h
estimated_diameter_min_km
estimated_diameter_max_km
is_potentially_hazardous_asteroid

The close_approach table contains data such as :
neo_reference_id(same as id in asteroids)
close_approach_date
relative_velocity_kmph
astronomical(AU)
miss_distance_km
miss_distance_lunar
orbiting_body

After creating the table, I have inserted the values inside the table that I have taken from the API from NASA website.

Then, I have run queries to fetch the data from sql.

The 20 queries are :
Count how many times each asteroid has approached Earth
Average velocity of each asteroid over multiple approaches
List top 10 fastest asteroids
Find potentially hazardous asteroids that have approached Earth more than 3 times
Find the month with the most asteroid approaches
Get the asteroid with the fastest ever approach speed
Sort asteroids by maximum estimated diameter (descending)
An asteroid whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance).
Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.
List names of asteroids that approached Earth with velocity > 50,000 km/h
Count how many approaches happened per month
Find asteroid with the highest brightness (lowest magnitude value)
Get number of hazardous vs non-hazardous asteroids
Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.
Find asteroids that came within 0.05 AU(astronomical distance)
Count of potentially hazardous asteroids
List asteroids orbiting Earth
Asteroids with estimated max diameter > 5 km
Count of close approaches in the year 2024
Average miss distance of all approaches (km)

In the streamlit dashboard, I have created two selectboxes - Queries and Filter

Tools used for the analysis:
Pandas, Numpy, pymysql, streamlit

