import numpy as np
import pandas as pd
import streamlit as st
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from deap import base, creator, tools, algorithms
import random
import folium
import streamlit.components.v1 as components

geolocator = Nominatim(user_agent="my_app")
st.title('Vehicle Routing Problem')

# Sidebar for inputs
st.sidebar.write('Enter the number of vehicles')
n = st.sidebar.number_input('Number of vehicles', min_value=1, step=1)

depot = st.sidebar.text_input('Enter Depot location')

if 'locations' not in st.session_state:
    st.session_state.locations = []

# Function to add a new location input box
def add_location():
    st.session_state.locations.append("")

# Display the input boxes for locations
for i, location in enumerate(st.session_state.locations):
    new_location = st.sidebar.text_input(f'Location {i+1}', value=location, key=f'location_{i}')
    st.session_state.locations[i] = new_location

# Placeholder for the "Add Location" button
add_location_placeholder = st.sidebar.empty()
if add_location_placeholder.button('Add Location'):
    add_location()

# Get coordinates for the depot
try:
    depot_coordinates = geolocator.geocode(depot)
except GeocoderTimedOut:
    st.warning("Geocoding timed out. Please try again.")
    depot_coordinates = None

if depot_coordinates:
    coordinates = [(depot_coordinates.longitude, depot_coordinates.latitude)]
else:
    st.warning("Depot location not found. Please enter a valid location.")
    coordinates = []

# Get coordinates for the other locations
for location in st.session_state.locations:
    if location:
        try:
            location_coordinates = geolocator.geocode(location)
        except GeocoderTimedOut:
            st.write(f'Geocoding timed out for: {location}')
            location_coordinates = None

        if location_coordinates:
            x, y = location_coordinates.longitude, location_coordinates.latitude
            coordinates.append((x, y))
        else:
            st.write(f'Coordinates not found for: {location}')

# Display locations with their coordinates
st.write('Coordinates:')
for idx, (location, (x, y)) in enumerate(zip(['Depot'] + st.session_state.locations, coordinates)):
    if location:
        st.write(f'{location}: Longitude={x}, Latitude={y}')

if len(coordinates) < 2:
    st.warning("Please enter at least two valid locations.")
else:
    # Genetic Algorithm setup
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))  
    creator.create("Individual", list, fitness=creator.FitnessMin)

    num_locations = len(coordinates)
    num_vehicles = n
    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_locations), num_locations)  
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)  
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalVRP(individual):
        total_distance = 0
        distances = []  # Track distance traveled by each vehicle for balance calculation
        # Split the list of locations among vehicles, ensuring each starts and ends at the depot
        for i in range(num_vehicles):
            vehicle_route = [coordinates[0]] + [coordinates[individual[j]] for j in range(i, len(individual), num_vehicles)] + [coordinates[0]]
            # Calculate total distance traveled by this vehicle
            vehicle_distance = sum(np.linalg.norm(np.array(vehicle_route[k+1]) - np.array(vehicle_route[k])) for k in range(len(vehicle_route)-1))
            total_distance += vehicle_distance
            distances.append(vehicle_distance)
        balance_penalty = np.std(distances)  # Use standard deviation of distances as a penalty for imbalance among vehicles
        return total_distance, balance_penalty

    toolbox.register("evaluate", evalVRP)  # Register the evaluation function
    toolbox.register("mate", tools.cxPartialyMatched)  # Register the crossover function suitable for permutation-based representation
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)  # Register the mutation function to shuffle indices with a 5% chance per index
    toolbox.register("select", tools.selTournament, tournsize=3)  # Register the selection function using tournament selection

    def plot_routes(individual, title="Routes"):
        # Create a Folium map centered around the depot
        m = folium.Map(location=[coordinates[0][1], coordinates[0][0]], zoom_start=13)
        
        # Add depot marker
        folium.Marker(location=[coordinates[0][1], coordinates[0][0]], popup="Depot", icon=folium.Icon(color='red')).add_to(m)
        
        # Add markers for all locations
        for idx, (location, (x, y)) in enumerate(zip(['Depot'] + st.session_state.locations, coordinates)):
            if location:
                folium.Marker(location=[y, x], popup=f'{location}').add_to(m)

        # Draw routes for each vehicle
        colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue']
        vehicle_routes = []  # To store the routes for each vehicle
        for i in range(num_vehicles):
            vehicle_route = [coordinates[0]] + [coordinates[individual[j]] for j in range(i, len(individual), num_vehicles)] + [coordinates[0]]
            vehicle_routes.append(vehicle_route)  # Store the route for this vehicle
            folium.PolyLine(locations=[(loc[1], loc[0]) for loc in vehicle_route], color=colors[i % len(colors)], weight=2.5, opacity=1).add_to(m)

        map_html = m._repr_html_()

        # Display the map in an iframe
        components.html(map_html, width=700, height=500)
        
        # Return the vehicle routes
        return vehicle_routes

    def main():
        random.seed(42)  # Seed for reproducibility
        pop = toolbox.population(n=300)  # Generate initial population
        hof = tools.HallOfFame(1)  # Hall of Fame to store the best individual

        # Setup statistics to track
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)

        # Run the genetic algorithm
        algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 300, stats=stats, halloffame=hof)

        # Plot the best route found
        vehicle_routes = plot_routes(hof[0], "Optimal Route")

        # Display the vehicle routes
        st.write("Vehicle Routes:")
        for i, route in enumerate(vehicle_routes):
            route_locations = [f'{coordinates.index(loc)}' for loc in route]
            st.write(f"Vehicle {i+1}: {', '.join(route_locations)}")

        return pop, stats, hof

    if st.button('Get Routes'):
        main()
