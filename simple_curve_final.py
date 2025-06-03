from tkinter import *
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import numpy as np

window = Tk()

def correct_angle(angle):
    x = angle.split(",")
    return float(x[0]) + float(x[1]) / 60 + float(x[2]) / 3600

def correct_klm(klm):
    x = klm.split("+")
    return float(x[0])*1000 + float(x[1])
    
def get_values():
    intersection_angle = E1.get()
    radius = float(E2.get())
    klm_ints = E4.get()
    length = radius // 20

    intersection_angle = correct_angle(intersection_angle)
    klm_ints = correct_klm(klm_ints)

    azimuth = correct_angle(E10.get())

    # azimuth = 90 - intersection_angle / 2

    tangant_length = radius * math.tan(math.radians(intersection_angle / 2))
    curve_length = radius * math.radians(intersection_angle)

    delta = []

    kml_start = klm_ints - tangant_length
    kml_end = kml_start + curve_length    

    next_multiple = math.ceil(kml_start / length) * length

    data = []
    point_count = 1
    data.append((point_count, round(kml_start, 3), 0, 0, 0, 0))
    
    L1 = next_multiple - kml_start
    s1 = (L1 / (2*radius)) * (180 / math.pi)
    c1 = 2 * radius * math.sin(math.radians(s1))
    point_count += 1
    sum_s = s1
    delta.append(sum_s)
    data.append((point_count, round(next_multiple, 3), round(s1, 3), round(sum_s, 4), round(c1, 3), round(L1, 4)))
    
    c = curve_length - (next_multiple - kml_start)
    x = c // length
    for i in range(int(x)):
        if next_multiple > kml_end:
            break
        next_multiple += length
        s = (length / (2*radius)) * (180 / math.pi)
        c = 2 * radius * math.sin(math.radians(s))
        point_count += 1
        sum_s += s
        delta.append(sum_s)
        data.append((point_count, round(next_multiple, 3), round(s, 3), round(sum_s, 4), round(c, 3), length))

    L2 = kml_end - next_multiple
    s2 = (L2 / (2*radius)) * (180 / math.pi)
    c2 = 2 * radius * math.sin(math.radians(s2))
    sum_s += s2
    data.append((point_count + 1, round(kml_end, 3), round(s2, 3), round(sum_s, 4), round(c2, 3), round(L2, 4)))

    for row in tree.get_children():
        tree.delete(row)

    for row in data:
        tree.insert("", "end", values=row)

    def plot_curve(radius, intersection_angle, tangant_length, delta, azimuth):
        angle_rad = math.radians(intersection_angle)  
        
        x_start = 0
        y_start = 0
        x_end = 2 * radius * math.sin(angle_rad / 2) * math.sin(math.radians((intersection_angle / 2) + azimuth))
        y_end = 2 * radius * math.sin(angle_rad / 2) * math.cos(math.radians((intersection_angle / 2) + azimuth))

        x_int = tangant_length * math.sin(math.radians(azimuth))
        y_int = tangant_length * math.cos(math.radians(azimuth))
                
        impl_points = []
        for i in delta:
            l = 2 * radius * math.sin(math.radians(i))
            x_pt = x_start + (l * math.sin(math.radians((azimuth + i))))
            y_pt = y_start + (l * math.cos(math.radians((azimuth + i))))
            impl_points.append((x_pt, y_pt))
                
        plt.figure(figsize=(6, 6))
        
        plt.plot([x_start, x_int], [y_start, y_int], linestyle="--", color="red", label="Tangent Line 1")
        plt.plot([x_end, x_int], [y_end, y_int], linestyle="--", color="red", label="Tangent Line 2")
                
        plt.scatter([x_start, x_end, x_int], [y_start, y_end, y_int], color="black", zorder=3)
        plt.text(x_start, y_start, " Start", verticalalignment="bottom", horizontalalignment="right", fontsize=10)
        plt.text(x_end, y_end, " End", verticalalignment="bottom", horizontalalignment="left", fontsize=10)
        plt.text(x_int, y_int, " Intersection", verticalalignment="bottom", horizontalalignment="center", fontsize=10)
        
        for (x_pt, y_pt), ang in zip(impl_points, delta):
            plt.scatter(x_pt, y_pt, color="green", zorder=4)
            plt.text(x_pt, y_pt, f"angle:{round(ang, 2)}, len:{round(2*radius*math.sin(math.radians(ang)),2)}", 
                    fontsize=8, color="green", verticalalignment="bottom")
            plt.plot([x_start, x_pt], [y_start, y_pt], color="black", linestyle="--", linewidth=0.8)
        
        impl_points.append((x_end, y_end))
        x_vals, y_vals = zip(*impl_points)
        plt.plot(x_vals, y_vals, color='blue', linewidth=1.2, zorder=3, label='Impl. Curve')
        
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
        plt.xlabel("X (meters)")
        plt.ylabel("Y (meters)")
        plt.title("Curve with Tangents, Arc and Implementation Points")
        plt.legend()
        plt.grid()
        plt.axis("equal")
        plt.show()

    plot_curve(radius, intersection_angle, tangant_length, delta, azimuth)

window.title("Simple Curve")

window.configure(bg="#D3D3D3")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 580
window_height = 400
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
window.resizable(False, True)

L1 = Label(window, text="Intersection angle:", font=("Arial", 9, "bold"))
L1.grid(row=0, column=0, pady=10)
E1 = Entry(window)
E1.grid(row=0, column=1, pady=10, padx=20)
E1.insert(0, "41,48,0") 

L2 = Label(window, text="Radius of curve:", font=("Arial", 9, "bold"))
L2.grid(row=1, column=0, pady=10)
E2 = Entry(window)
E2.grid(row=1, column=1, pady=10)
E2.insert(0, 200) 

L10 = Label(window, text="azimuth:", font=("Arial", 9, "bold"))
L10.grid(row=2, column=0, pady=10)
E10 = Entry(window)
E10.grid(row=2, column=1, pady=10, padx=20)
E10.insert(0, "90,0,0") 

L4 = Label(window, text="Kilometraj of PI:", font=("Arial", 9, "bold"))
L4.grid(row=3, column=0, pady=10)
E4 = Entry(window)
E4.grid(row=3, column=1, pady=10)
E4.insert(0, "14+895.68") 

B1 = Button(window, text="Calculate", command=get_values, fg="white", bg="#2b2b2b", relief="raised", borderwidth=3, font=("Arial", 10, "bold"))
B1.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

tree = ttk.Treeview(window, columns=("pointNumber", "Kilometraj", "S Angle", "Stotal", "C Length", "arc"), show="headings")
tree.heading("arc", text="طول کمان دهنه")
tree.heading("pointNumber", text="شماره نقاط")
tree.heading("Stotal", text="زاویه انحراف کل")
tree.heading("S Angle", text="زاویه انحراف جز")
tree.heading("C Length", text="طول وتر")
tree.heading("Kilometraj", text="کیلومتراژ")

tree.column("pointNumber", width=70, anchor="center")
tree.column("Kilometraj", width=100, anchor="center")
tree.column("S Angle", width=100, anchor="center")
tree.column("Stotal", width=100, anchor="center")
tree.column("C Length", width=100, anchor="center")
tree.column("arc", width=100, anchor="center")

tree.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

window.mainloop()
