from tkinter import *
from tkinter import ttk
import random
import time

root = Tk()
root.title("Sorting Algorithm Visualization")
root.maxsize(900, 800)
root.config(bg="black")

# Variables
selected_algo = StringVar()
data = []  # Global Data Array


def draw_data(data, color_array):
    # Clear the canvas every time you want to redraw the rectangles (plot)
    canvas.delete("all")

    canvas_height = 380
    canvas_width = 800  # Canvas cuts off some of plot if set to 600, but why?!
    x_width = canvas_width / (len(data) + 1)
    offset = 10
    spacing = 10

    # Normalize the data (making the value between 0 - 1, so that you can then adjust the scaling based on the size
    # of the canvas (so by pixel height). This helps for when you have values that are very small.
    normalize_data = [(h / max(data)) for h in data]

    for i, height in enumerate(normalize_data):
        # .create_rectangle requires x1, y1, x2, y2 (think bottom left corner, top right corner)
        # Top Left
        x0 = i * x_width + offset + spacing
        y0 = canvas_height - height * 340  # Multiply by 340 to adjust scaling since we normalized the data points
        # Bottom Right
        x1 = (i + 1) * x_width + offset
        y1 = canvas_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        canvas.create_text(x0 + 2, y0, anchor=SW, text=str(data[i]))

    # Show Sorting Updates // *NOTE: root.update_idletasks() did not work.
    root.update()


def generate():
    global data

    try:
        min_val = int(min_entry.get())
    except:
        min_val = 1

    try:
        max_val = int(max_entry.get())
    except:
        max_val = 10

    try:
        size_val = int(size_entry.get())
    except:
        size_val = 10

    if min_val < 0:
        min_val = 0

    if max_val > 100:
        max_val = 100

    if size_val > 50 or size_val < 3:
        size_val = 50

    if min_val > max_val:
        min_val, max_val = max_val, min_val

    data = []
    for _i in range(0, size_val):
        data.append(random.randrange(min_val, max_val + 1))

    color_array = ["red" for _i in range(0, len(data))]  # Produces ["red", "red", "red", ...]
    draw_data(data, color_array)


# Helper function to call upon the selected algo function
# Algo Functions at the bottom of this file
def sort_selection():
    global data

    current_sort = selected_algo.get()
    if current_sort == "Bubble Sort":
        bubble_sort(data, sort_speed.get())

    elif current_sort == "Heap Sort":
        heap_sort(data, sort_speed.get())

    elif current_sort == "Merge Sort":
        merge_sort(data, 0, len(data) - 1, sort_speed.get())

    else:
        quick_sort(data, 0, len(data) - 1, sort_speed.get())

    # Completion = All bars become green
    color_array = ["green" for _i in range(0, len(data))]
    draw_data(data, color_array)


# Frame / Base Layout
UI_FRAME = Frame(root, width=800, height=200, bg="white")
UI_FRAME.grid(row=0, column=0, padx=10, pady=5)

canvas = Canvas(root, width=800, height=380, bg="white")
canvas.grid(row=1, column=0, padx=10, pady=5)

# User Interface Layout
# Row[0 & 1] -----

# Array Size
Label(UI_FRAME, text="Size [3-25]", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=S)
size_entry = Entry(UI_FRAME)
size_entry.grid(row=1, column=0, padx=5, pady=5, sticky=W)

# Min Value Entry
Label(UI_FRAME, text="Min Value [0]", bg="white").grid(row=0, column=1, padx=5, pady=5)
min_entry = Entry(UI_FRAME)
min_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# Max Value Entry
Label(UI_FRAME, text="Max Value [100]", bg="white").grid(row=0, column=2, padx=5, pady=5)
max_entry = Entry(UI_FRAME)
max_entry.grid(row=1, column=2, padx=5, pady=5, sticky=W)

# Row[2] -----

# Generate Array Button
ttk.Button(UI_FRAME, text="Generate Array", command=generate, width=11).grid(row=2, column=1, padx=5, pady=5)

# Row[2 & 3] -----

# Sorting Speed Slider
Label(UI_FRAME, text="Sort Speed [Fast->Slow]", bg="white").grid(row=2, column=0, padx=5, pady=5)
sort_speed = ttk.Scale(UI_FRAME, from_=.1, to=2, orient=HORIZONTAL, length=190, value=.1)
sort_speed.grid(row=3, column=0, padx=5, pady=5)

# Sorting Method Selection
Label(UI_FRAME, text="Algorithm: ", bg="white").grid(row=2, column=2, padx=5, pady=5)
algo_menu = ttk.Combobox(UI_FRAME, textvariable=selected_algo, width=18, values=[
    "Bubble Sort", "Heap Sort", "Merge Sort", "Quick Sort"]
                         )
algo_menu.grid(row=3, column=2, padx=5, pady=5)
algo_menu.current(0)

# Row[4] -----

# Sort Array Button
ttk.Button(UI_FRAME, text="Sort", command=sort_selection, width=11, style="TButton").grid(row=4, column=1, padx=5, pady=5)


# ALGORITHMS -----

