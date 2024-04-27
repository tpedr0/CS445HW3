# Tax Visualization Dash App

This Dash application visualizes U.S. tax data per capita using interactive choropleth maps. It leverages Python, Dash by Plotly, and other essential libraries to offer an interactive interface where users can explore various tax metrics across different states.
# Features

    Dual Interactive Maps: Visualize different tax items on separate maps.
    Per Capita Tax Data: Data normalized by state population to reflect per capita metrics.
    Interactive Elements: Buttons to select different tax categories for visualization.

# Installation

Before you can run this application, you'll need to install several dependencies:

	cd C:\Users\'UserName'\Desktop
	git clone https://github.com/tpedr0/CS445HW3.git


4. Install dependencies
3.pip install -r requirements.txt

# Usage

To run the application, execute the following command in your terminal:

	python choroplethMap.py

This will start the Dash server, and you can access the app in your web browser at http://127.0.0.1:8050.

The application utilizes two main datasets:
- Filtered Tax Data 2021: Contains various tax metrics per state.
- State Populations 2021: Population data sourced from the U.S. Census, used for normalizing tax data.

App Structure

- Data Processing: Load and preprocess data using Pandas.
- App Layout: Define the layout and interactive components of the Dash app.
- Callbacks: Handle interactivity and updates to the visual components based on user input.

# Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
