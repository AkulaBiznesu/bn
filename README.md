# Binance Data Collection and Visualization
The project is a web application built using Flask and Plotly. It allows users to fetch and visualize candlestick data from the Binance API for various symbols and time intervals. The application collects data from the API, stores it in a SQLite database, and provides a user interface to view the data in the form of candlestick charts and a pie chart of market caps. Users can select symbols and intervals through a dropdown menu and fetch the corresponding data. The charts are dynamically rendered using Plotly, providing an interactive and visually appealing representation of the data.
## Task 1: Collecting Data from Binance API

- Install the required dependencies by running `pip3 install -r requirements.txt`.
- Open the script file `binance.py`
- Run the script using the command `python3 binance.py`, input pair and interval
- The data will be saved in a CSV file and db sqlite named by pair and interval.

## Task 2: Flask UI for Data Visualization

- Install the required dependencies by running `pip3 install -r requirements.txt`.
- Open the script file `flask_app.py`
- Run the Flask application using the command `python3 app.py`.
- Open a web browser and visit `http://localhost:5000` to view the candlestick chart and pie chart.
- You can also pick Pair and Interval through web interface, all the data will be saved to db.

