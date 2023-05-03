import matplotlib.pyplot as plt
import math
import RegExService
import random
import numpy
from functools import reduce
import sys
import getopt


# Default parameter values
alpha = 2
beta = 3
sigma = 1
rho = 0.9
theta = 80
fileName = "E-n101-k14.txt"
iterations = 1000
ants = 101

# Generate the graph from the given file
def generateGraph():
    # RegExService to extract data from the file
    capacity_Limit, graph, demand, optimal_Value = RegExService.getData(fileName)
    # list of all vertices in the graph, except the depot (vertex 1)
    vertices = list(graph.keys())
    vertices.remove(1)

    # all edges in the graph and their distances
    edges = { (min(a,b),max(a,b)) : numpy.sqrt((graph[a][0]-graph[b][0])**2 + (graph[a][1]-graph[b][1])**2) for a in graph.keys() for b in graph.keys()}
    # pheromone levels for all edges in the graph
    pheromones = {(min(a, b), max(a, b)) : 1 for a in graph.keys() for b in graph.keys() if a != b}
    # Return all the relevant graph information
    return vertices, edges, capacity_Limit, demand, pheromones, optimal_Value

# Generate a solution for 1. ant
def solutionOfOneAnt(vertices, edges, capacity_Limit, demand, pheromones):
    solution = list()
    # Repeat until all vertices have been visited
    while(len(vertices)!=0):
        path = list()
        # Choose a random vertex as the starting city
        city = numpy.random.choice(vertices)
        # Subtract the demand of the 1st city from the capacity limit
        capacity = capacity_Limit - demand[city]
        # Add the 1st city to the current path and remove it from the list of remaining vertices
        path.append(city)
        vertices.remove(city)
        # Repeat until capacity gets over or there are no remaining places to visit
        while(len(vertices)!=0):
            # Calculate the probability of each remaining vertex being the next city to visit
            probabilities = list(map(lambda x: ((pheromones[(min(x, city), max(x, city))]) ** alpha) * ((1 / edges[(min(x, city), max(x, city))]) ** beta), vertices))
            probabilities = probabilities/numpy.sum(probabilities)
            # Choose the next city based on the calculated probabilities
            city = numpy.random.choice(vertices, p=probabilities)
            # Subtract the demand of the next city from the capacity limit
            capacity = capacity - demand[city]
            # If there is still capacity, add the next city to the current path and remove it from the list of remaining vertices
            if (capacity>0):
                path.append(city)
                vertices.remove(city)
            else:
                # If there is no more capacity left, break the loop
                break
    # Add the current path to the solution
        solution.append(path)
# Return the solution
    return solution
# Calculate the distance of a given solution
def rateSolution(solution, edges):
    s = 0
    for i in solution:
        a = 1
        for j in i:
            b = j
            # Add the distance between each pair of consecutive cities in the path
            s = s + edges[(min(a,b), max(a,b))]
            a = b
        b = 1
        s = s + edges[(min(a,b), max(a,b))]
    return s

def updateFeromone(pheromones, solutions, bestSolution):
    # Calculate the average length of all solutions
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
    # Update pheromone level for each edge
    pheromones = {k : (rho + theta / Lavg) * v for (k, v) in pheromones.items()}
    # Sort the solutions by length
    solutions.sort(key = lambda x: x[1])
    # If a best solution already exists, check if the new best solution is better and update pheromones for its edges
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = sigma / bestSolution[1] + pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))]
    # If no best solution exists yet, set it to the first solution and update pheromones for its edges
    else:
        bestSolution = solutions[0]
        # Update pheromones for each edge in each solution, with decreasing importance based on the solution's rank
    for l in range(sigma):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = (sigma - (l + 1) / L ** (l + 1)) + pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))]
    return bestSolution


