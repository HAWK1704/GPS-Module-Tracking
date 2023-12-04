import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkintermapview import TkinterMapView
import time
import threading
import serial.tools.list_ports
import csv

ports = serial.tools.list_ports.comports()

portsList = []
data_list = []

with open('data.csv', 'r', newline='') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        data_list.append(row)

for onePort in ports:
    portsList.append(str(onePort))

print(portsList)

portvar = input('Input Port number :')

portvar='COM'+portvar


serialInst = serial.Serial(baudrate=9600,port=portvar)
# Check if the serial port is already open
if not serialInst.is_open:
    serialInst.open()
else:
    print("Serial port is already open.")

# def initialize_serial_port():
#     serialInst.open()
    # try:
    #     serialInst.open()
    # except serial.SerialException as e:
    #     messagebox.showerror("Serial Port Error", f"Error: {e}\nMake sure the Arduino is connected.")
    #     return False

    # return True

V1_x = 50
V2_x = 50
V3_x = 50

def resize_image(image_path, width, height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height), Image.BILINEAR)
    return ImageTk.PhotoImage(resized_image)

def is_numeric_input(P):
    try:
        float(P)
        return True
    except ValueError:
        return False

def toggle_fullscreen(window):
    state = not window.attributes("-fullscreen")
    window.attributes("-fullscreen", state)

# Function to simulate vehicle movement for V1
def move_V1_simulator(V1_veh_label, V1_gar_label, garage_image_path):
    global V1_x
    move_speed = 5
    while V1_x < V1_veh_label.winfo_screenwidth()-130:
        V1_x += move_speed
        V1_veh_label.place(x=V1_x, y=20)
        if V1_x >= V1_veh_label.winfo_screenwidth()-131:
            V1_veh_label.place_forget()
            garage_image = resize_image(garage_image_path, 50, 50)
            V1_gar_label.config(image=garage_image)
            V1_gar_label.image = garage_image
            messagebox.showinfo("Vehicle Reached Destination", "V1 has reached its destination!")
            break
        root.update()
        time.sleep(0.1)

# Function to simulate vehicle movement for V2
def move_V2_simulator(V2_veh_label, V2_gar_label, garage_image_path):
    global V2_x
    move_speed = 2
    while V2_x < V2_veh_label.winfo_screenwidth()-130:
        V2_x += move_speed
        V2_veh_label.place(x=V2_x, y=70)
        if V2_x >= V2_veh_label.winfo_screenwidth() - 131:
            V2_veh_label.place_forget()
            garage_image = resize_image(garage_image_path, 50, 50)
            V2_gar_label.config(image=garage_image)
            V2_gar_label.image = garage_image
            messagebox.showinfo("Vehicle Reached Destination", "V2 has reached its destination!")
            break
        root.update()
        time.sleep(0.1)

# Function to simulate vehicle movement for V3
def move_V3_simulator(V3_veh_label, V3_gar_label, garage_image_path):
    global V3_x
    move_speed = 3
    while V3_x < V3_veh_label.winfo_screenwidth() - 130:
        V3_x += move_speed
        V3_veh_label.place(x=V3_x, y=120)
        if V3_x >= V3_veh_label.winfo_screenwidth() - 131:
            V3_veh_label.place_forget()
            garage_image = resize_image(garage_image_path, 50, 50)
            V3_gar_label.config(image=garage_image)
            V3_gar_label.image = garage_image
            messagebox.showinfo("Vehicle Reached Destination", "V3 has reached its destination!")
            break
        root.update()
        time.sleep(0.1)

def initialize_labels(labels_frame, map_and_labels_window):
    # Determine the screen width
    screen_width = map_and_labels_window.winfo_screenwidth()

    V1 = Label(labels_frame, text='V1', font=('Helvetica', 16))
    V1.grid(row=1, column=0, sticky="w")
    V1.place(x=0, y=35)

    V2 = Label(labels_frame, text='V2', font=('Helvetica', 16))
    V2.grid(row=2, column=0, sticky="w")
    V2.place(x=0, y=85)

    V3 = Label(labels_frame, text='V3', font=('Helvetica', 16))
    V3.grid(row=3, column=0, sticky="w")
    V3.place(x=0, y=135)

    V1_veh_img = resize_image('./IMAGES/car.png', 50, 50)
    V1_veh_label = Label(labels_frame, image=V1_veh_img)
    V1_veh_label.image = V1_veh_img
    V1_veh_label.grid(row=1, column=1)
    V1_veh_label.place(x=screen_width - 135, y=20)

    V2_veh_img = resize_image('./IMAGES/car (1).png', 50, 50)
    V2_veh_label = Label(labels_frame, image=V2_veh_img)
    V2_veh_label.image = V2_veh_img
    V2_veh_label.place(x=screen_width - 135, y=70)

    V3_veh_img = resize_image('./IMAGES/car (2).png', 50, 50)
    V3_veh_label = Label(labels_frame, image=V3_veh_img)
    V3_veh_label.image = V3_veh_img
    V3_veh_label.place(x=screen_width - 135, y=120)

    return V1_veh_label, V2_veh_label, V3_veh_label

