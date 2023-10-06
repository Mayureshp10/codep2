import random
import math
import time

# Function to calculate the orientation of three points
def calculate_orientation(a, b, c):
    cross_product = (b[1] - a[1]) * (c[0] - b[0]) - (c[1] - b[1]) * (b[0] - a[0])
    return 0 if cross_product == 0 else (1 if cross_product > 0 else -1)

# Function to merge two convex hulls
def merge_hulls(left_hull, right_hull):
    # Find the rightmost point in the left convex hull
    left_idx = max(range(1, len(left_hull)), key=lambda i: left_hull[i][0])

    # Find the leftmost point in the right convex hull
    right_idx = min(range(1, len(right_hull)), key=lambda i: right_hull[i][0])

    left_x, right_x = left_idx, right_idx
    done = False

    # Compute the upper tangent
    while not done:
        done = True

        # Find the next point in the left convex hull
        while calculate_orientation(right_hull[right_x], left_hull[left_x], left_hull[(left_x + 1) % len(left_hull)]) >= 0:
            left_x = (left_x + 1) % len(left_hull)

        # Find the next point in the right convex hull
        while calculate_orientation(left_hull[left_x], right_hull[right_x], right_hull[(len(right_hull) + right_x - 1) % len(right_hull)]) <= 0:
            right_x = (right_x - 1) % len(right_hull)
            done = False

    upper_left, upper_right = left_x, right_x
    left_x, right_x = left_idx, right_idx
    done = False

    # Compute the lower tangent
    while not done:
        done = True

        # Find the next point in the left convex hull
        while calculate_orientation(left_hull[left_x], right_hull[right_x], right_hull[(right_x + 1) % len(right_hull)]) >= 0:
            right_x = (right_x + 1) % len(right_hull)

        # Find the next point in the right convex hull
        while calculate_orientation(right_hull[right_x], left_hull[left_x], left_hull[(len(left_hull) + left_x - 1) % len(left_hull)]) <= 0:
            left_x = (left_x - 1) % len(left_hull)
            done = False

    merged = []
    lower_left, lower_right = left_x, right_x

    # Merge the upper and lower hulls
    index = upper_left
    merged.append(left_hull[upper_left])
    while index != lower_left:
        index = (index + 1) % len(left_hull)
        merged.append(left_hull[index])

    index = lower_right
    merged.append(right_hull[lower_right])
    while index != upper_right:
        index = (index + 1) % len(right_hull)
        merged.append(right_hull[index])

    return merged

# Function to calculate the convex hull using the divide-and-conquer approach
def convex_hull_divide_and_conquer(points):
    n = len(points)

    if n <= 3:
        return points

    # Sort the points by x-coordinate
    points.sort()

    # Divide the points into two halves
    left_half = points[:n // 2]
    right_half = points[n // 2:]

    # Recursively find the convex hull of each half
    left_hull = convex_hull_divide_and_conquer(left_half)
    right_hull = convex_hull_divide_and_conquer(right_half)

    # Merge the convex hulls of the two halves
    return merge_hulls(left_hull, right_hull)

if __name__ == '__main__':
    # Input points
    input_points = [
         (15, 47), (38, 12), (92, 61), (54, 38), (77, 84),
    (26, 73), (61, 19), (42, 66), (33, 55), (70, 29)
    ]

    # Measure the execution time
    start_time = time.perf_counter_ns()
    convex_hull = convex_hull_divide_and_conquer(input_points)
    end_time = time.perf_counter_ns()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} nano seconds")

    print('Convex Hull:')
    for point in convex_hull:
        print(int(point[0]), int(point[1]))
