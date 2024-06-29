### Vehicle Routing Problem (VRP) with Genetic Algorithm

## Overview
This project aims to solve the Vehicle Routing Problem (VRP) using a Genetic Algorithm (GA). The VRP is a combinatorial optimization problem that seeks the most efficient routes for a fleet of vehicles to deliver goods to a set of locations. The goal is to minimize the total distance traveled while ensuring that the demands of all locations are met and that the routes are balanced across all vehicles.

## Genetic Algorithm (GA)
Genetic Algorithms are a class of evolutionary algorithms inspired by the process of natural selection. They are particularly effective for optimization problems where the search space is large and complex. GAs use a population of potential solutions, iteratively evolving them over generations to find the best solution.

### Key Concepts in GA:
- **Population**: A set of potential solutions to the problem.
- **Individual**: A single solution in the population.
- **Fitness Function**: A function that evaluates how close an individual is to the optimal solution.
- **Selection**: The process of choosing individuals from the population to create offspring.
- **Crossover**: Combining parts of two individuals to create a new individual.
- **Mutation**: Randomly altering an individual to introduce genetic diversity.

## Project Description
In this project, we use a Genetic Algorithm to optimize the routes for a fleet of vehicles starting from a depot, visiting multiple locations, and returning to the depot. The project is implemented using Streamlit for the web interface and Folium for map visualization.

### Key Features:
1. **User Inputs**: The user can input the number of vehicles and the depot location, as well as add multiple delivery locations.
2. **Geocoding**: Locations are geocoded to obtain their coordinates using the Geopy library.
3. **Genetic Algorithm**: 
   - **Initialization**: A population of potential routes is generated.
   - **Evaluation**: Routes are evaluated based on total distance traveled and balance among vehicles.
   - **Selection, Crossover, Mutation**: Routes are evolved over generations to find the optimal solution.
4. **Visualization**: The optimal routes are displayed on an interactive map using Folium, with different colors representing different vehicle routes.

### Project Impact
This project has significant practical implications in logistics and supply chain management. By optimizing vehicle routes:
- **Cost Reduction**: Minimize fuel consumption and vehicle maintenance costs.
- **Time Efficiency**: Reduce delivery times and improve customer satisfaction.
- **Resource Utilization**: Efficiently balance the workload among vehicles, leading to better utilization of resources.

### Usage Instructions
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Streamlit app with `streamlit run app.py`.
4. Enter the number of vehicles and the depot location.
5. Add delivery locations as needed.
6. Click 'Get Routes' to see the optimized routes on the map.

### Future Enhancements
- **Dynamic Demand Handling**: Allow input of delivery demands for each location.
- **Time Windows**: Incorporate time windows for deliveries.
- **Real-Time Traffic Data**: Use real-time traffic data to further optimize routes.

This project demonstrates the power of genetic algorithms in solving complex optimization problems and provides a foundation for further enhancements and applications in real-world logistics and transportation systems.

### Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bug fixes.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

By leveraging Genetic Algorithms, this project offers an efficient solution to the Vehicle Routing Problem, making it a valuable tool for optimizing logistics and delivery systems.
### Web App
https://vehical-routing-problem.streamlit.app