def create_label_gui(map_and_labels_window):
    labels_frame = Frame(map_and_labels_window)
    labels_frame.pack(fill='both', expand=True, side=LEFT)
    labels_frame.place(relx=0, rely=0.79, relwidth=1.0, relheight=0.2)

    for i in range(7):
        labels_frame.grid_rowconfigure(i, weight=1)
    for i in range(11):
        labels_frame.grid_columnconfigure(i, weight=1)

    # Initialize vehicle labels and get references to them
    V1_veh_label, V2_veh_label, V3_veh_label = initialize_labels(labels_frame, map_and_labels_window)

    # Add garage images for V1, V2, and V3
    garage_image_path = './IMAGES/empty_garage_1.png'
    garage_image = resize_image(garage_image_path, 40, 40)

    V1_gar_label = Label(labels_frame, image=garage_image)
    V1_gar_label.image = garage_image
    V1_gar_label.place(x=map_and_labels_window.winfo_screenwidth() - 135, y=22)

    V2_gar_label = Label(labels_frame, image=garage_image)
    V2_gar_label.image = garage_image
    V2_gar_label.place(x=map_and_labels_window.winfo_screenwidth() - 135, y=71)

    V3_gar_label = Label(labels_frame, image=garage_image)
    V3_gar_label.image = garage_image
    V3_gar_label.place(x=map_and_labels_window.winfo_screenwidth() - 135, y=120)

    for i in range(11):
        percentage_label = Label(labels_frame, text=f'{i * 10}%')
        percentage_label.grid(row=0, column=i, sticky='w')

    thread_V3 = threading.Thread(
        target=lambda: move_V3_simulator(V3_veh_label, V3_gar_label, './IMAGES/full_garage_1.png'))
    thread_V3.start()

    thread_V2 = threading.Thread(
        target=lambda: move_V2_simulator(V2_veh_label, V2_gar_label, './IMAGES/full_garage_1.png'))
    thread_V2.start()

    thread_V1 = threading.Thread(
        target=lambda: move_V1_simulator(V1_veh_label, V1_gar_label, './IMAGES/full_garage_1.png'))
    thread_V1.start()

def create_map_gui(map_and_labels_window, center_lat, center_long, zoom, source_lat, source_long,
                   end_lat_1, end_long_1, end_lat, end_long, end_lat_2, end_long_2):
    map_frame = Frame(map_and_labels_window)
    map_frame.pack(fill='both', expand=True)

    earth = TkinterMapView(map_frame)
    earth.grid(row=0, column=0, sticky="nsew")

    map_frame.grid_rowconfigure(0, weight=1)
    map_frame.grid_columnconfigure(0, weight=1)

    earth.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    earth.set_position(center_lat, center_long)
    earth.set_zoom(zoom)

    marker_0 = earth.set_marker(source_lat, source_long, text='SOURCE')
    marker_1 = earth.set_marker(end_lat_1, end_long_1, text="DESTINATION 1")
    marker_2 = earth.set_marker(end_lat, end_long, text='DESTINATION 2')
    marker_3 = earth.set_marker(end_lat_2, end_long_2, text='DESTINATION 3')
    path1 = earth.set_path([(source_lat, source_long), (end_lat, end_long)])
    path2 = earth.set_path([(source_lat, source_long), (end_lat_1, end_long_1)])
    path3 = earth.set_path([(source_lat, source_long), (end_lat_2, end_long_2)])

