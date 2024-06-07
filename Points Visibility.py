import matplotlib.pyplot as plt
import random
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon

def create_closed_polygon():
    while True:
        num_edges = random.randint(6, 100)  # Randomly generate the number of edges
        polygon_edges = []  # Store the coordinates of polygon edges

        # Generate random vertices
        for _ in range(num_edges):
            x = random.uniform(-10, 10)  # Random x-coordinate
            y = random.uniform(-10, 10)  # Random y-coordinate
            polygon_edges.append((x, y))

        # Create a Shapely Polygon object
        polygon = Polygon(polygon_edges)

        # Check if the polygon is simple
        if polygon.is_simple:
            break

    # Connect the points to form sides of the polygon
    polygon_sides = [(polygon_edges[i], polygon_edges[(i + 1) % num_edges]) for i in range(num_edges)]

    print("Polygon Edges:", polygon_edges)
    print("Polygon Sides:", polygon_sides)

    return polygon_edges, polygon_sides

def plot_lines_from_vertex(vertex, polygon_edges):
    # Generate random points until a point inside the polygon is found
    while True:
        x_vertex = random.uniform(min(x for x, y in polygon_edges), max(x for x, y in polygon_edges))
        y_vertex = random.uniform(min(y for x, y in polygon_edges), max(y for x, y in polygon_edges))
        vertex = (x_vertex, y_vertex)
        if Point(vertex).within(Polygon(polygon_edges)):
            break
    
    lines = [(vertex, polygon_edges[i]) for i in range(len(polygon_edges))]  # Include all edges
    vertex_label = 'X'  # Label for the vertex inside the polygon
    lines_labels = [f"{vertex_label}{chr(65 + i)}" for i in range(len(polygon_edges))]  # Labels for lines

    # Plot lines from the vertex to each polygon vertex
    x_vertex, y_vertex = zip(*[vertex] * len(polygon_edges))  # Include all edges
    x_polygon, y_polygon = zip(*polygon_edges)  # Include all edges
    plt.plot(x_vertex, y_vertex, marker='o', linestyle='--', color='r', label='Lines from Vertex')
    for line, label in zip(lines, lines_labels):
        x_line, y_line = zip(*line)
        plt.plot(x_line, y_line, linestyle='--', color='r')
        # Plot labels for lines
        mid_x = (line[0][0] + line[1][0]) / 2
        mid_y = (line[0][1] + line[1][1]) / 2
        plt.text(mid_x, mid_y, label, fontsize=10, ha='right', va='bottom')
    
    return lines, lines_labels  # Return the lines and labels
 
def find_non_intersecting_lines(lines, polygon_sides, polygon_edges):
    nonintersectlines = []
    nonintersectline_labels = []

    for line in lines:
        line_to_check = LineString([Point(line[0]), Point(line[1])])

        # Check if the line ends at any polygon edge
        ends_at_polygon_edge = line[1] in polygon_edges

        # Check if the line intersects with any polygon side (excluding the edge it ends at)
        intersects = any(
            LineString([(x1, y1), (x2, y2)]).crosses(line_to_check) and ((x1, y1), (x2, y2)) != ((line[0]), line[1])
            for side_start, side_end in polygon_sides
            for x1, y1, x2, y2 in [(side_start[0], side_start[1], side_end[0], side_end[1])]
        )

        # Check if the line passes through a polygon edge and ends at another polygon edge
        passes_through_ends_at_polygon_edge = (
            line_to_check.touches(Point(line[1])) and line_to_check.crosses(LineString(polygon_edges))
        )

        if ends_at_polygon_edge and not intersects and not passes_through_ends_at_polygon_edge:
            nonintersectlines.append(line)
            nonintersectline_labels.append(f"X{chr(65 + polygon_edges.index(line[1]))}")

    print("Non-intersecting Lines:", nonintersectlines)
    print("Non-intersecting Lines Labelled:", nonintersectline_labels)

    return nonintersectlines, nonintersectline_labels

def create_polygon_sides(polygon_edges):
    polygon_sides = [(polygon_edges[i], polygon_edges[(i + 1) % len(polygon_edges)]) for i in range(len(polygon_edges))]
    return polygon_sides

# Example usage:
polygon_edges, polygon_sides = create_closed_polygon()
polygon_sides = create_polygon_sides(polygon_edges)

# Input for Part B (vertex is set to None for random selection)
lines, lines_labels = plot_lines_from_vertex(None, polygon_edges)

# Check for non-intersecting lines
nonintersectlines, nonintersectline_labels = find_non_intersecting_lines(lines, polygon_sides, polygon_edges)

# Plotting the polygon edges
x_polygon, y_polygon = zip(*polygon_edges)  # Include all edges
plt.plot(x_polygon + (x_polygon[0],), y_polygon + (y_polygon[0],), linestyle='-', color='b', label='Polygon Edges')

# Displaying all three lists
print("Closed Polygon Edges:", polygon_edges)
print("Polygon Sides:", polygon_sides)
#print("Polygon Edges Labelled:", polygon_edge_labels)
print("Lines from Vertex to Polygon Edges:", lines)
print("Lines from Vertex to Polygon Edges Labelled:", lines_labels)

# Display non-intersecting lines only if there are any
if nonintersectlines:
    print("Non-intersecting Lines:", nonintersectlines)
    print("Non-intersecting Lines:", nonintersectline_labels)
    
    # Additional plot settings for non-intersecting lines
    for line in nonintersectlines:
        x_nonintersect, y_nonintersect = zip(*line)
        plt.plot(x_nonintersect, y_nonintersect, linestyle='-', color='g', label='Non-intersecting Lines')

# Additional plot settings
plt.title("Closed Polygon, Lines from Vertex, and Non-intersecting Lines")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.grid(True)
plt.show()