# Bubble Sort --> https://www.geeksforgeeks.org/python-program-for-bubble-sort/
def bubble_sort(data, sort_speed):
    for i in range(0, len(data) - 1):
        for j in range(0, len(data) - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                color_array = ["green" if x == j or x == (j + 1) else "red" for x in range(0, len(data))]
                draw_data(data, color_array)
                time.sleep(sort_speed)
    # print(data)


# Bubble Sort -->  https://www.geeksforgeeks.org/heap-sort/
def heap_sort(data, sort_speed):
    n = len(data)

    # Max Heap Function (1st step in algo)
    for i in range((n // 2) - 1, -1, -1):
        heapify(data, n, i, sort_speed)

    # Heapify Function (2nd step after creating the max heap)
    for i in range(n-1, 0, -1):
        data[i], data[0] = data[0], data[i]
        heapify(data, i, 0, sort_speed)


# Heap Sort Helper Function
def heapify(data, n, i, sort_speed):
    largest_val = i  # Largest Valued Index
    # print(largest_val)
    l_child = (2 * i) + 1  # Left Child Index
    r_child = (2 * i) + 2  # Right Child Index
    # print(l_child, r_child)

    draw_data(data, hs_get_color_array(len(data), l_child, r_child, largest_val))
    time.sleep(sort_speed)

    if l_child < n and data[i] < data[l_child]:  # Check if the left child is larger than the parent
        largest_val = l_child

        draw_data(data, hs_get_color_array(len(data), l_child, r_child, largest_val))
        time.sleep(sort_speed)

    if r_child < n and data[largest_val] < data[r_child]:  # Check if the right child is larger than the parent
        largest_val = r_child

        draw_data(data, hs_get_color_array(len(data), l_child, r_child, largest_val))
        time.sleep(sort_speed)

    # i is initialized from the end of the data array, so by swapping below, we move the larger value to the end = sort
    if largest_val != i:  # Sort of a Base Case, which will end a recursive run of the heapify function
        data[i], data[largest_val] = data[largest_val], data[i]  # Swap parent and larger valued child indices

        draw_data(data, hs_get_color_array(len(data), l_child, r_child, largest_val))
        time.sleep(sort_speed)

        heapify(data, n, largest_val, sort_speed)


# Merge Sort --> https://www.geeksforgeeks.org/merge-sort/ * Visualization purposes needed it down inplace *
def merge_sort(data, left, right, sort_speed):
    if left < right:
        middle = (left + right) // 2  # Split Point Index
        merge_sort(data, left, middle, sort_speed)  # Split the function down by splitting it in half recursively
        merge_sort(data, middle + 1, right, sort_speed)
        merge(data, left, middle, right, sort_speed)  # This compares and merges the elements back together in order


# Merge Sort Helper Function
def merge(data, left, middle, right, sort_speed):
    draw_data(data, ms_get_color_array(len(data), left, middle, right))
    time.sleep(sort_speed)

    left_half = data[left: middle+1]
    right_half = data[middle+1: right + 1]

    l_index = r_index = 0

    for data_index in range(left, right + 1):
        if l_index < len(left_half) and r_index < len(right_half):
            if left_half[l_index] <= right_half[r_index]:
                data[data_index] = left_half[l_index]
                l_index += 1
            else:
                data[data_index] = right_half[r_index]
                r_index += 1

        elif l_index < len(left_half):
            data[data_index] = left_half[l_index]
            l_index += 1
        else:
            data[data_index] = right_half[r_index]
            r_index += 1

    draw_data(data, ["green" if left <= x <= right else "white" for x in range(0, len(data))])
    time.sleep(sort_speed)


# Quick Sort --> https://www.geeksforgeeks.org/quick-sort/
def quick_sort(data, low, high, sort_speed):
    if low < high:  # Base Case
        p_i = partition(data, low, high, sort_speed)  # Helper function that returns the partition index

        quick_sort(data, low, p_i - 1, sort_speed)  # Left side of partition index, which will run 1st in the animation
        quick_sort(data, p_i + 1, high, sort_speed)  # Right side of partition index


# Quick Sort Helper Function
def partition(data, low, high, sort_speed):
    i = (low - 1)  # This points to an element of smaller value, and stops before a larger value than the pivot
    pivot = data[high]

    draw_data(data, qs_get_color_array(len(data), low, high, i))
    time.sleep(sort_speed)

    for j in range(low, high):
        if data[j] < pivot:
            i += 1  # This now points to an element with value greater than the pivot value
            data[i], data[j] = data[j], data[i]  # Swap these values putting the larger value further to the right

            draw_data(data, qs_get_color_array(len(data), low, high, i, j))
            time.sleep(sort_speed)

    data[i + 1], data[high] = data[high], data[i + 1]  # This swaps the final larger value with the pivot itself

    draw_data(data, qs_get_color_array(len(data), low, high, i))
    time.sleep(sort_speed)

    return i + 1  # This is the final position of the pivot index


# ----- Below are specific coloring functions per sort type ------

def hs_get_color_array(data_length, l_child, r_child, largest_val):
    color_array = ["red" for _i in range(0, len(data))]

    if l_child < data_length:
        color_array[l_child] = "blue"
    if r_child < data_length:
        color_array[r_child] = "blue"
    color_array[largest_val] = "yellow"

    return color_array


def ms_get_color_array(data_length, left, middle, right):
    color_array = []

    for i in range(0, data_length):
        if left <= i <= right:
            if left <= i <= middle:
                color_array.append("yellow")
            else:
                color_array.append("pink")
        else:
            color_array.append("white")

    return color_array


def qs_get_color_array(data_length, low, high, smaller_val, comparison_val=None):
    color_array = ["red" for _i in range(0, data_length)]  # Base coloring is all red
    for i in range(0, data_length):
        if i == low:
            color_array[i] = "green"
        elif i == high:
            color_array[i] = "green"
        if i == smaller_val:
            color_array[i] = "purple"
        if i == comparison_val:
            color_array[i] = "blue"

    return color_array


root.mainloop()