def open_map_and_labels():
    global V1_x
    V1_x = 50
    global V2_x
    V2_x = 50
    global V3_x
    V3_x = 50

    # Function to get the latitude and longitude values or use default values
    def get_latitude_longitude_values(entry_widget, default_value):
        value = entry_widget.get()
        if not value:
            return default_value
        return float(value)

    # Get latitude and longitude values or use default values
    source_lat = float(source_latitude_entry.get())
    source_long = float(source_longitude_entry.get())
    end_lat = get_latitude_longitude_values(end_latitude_entry, float(data_list[1]['values']))
    end_long = get_latitude_longitude_values(end_longitude_entry, float(data_list[0]['values']))
    end_lat_1 = get_latitude_longitude_values(end_latitude_entry_1, float(data_list[3]['values']))
    end_long_1 = get_latitude_longitude_values(end_longitude_entry_1, float(data_list[2]['values']))
    end_lat_2 = get_latitude_longitude_values(end_latitude_entry_2, float(data_list[5]['values']))
    end_long_2 = get_latitude_longitude_values(end_longitude_entry_2, float(data_list[4]['values']))

    data = f"{end_lat} {end_long} {end_lat_1} {end_long_1} {end_lat_2} {end_long_2}"

    try:
        serialInst.write(data.encode('utf-8'))
    except Exception:
        print("NO SERIAL PORT FOUND!")

    center_lat = (source_lat + end_lat_1 + end_lat + end_lat_2) / 4
    center_long = (source_long + end_long_1 + end_long + end_long_2) / 4

    min_lat = min(source_lat, end_lat_1, end_lat, end_lat_2)
    max_lat = max(source_lat, end_lat_1, end_lat, end_lat_2)
    min_long = min(source_long, end_long_1, end_long, end_long_2)
    max_long = max(source_long, end_long_1, end_long, end_long_2)

    zoom =30
    while max_lat - min_lat > 180 / (2 ** zoom) or max_long - min_long > 360 / (2 ** zoom):
        zoom -= 1
    print(zoom)

    map_and_labels_window = Toplevel(root)
    map_and_labels_window.title('Map and Labels')
    map_and_labels_window.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    map_and_labels_window.bind("<F11>", lambda event: toggle_fullscreen(map_and_labels_window))

    create_map_gui(map_and_labels_window, center_lat, center_long, zoom, source_lat, source_long,
                   end_lat_1, end_long_1, end_lat, end_long, end_lat_2, end_long_2)

    create_label_gui(map_and_labels_window)

root = Tk()
root.title('TRACKER')
root.geometry('300x370')
img = ImageTk.PhotoImage(Image.open('./IMAGES/ait_pune_logo_jKb_icon.ico'))
img_label = Label(root, image=img)
img_label.configure(background='#0096DC')
img_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))
root.iconbitmap('./IMAGES/ait_pune_logo_jKb_icon.ico')
root.configure(background='#0096DC')
text = Label(root, text='CME', bg='#0096DC', fg='white', font=('verdana', 18))
text.grid(row=1, column=0, columnspan=2)

source_longitude = Label(root, text='SOURCE LONGITUDE', bg='#0096DC', fg='white')
source_longitude.grid(row=2, column=0)
source_longitude_entry = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"))
source_longitude_entry.grid(row=2, column=1)

source_latitude = Label(root, text='SOURCE LATITUDE', bg='#0096DC', fg='white')
source_latitude.grid(row=3, column=0)
source_latitude_entry = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"))
source_latitude_entry.grid(row=3, column=1)

end_longitude = Label(root, text='DESTINATION LONGITUDE 1', bg='#0096DC', fg='white')
end_longitude.grid(row=4, column=0)
end_longitude_entry = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[0]['values'])))
end_longitude_entry.grid(row=4, column=1)

end_latitude = Label(root, text='DESTINATION LATITUDE 1', bg='#0096DC', fg='white')
end_latitude.grid(row=5, column=0)
end_latitude_entry = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[1]['values'])))
end_latitude_entry.grid(row=5, column=1)

end_longitude_1 = Label(root, text='DESTINATION LONGITUDE 2', bg='#0096DC', fg='white')
end_longitude_1.grid(row=6, column=0)
end_longitude_entry_1 = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[2]['values'])))
end_longitude_entry_1.grid(row=6, column=1)

end_latitude_1 = Label(root, text='DESTINATION LATITUDE 2', bg='#0096DC', fg='white')
end_latitude_1.grid(row=7, column=0)
end_latitude_entry_1 = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[3]['values'])))
end_latitude_entry_1.grid(row=7, column=1)

end_longitude_2 = Label(root, text='DESTINATION LONGITUDE 3', bg='#0096DC', fg='white')
end_longitude_2.grid(row=8, column=0)
end_longitude_entry_2 = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[4]['values'])))
end_longitude_entry_2.grid(row=8, column=1)

end_latitude_2 = Label(root, text='DESTINATION LATITUDE 3', bg='#0096DC', fg='white')
end_latitude_2.grid(row=9, column=0)
end_latitude_entry_2 = Entry(root, validate="key", validatecommand=(root.register(is_numeric_input), "%P"), textvariable=tkinter.StringVar(value=float(data_list[5]['values'])))
end_latitude_entry_2.grid(row=9, column=1)

track_button = Button(root, text='START', command=open_map_and_labels)
track_button.grid(row=10, column=0, columnspan=2)

# if not initialize_serial_port():
#     pass

root.mainloop()
