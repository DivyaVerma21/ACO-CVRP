# ACO-CVRP
This repository contains Python code implementing an Ant Colony Optimization (ACO) algorithm to solve the Capacitated Vehicle Routing Problem (CVRP).
The Capacitated Vehicle Routing Problem (CVRP) is a combinatorial optimization problem where the goal is to find the optimal set of routes for a fleet of vehicles to deliver goods to a set of customers, considering capacity constraints for each vehicle.
Ant Colony Optimization (ACO) is a metaheuristic inspired by the foraging behavior of ants to find optimal paths through a given graph. In the context of CVRP, ACO algorithms can be used to efficiently find near-optimal solutions.
I used
Python 3.x
Matplotlib
NumPy
Data Processing
The getData function, located in **RegExService.py**, is responsible for extracting relevant information from the input file containing problem data. This function utilizes regular expressions to parse the file and extract the following information:
Optimal Value: The optimal solution value or the best value found in the content of the file.
Capacity: The capacity of the vehicles for the CVRP instance.
Graph Information: Coordinates of the nodes in the graph along with their corresponding identifiers.
Demand Information: Demand of each customer node.
The extracted information is then organized and returned as a tuple containing capacity, graph, demand, and optimalValue.
The getData function is invoked within the generateGraph function in the ACO-CVRP algorithm. It retrieves the necessary data required to construct the graph representation of the CVRP instance.
Upon execution, the algorithm will print the progress of each iteration, including the best solution found so far and the optimal solution for comparison.
