import re

def getData(fileName):
    # Open the file for reading
    f = open(fileName, "r")
    # Read the entire contents of the file
    content = f.read()
    # Search for the optimal value in the content of the file
    optimalValue = re.search("Optimal value: (\d+)", content, re.MULTILINE)
    # If the optimal value is not found, search for the best value
    if(optimalValue != None):
        optimalValue = optimalValue.group(1)
    else:
        optimalValue = re.search("Best value: (\d+)", content, re.MULTILINE)

        if(optimalValue != None):
            optimalValue = optimalValue.group(1)
    # Search for the capacity of the problem
    capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)
    # Find all the lines in the file that contain graph information
    graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
    # Find all the lines in the file that contain demand information
    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    # Convert the graph information to a dictionary with node as key and (x, y) tuple as value
    graph = {int(a):(int(b),int(c)) for a,b,c in graph}
    # Convert the demand information to a dictionary with node as key and demand as value
    demand = {int(a):int(b) for a,b in demand}
    # Convert capacity and optimalValue to integers
    capacity = int(capacity)
    optimalValue = int(optimalValue)
    # Return the capacity, graph, demand, and optimalValue as a tuple
    return capacity, graph, demand, optimalValue