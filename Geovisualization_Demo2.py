__author__ = "John K. Tran (johtran@deloitte.com)"

import Tkinter as tk
import ttk
import shapefile as shp # Download pyshp from https://pypi.python.org/pypi/pyshp
from dbfpy import dbf # Download dbfpy from http://dbfpy.sourceforge.net/

# Read the "Test" shapefile and dbf file
test_shp = shp.Reader("Test")
test_dbf = dbf.Dbf("Test.dbf", True)

x_min, y_min, x_max, y_max = test_shp.bbox # Bounding box for shapefile
x_range, y_range = x_max-x_min, y_max-y_min # Get horizontal/vertical extent
metadata = test_dbf.header.__str__() # Nice metadata info on table
header = test_dbf.fieldNames # Header row in a list
shaperecords = test_shp.shapeRecords() # Shape and record rows
records = [rec.asList() for rec in test_dbf] # Record rows in a list
canvas_shapes = [] # Store list of x,y to input into create_polygon method

for shaperecord in shaperecords:
    if shaperecord.shape.parts.tolist() == [0]: # If polygon has only 1 part...
        points = shaperecord.shape.points
        xy_list = []
        for point in points:
            x, y = point[0], point[1]
            xy_list.append(x)
            xy_list.append(y)
        canvas_shapes.append(xy_list) # Append x, y coords to canvas_shapes
    else: # If polygon is a multi-part feature...
        shaperecord.shape.parts.extend([-1]) # read each part sequentially
        for i, j in zip(shaperecord.shape.parts, shaperecord.shape.parts[1:]):
            points = shaperecord.shape.points[i:j]
            xy_list = []
            for point in points:
                x, y = point[0], point[1]
                xy_list.append(x)
                xy_list.append(y)
            canvas_shapes.append(xy_list) # Append x, y coords to canvas_shapes

# Initialize root and canvas
root = tk.Tk()
canvas_width, canvas_height = 500, 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height,
                   background="#FFFFFF")

# Create a range of hex colors
colors = ['0', '1', '2', '3', '4', '5', '6', '7',
          '8', '9', "A", "B", "C", "D", "E", "F"]
colorrange = [i+j for i in colors for j in colors]

# Determine conversion ratio for x,y coords to window coords
ratio_x = x_range/canvas_width
ratio_y = y_range/canvas_height
ratio = ratio_x if ratio_x > ratio_y else ratio_y

# Convert x,y coordinates to window coordinates
canvas_shapes_window = []
shapes = []
for xy_list in canvas_shapes:
    canvas_shapes_window = []
    for val in xy_list:
        if xy_list.index(val) % 2 == 0:
            canvas_shapes_window.append((val-x_min)/ratio)
        else:
            canvas_shapes_window.append((y_max-val)/ratio)

    c = canvas.create_polygon(canvas_shapes_window,
                              fill="#99FFCC",
                              outline="#000000",
                              width=0.1)
    shapes.append(c)

# Finalize canvas onto grid
canvas.grid(row=0, column=0, rowspan=3, sticky="NSEW")

# Crete treeiew object for attribute table
tree = ttk.Treeview(root)

# Populate attributes for each row
for i, record in enumerate(records):
    tree.insert("", "end", "test{0}".format(i), text=record[0], values=record[1:])

# Configure table headers
tree.configure(columns=header[1:])
tree.column("#0", width=75, anchor='center')
tree.heading("#0", text=header[0])
for head in header[1:]:
    tree.column(head, width=100, anchor='center')
    tree.heading(head, text=head)

# Finalize treeview onto grid
tree.grid(row=1, column=1, rowspan=1, sticky="NSEW")

# Add attribute table label
at_label = ttk.Label(root, text="***SHAPEFILE METADATA***\n"+metadata, background="#FFFFCC")
at_label.grid(row=0, column=1, columnspan=2, sticky="EW")

# Add scrollbars to treeview
x_scrollbar = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
x_scrollbar.grid(row=2, column=1, sticky="EW")
tree.configure(xscrollcommand=x_scrollbar.set)
y_scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
y_scrollbar.grid(row=1, column=2, sticky="NS")
tree.configure(yscrollcommand=y_scrollbar.set)

# Create frame for navigation buttons
frame = ttk.Frame(root)
frame.grid(row=2, column=0, sticky="W")

# Create zoom and pan buttons for canvas
def zoom_in():
    for shape in shapes:
        canvas.scale(shape, canvas_width/2.0, canvas_height/2.0, 1.0/0.75, 1.0/0.75)
def zoom_out():
    for shape in shapes:
        canvas.scale(shape, canvas_height/2.0, canvas_width/2.0, 0.75, 0.75)
def pan_left():
    for shape in shapes:
        canvas.move(shape, 50.0, 0.0)
def pan_right():
    for shape in shapes:
        canvas.move(shape, -50.0, 0.0)
def pan_up():
    for shape in shapes:
        canvas.move(shape, 0.0, 50.0)
def pan_down():
    for shape in shapes:
        canvas.move(shape, 0.0, -50.0)

zoom_in_button = ttk.Button(frame, text="Zoom In", command=zoom_in)
zoom_out_button = ttk.Button(frame, text="Zoom Out", command=zoom_out)
pan_up_button = ttk.Button(frame, text="Pan Up", command=pan_up)
pan_down_button = ttk.Button(frame, text="Pan Down", command=pan_down)
pan_left_button = ttk.Button(frame, text="Pan Left", command=pan_left)
pan_right_button = ttk.Button(frame, text="Pan Right", command=pan_right)

zoom_in_button.grid(row=0, column=1)
zoom_out_button.grid(row=1, column=1)
pan_up_button.grid(row=0, column=0)
pan_down_button.grid(row=1, column=0)
pan_left_button.grid(row=2, column=0)
pan_right_button.grid(row=2, column=1)


root.mainloop()
