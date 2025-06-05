import pandas as pd
import numpy as np
import streamlit as st
import pymysql
import datetime
from datetime import datetime

st.title("NASA Project")

myconnection = pymysql.connect(host='127.0.0.1', user = 'root', password = 'rootroot', database = 'nasa_db')

asteroid_count_df = pd.read_sql_query("SELECT COUNT(*) AS total_asteroids FROM ASTEROIDS", myconnection)
st.write("Total Asteroids in Database:", asteroid_count_df['total_asteroids'].iloc[0])

st.sidebar.header("Navigation")
selected_page = st.sidebar.radio("Go to", ["Query Dashboard", "Filter Options"])


if selected_page == "Query Dashboard":
    sql_queries = {
        "Count how many times each asteroid has approached Earth": """
            SELECT asteroids.name AS asteroid_name, COUNT(close_approach.neo_reference_id) AS approach_count from asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            GROUP BY asteroids.id, asteroids.name
            ORDER BY approach_count DESC, asteroids.name ASC;
        """,
        "Average velocity of each asteroid over multiple approaches": """
            SELECT asteroids.name, AVG(close_approach.relative_velocity_kmph) AS average_velocity_kmph
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            GROUP BY asteroids.id, asteroids.name
            ORDER BY asteroids.name ASC
        """,
        "List top 10 fastest asteroids": """
            SELECT asteroids.name as NAME, close_approach.relative_velocity_kmph from asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            ORDER BY close_approach.relative_velocity_kmph DESC
            LIMIT 10;
        """,
        "Find potentially hazardous asteroids that have approached Earth more than 3 times": """
            SELECT asteroids.name, COUNT(close_approach.neo_reference_id) AS approach_count
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE asteroids.is_potentially_hazardous_asteroid = TRUE
            GROUP BY asteroids.id, asteroids.name
            HAVING COUNT(close_approach.neo_reference_id) > 3
            ORDER BY approach_count DESC
        """,
        "Find the month with the most asteroid approaches": """
            SELECT MONTH(close_approach_date) AS month_number, COUNT(*) AS approach_count
            FROM close_approach
            GROUP BY month_number
            ORDER BY approach_count DESC
            LIMIT 1;
        """,
        "Get the asteroid with the fastest ever approach speed": """
            SELECT asteroids.name, close_approach.relative_velocity_kmph
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            ORDER BY close_approach.relative_velocity_kmph DESC
            LIMIT 1;
        """,
        "Sort asteroids by maximum estimated diameter (descending)": """
            SELECT asteroids.name, asteroids.estimated_diameter_max_km FROM asteroids
            GROUP BY asteroids.name, asteroids.estimated_diameter_max_km
            ORDER BY asteroids.estimated_diameter_max_km DESC;
        """,
        "An asteroid whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance).": """
            SELECT asteroids.name, COUNT(close_approach.neo_reference_id) AS approach_count,close_approach.close_approach_date ,close_approach.miss_distance_lunar
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            GROUP BY asteroids.id, asteroids.name, close_approach.close_approach_date, close_approach.miss_distance_lunar
            ORDER BY close_approach.miss_distance_lunar ASC
            LIMIT 1
        """,
        "Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.": """
            SELECT asteroids.name, close_approach.close_approach_date, close_approach.miss_distance_km
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            GROUP BY asteroids.name, close_approach.close_approach_date, close_approach.miss_distance_km
            ORDER BY close_approach.miss_distance_km ASC;
        """,
        "List names of asteroids that approached Earth with velocity > 50,000 km/h": """
            SELECT DISTINCT asteroids.name
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE close_approach.relative_velocity_kmph > 50000
        """,
        "Count how many approaches happened per month": """
            SELECT MONTH(close_approach_date) AS month_number, COUNT(neo_reference_id) AS approach_count
            FROM close_approach
            GROUP BY month_number;
        """,
        "Find asteroid with the highest brightness (lowest magnitude value)": """
            SELECT asteroids.name, asteroids.absolute_magnitude_h
            FROM asteroids
            ORDER BY asteroids.absolute_magnitude_h ASC
            LIMIT 1;
        """,
        "Get number of hazardous vs non-hazardous asteroids": """
            SELECT asteroids.is_potentially_hazardous_asteroid, COUNT(*) AS asteroid_count
            FROM asteroids
            GROUP BY asteroids.is_potentially_hazardous_asteroid
        """,
        "Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.": """
            SELECT asteroids.name, close_approach.close_approach_date, close_approach.miss_distance_lunar
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE close_approach.miss_distance_lunar < 1
            ORDER BY close_approach.miss_distance_lunar ASC, asteroids.name ASC
        """,
        "Find asteroids that came within 0.05 AU(astronomical distance)": """
            SELECT asteroids.name, close_approach.astronomical
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE close_approach.astronomical < 0.05
            GROUP BY asteroids.name, close_approach.astronomical
        """,
        "Count of potentially hazardous asteroids": """
            SELECT COUNT(*) AS hazardous_asteroid_count
            FROM asteroids
            WHERE is_potentially_hazardous_asteroid = TRUE;
        """,
        "List asteroids orbiting Earth": """
            SELECT DISTINCT asteroids.name
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE close_approach.orbiting_body = 'Earth';
        """,
        "Asteroids with estimated max diameter > 5 km": """
            SELECT name, estimated_diameter_max_km
            FROM asteroids
            WHERE estimated_diameter_max_km > 5
            ORDER BY estimated_diameter_max_km DESC;
        """,
        "Count of close approaches in the year 2025": """
            SELECT COUNT(*) AS approaches_in_2025
            FROM close_approach
            WHERE YEAR(close_approach_date) = 2025;
        """,
        "Average miss distance of all approaches (km)": """
            SELECT AVG(miss_distance_km) AS average_miss_distance_km
            FROM close_approach;
        """
    }

    option = st.selectbox(
        'Select the Query',
        tuple(sql_queries.keys()),
        index=None,
        placeholder="Select a Query"
    )

    st.write('You selected:', option)

    if option:
        st.subheader(f"Query: {option}")

        query_to_execute = sql_queries.get(option)

        df = pd.read_sql_query(query_to_execute, myconnection)

        st.dataframe(df, use_container_width=True)