def main():
    # Initialize variables and generate a graph
    bestSolution = None
    vertices, edges, capacity_Limit, demand, pheromones, optimal_Value = generateGraph()
    # Run the algorithm for the given number of iterations
    for i in range(iterations):
        solutions = list()
        # Generate a solution for each ant
        for _ in range(ants):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacity_Limit, demand, pheromones)
            solutions.append((solution, rateSolution(solution, edges)))
        # Update the pheromones and the best solution
        bestSolution = updateFeromone(pheromones, solutions, bestSolution)
        # Print the updates
        print(str(i)+":\t"+str(int(bestSolution[1]))+"\t"+str(optimal_Value))
    return bestSolution

if __name__ == "__main__":
    # Parse command line arguments
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "f:a:b:s:r:t:i:n:",["fileName=",
        "alpha=","beta=","sigma=","rho=","theta=","iterations=","numberOfAnts="])
    except getopt.GetoptError:
        # If there is an error in parsing the arguments, prompts usage instructions and the script exits
        print("""use: python ACO_CVRP.py 
            -f <fileName> 
            -a <alpha> 
            -b <beta> 
            -s <sigma> 
            -r <rho> 
            -t <theta>
            -i <iterations>
            -n <numberOfAnts>

            Default values:
            fileName: E-n101-k14.txt
            alpha: 80
            beta: 5
            sigma: 3
            rho: 0.8
            theta: 80
            iterations: 1000
            number of ants: 101""")
        sys.exit(2)
    # Parse the arguments and update the corresponding parameter values
    for opt,arg in opts:
        if(opt in ("-a", "--alpha")):
            alpha = float(arg)
        elif(opt in ("-b", "--beta")):
            beta = float(arg)
        elif(opt in ("-s", "--sigma")):
            sigma = float(arg)
        elif(opt in ("-r", "--rho")):
            rho = float(arg)
        elif(opt in ("-t", "--theta")):
            theta = float(arg)
        elif(opt in ("-f", "--fileName", "--file")):
            fileName = str(arg)
        elif(opt in ("-i", "--iterations")):
            iterations = int(arg)
        elif(opt in ("-n", "--numberOfAnts")):
            ants = int(arg)
    # Print the parameter values for confirmation
    print("file name:\t" + str(fileName) +
"\nalpha:\t" + str(alpha) +
"\nbeta:\t" + str(beta) +
          "\nsigma:\t" + str(sigma) +
          "\nrho:\t" + str(rho) +
          "\ntheta:\t" + str(theta) +
          "\niterations:\t" + str(iterations) +
          "\nnumber of ants:\t" + str(ants))
    # Call the main function to solve the CVRP using ACO and save the solution
    solution = main()
    # Print the solution
    print("Solution: "+str(solution))
    # If the file name is E-n22-k4.txt, print the known optimal solution for comparison
    if(fileName=="E-n22-k4.txt"):
        optimalSolution = ([[18, 21, 19, 16, 13], [17, 20, 22, 15], [14, 12, 5, 4, 9, 11], [10, 8, 6, 3, 2, 7]], 375)
        print("Optimal solution: "+str(optimalSolution))
    if(fileName=="E-n33-k4.txt"):
        optimalSolution = ([[1, 15, 26, 27, 16, 28, 29], [30, 14, 31], [3, 5, 6, 10, 18, 19, 22, 21, 20, 23, 24, 25, 17, 13], [2, 12, 11, 32, 8, 9, 7, 4]], 835)
        print("Optimal solution: "+str(optimalSolution))
    if(fileName=="E-n51-k5.txt"):
        optimalSolution = ([[5, 49, 10, 39, 33, 45, 15, 44, 37, 17, 12], [47, 4, 42, 19, 40, 41, 13, 18], [46, 32, 1, 22, 20, 35, 36, 3, 28, 31, 26, 8], [6, 14, 25, 24, 43, 7, 23, 48, 27], [11, 16, 2, 29, 21, 50, 34, 30, 9, 38]], 521)
        print("Optimal solution: "+str(optimalSolution))




