from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import all_functions

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============================== FUNCTIONS ===============================

activities_db = []

# ==== CHARTS & TIME MANAGEMENT FUNCTIONS ====

# Graphic ----------

def update_pie_chart():
    for widget in tab4_graphics.winfo_children():
        widget.destroy()

    if not activities_db:
        Label(tab4_graphics, text="Add activities in order to view your schedule breakdown!")
        return

    labels = [activity["name"] for activity in activities_db]
    sizes = [activity["hours"] for activity in activities_db]

    total_hours = sum(sizes)
    leftover = 168.0 - total_hours

    if leftover > 0:
        labels.append("Unallocated Time")
        sizes.append(leftover)

    fig = Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(sizes,labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Weekly Hours Breakdown", fontsize=14, fontweight="bold")

    canvas = FigureCanvasTkAgg(fig, master=tab4_graphics)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Weekly Optimizer ----------

def update_optimal_view():
    feasible_listbox.delete(0,END)
    rejected_listbox.delete(0,END)

    try:
        total_time = float(total_time_entry.get().strip())
    except ValueError:
        total_time = 168.0

    feasible, rejected = all_functions.calculate_optimal_schedule(activities_db, total_time)

    for item in feasible:
        feasible_listbox.insert(END, f"[{item['name']} | {item['category']} | {item['hours']} hrs | Priority: {item['importance']}]")

    for item in rejected:
        rejected_listbox.insert(END, f"[{item['name']} | {item['category']} | {item['hours']} hrs | Priority: {item['importance']}]")

# ==== GUI FUNCTIONS ====

# ---- Available Weekly Hours ----

def update_time_display():

    total_hours_used = sum(activity["hours"] for activity in activities_db)

    try:
        total_available = float(total_time_entry.get().strip())
    except ValueError:
        total_available = 168.0

    hours_left = total_available - total_hours_used
    free_time_label.config(text=f"Free Time for this week: {hours_left:.1f} hours")

    update_pie_chart()
    update_optimal_view()

# ---- Adding an Activity ----

def on_add_clicked():
    raw_name = activity_name_entry.get().strip()
    raw_category = category_combo.get()
    raw_hours = hours_entry.get().strip()
    raw_importance = importance_combo.get()

    success, result = all_functions.validate_activity_data(raw_name, raw_category, raw_hours, raw_importance)

    if success == False:
        messagebox.showerror("Error!", result)
    else:
        activities_db.append(result)
        row_data = (result["name"], result["category"], result["hours"], result["importance"])
        db_table.insert(parent="", index="end", values=row_data)

        activity_name_entry.delete(0, "end")
        hours_entry.delete(0, "end")
        category_combo.set("Obligation")
        importance_combo.set("5")

        update_time_display()

# ---- Editing an Activity ----

def edit_activity():
    selected_item = db_table.selection()

    if not selected_item:
        messagebox.showwarning("Selection Error!", "Please select an activity to edit!")
        return

    item_id = selected_item[0]
    item_index = db_table.index(item_id)
    current_values = db_table.item(item_id, "values")

    edit_window = Toplevel(root)
    edit_window.title("Edit Activity")
    edit_window.geometry("350x250")
    edit_window.grab_set()

    Label(edit_window, text="Activity Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    edit_name = Entry(edit_window)
    edit_name.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
    edit_name.insert(0, current_values[0])

    Label(edit_window, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    edit_category = Combobox(edit_window, values=["Obligation", "Free Time"], state="readonly")
    edit_category.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    edit_category.set(current_values[1])

    Label(edit_window, text="Weekly Hours:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    edit_hours = Entry(edit_window)
    edit_hours.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    edit_hours.insert(0, current_values[2])

    Label(edit_window, text="Importance:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    edit_importance = Combobox(edit_window, values=list(range(1, 11)), state="readonly")
    edit_importance.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    edit_importance.set(current_values[3])

    def save_edits():
        raw_name = edit_name.get().strip()
        raw_category = edit_category.get()
        raw_hours = edit_hours.get().strip()
        raw_importance = edit_importance.get()

        success, result = all_functions.validate_activity_data(raw_name,raw_category,raw_hours,raw_importance)

        if success == False:
            messagebox.showerror("Error!", result, parent=edit_window)
        else:
            activities_db[item_index] = result
            db_table.item(item_id, values=(result["name"], result["category"], result["hours"], result["importance"]))
            edit_window.destroy()

            update_time_display()

    Button(edit_window, text= "Save Changes" , command=save_edits).grid(row=4, column=0, columnspan=2, pady=15)

# ---- Deleting an Activity ----

def delete_activity():
    selected_item = db_table.selection()

    if not selected_item:
        messagebox.showwarning("Selection Error!", "Please select an activity to delete!")
        return

    item_id = selected_item[0]
    item_index = db_table.index(item_id)

    activity_name = db_table.item(item_id, "values")[0]

    confirm = messagebox.askyesno("Deletion Confirmation", f"Are you sure you want to delete '{activity_name}'?")

    if confirm:
        del activities_db[item_index]

        db_table.delete(item_id)

        update_time_display()

# MAIN WINDOW ==========

root = Tk()
root.geometry("1000x800")
root.title("Time Management Application")
root.iconbitmap("icon_2.ico")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

root.rowconfigure(0, weight=1)

# LEFT FRAME ==========

left_frame = LabelFrame(root, text="Inputs", padding=10)
left_frame.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

# Row 0 ----------

Label(left_frame, text="Total Available Hours:").grid(row=0, column=0, sticky=W, pady=5)
total_time_entry = Entry(left_frame)
total_time_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
total_time_entry.insert(0, "168.0")

# Row 1 ----------

Separator(left_frame, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky= EW, pady=15, padx=5)

# Row 2 ----------

Label(left_frame, text="Activity Name:").grid(row=2, column=0, sticky=W, pady=5)
activity_name_entry = Entry(left_frame)
activity_name_entry.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
activity_name_entry.insert(0, "")

# Row 3 ----------

Label(left_frame, text="Category:").grid(row=3, column=0, sticky=W, pady=5)
category_combo = Combobox(left_frame, state="readonly", values=["Choose Here...","Obligation", "Free Time"])
category_combo.grid(row=3, column=1, sticky=EW, padx=5, pady=5)
category_combo.set("Obligation")

# Row 4 ----------

Label(left_frame, text="Weekly Hours:").grid(row=4, column=0, sticky=W, pady=5)
hours_entry = Entry(left_frame)
hours_entry.grid(row=4, column=1, sticky=EW, padx=5, pady=5)
hours_entry.insert(0, "")

# Row 5 ----------

Label(left_frame, text="Importance (1-10):").grid(row=5, column=0, sticky=W, pady=5)
importance_combo = Combobox(left_frame, state="readonly", values= ["Choose here...", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
importance_combo.grid(row=5, column=1, sticky=EW, padx=5, pady=5)
importance_combo.set("5")

# Row 6 ----------

Separator(left_frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky= EW, pady=15, padx=5)

# Row 7 ----------

submit_button = Button(left_frame, text="Add Activity", command=on_add_clicked)
submit_button.grid(row=7, sticky=NSEW, columnspan=2, pady=5, padx=5)

# Row 8 ----------

edit_button = Button(left_frame, text= "Edit Activity", command=edit_activity)
edit_button.grid(row=8, sticky=NSEW, columnspan=2, pady=5, padx=5)

# Row 9 ----------

delete_button = Button(left_frame, text="Delete Activity", command=delete_activity)
delete_button.grid(row=9, sticky=NSEW, columnspan=2, pady=5, padx=5)

# Row 10 ----------

Separator(left_frame, orient='horizontal').grid(row=10, column=0, columnspan=2, sticky= EW, pady=15, padx=5)

# Row 11 ----------

import_button = Button(left_frame, text="Import CSV")
import_button.grid(row=11, sticky=NSEW, columnspan=2, pady=5, padx=5)

# Row 12 ----------

export_button = Button(left_frame, text="Export CSV")
export_button.grid(row=12, sticky=NSEW, columnspan=2, pady=5, padx=5)

# RIGHT FRAME ==========

right_frame = LabelFrame(root, text="Dashboard",padding=10)
right_frame.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)

free_time_label = Label(right_frame, text="Free Time for this week: 168 hours", font=("Arial", 14, "bold"))
free_time_label.pack(padx=5, pady=5)

tabs = Notebook(right_frame)
tabs.pack(fill="both", expand=True)

tab1_activities = Frame(tabs)
tab2_optimal_scheduling = Frame(tabs)
tab3_statistics = Frame(tabs)
tab4_graphics = Frame(tabs)

tabs.add(tab1_activities, text="All Activities")
tabs.add(tab2_optimal_scheduling, text="Optimal Scheduling")
tabs.add(tab3_statistics, text="Statistics")
tabs.add(tab4_graphics, text="Graphics")

# All Activities Tab --------

activities_tab_columns = ("name", "category", "hours", "importance")

db_table = Treeview(tab1_activities, columns=activities_tab_columns, show="headings")
db_table.pack(fill="both", expand=True, padx=10, pady=5)

db_table.heading("name", text="Name")
db_table.heading("category", text="Category")
db_table.heading("hours", text="Hours Spent (Hrs)")
db_table.heading("importance", text="Importance (1-10)")

db_table.column("name", width=150, anchor="center")
db_table.column("category", width=100, anchor="center")
db_table.column("hours", width=100, anchor="center")
db_table.column("importance", width=100, anchor="center")

# Optimal Scheduling Tab ----------

tab2_controls = Frame(tab2_optimal_scheduling)
tab2_controls.pack(fill="x", padx=10, pady=(10,0))

Button(tab2_controls, text="Recalculate Schedule", command=update_time_display).pack(side="left")

Label(tab2_optimal_scheduling, text="Feasible Activities (Sorted by Importance)", font=("Arial", 11, "bold"), foreground="green").pack(anchor="w", padx=10, pady=(15,0))
feasible_listbox = Listbox(tab2_optimal_scheduling, font=("Arial", 10), height=10)
feasible_listbox.pack(fill="both", expand=True, padx=10, pady=5)

Label(tab2_optimal_scheduling, text="Rejected Activities (Not Enough Time)", font=("Arial", 11, "bold"), foreground="red").pack(anchor="w", padx=10, pady=(10,0))
rejected_listbox = Listbox(tab2_optimal_scheduling, font=("Arial", 10), height=5)
rejected_listbox.pack(fill="both", expand=True, padx=10, pady=5)

# EXIT BUTTON ==========

exit_button = Button(root, text="Exit Application", command=root.destroy)
exit_button.grid(row=1, column=1, sticky=E, columnspan=2, pady=5, padx=5)

# ROOT.MAINLOOP() ==========
update_pie_chart()
update_optimal_view()

root.mainloop()