elif selected_page == "Filter Options":
    st.header("Asteroid Filter Options")

    c1, a, c2, b, c3 = st.columns([0.2, 0.1, 0.2, 0.1, 0.2])

    with c1:
        mag_min = st.slider("Min Magnitude", 13.8, 32.61, (13.8, 32.61))

        diam_min = st.slider("Min Estimated Diameter (km)", 0.00, 4.62, (0.00, 4.62))
        diam_max = st.slider("Max Estimated Diameter (km)", 0.00, 10.33, (0.00, 10.33))

    with c2:
        velocity = st.slider("Relative_velocity_kmph Range", 1418.21, 173071.83, value=(1418.21, 173071.83))

        astro = st.slider("Astronomical unit", 5.16453e-05, 0.4999515747)

        hazardous = st.selectbox("Only Show Potentially Hazardous", options=[0, 1], index=0)

    with c3:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
        end_date = st.date_input("End Date", datetime(2025, 4, 13))

    button = st.button("Apply Filters")


    query = """
             SELECT
    asteroids.id, asteroids.name, asteroids.absolute_magnitude_h, asteroids.estimated_diameter_min_km,
    asteroids.estimated_diameter_max_km, asteroids.is_potentially_hazardous_asteroid,
    close_approach.close_approach_date, close_approach.relative_velocity_kmph, close_approach.miss_distance_km, close_approach.orbiting_body
    FROM asteroids
    JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
    WHERE asteroids.absolute_magnitude_h BETWEEN %s AND %s
    AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
    AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
    AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
    AND close_approach.close_approach_date BETWEEN %s AND %s
    AND asteroids.is_potentially_hazardous_asteroid = %s

    """
    
    params = [
        mag_min[0], mag_min[1],
        diam_min[0], diam_min[1],
        diam_max[0], diam_max[1],
        velocity[0], velocity[1],
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),  
        hazardous
    ]

    if button:
        cursor = myconnection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        df = pd.DataFrame(rows, columns=columns)
        
        if not df.empty:
            st.subheader("Filtered Asteroid Data:")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No asteroids found matching the selected filters.")
        
        cursor.close()

    
