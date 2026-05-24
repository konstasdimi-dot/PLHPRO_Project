from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import all_functions

# ============================== FUNCTIONS ===============================

# ---- Adding an Activity ----

activities_db = []

def update_time_display():

    total_hours_used = sum(activity["hours"] for activity in activities_db)

    hours_left = 168.0 - total_hours_used

    free_time_label.config(text=f"Free Time for this week: {hours_left:.1f} hours")

def onn_add_clicked():
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
        category_combo.set("Choose here...")
        importance_combo.set("Choose here...")

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

# MAIN WINDOW ----------------------------------------------

root = Tk()
root.geometry("1000x800")
root.title("Time Management Application")
root.iconbitmap("icon_2.ico")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

root.rowconfigure(0, weight=1)


# ============================== LEFT FRAME ===============================

left_frame = LabelFrame(root, text="Inputs", padding=10)
left_frame.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

# ---- Row 0 ----

Label(left_frame, text="Activity Name:").grid(row=0, column=0, sticky=W, pady=5)
activity_name_entry = Entry(left_frame)
activity_name_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
activity_name_entry.insert(0, "Insert here...")


# ---- Row 1 ----

Label(left_frame, text="Category:").grid(row=1, column=0, sticky=W, pady=5)
category_combo = Combobox(left_frame, state="readonly", values=["Choose Here...","Obligation", "Free Time"])
category_combo.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
category_combo.set("Choose here...")

# ---- Row 2 ----

Label(left_frame, text="Weekly Hours:").grid(row=2, column=0, sticky=W, pady=5)
hours_entry = Entry(left_frame)
hours_entry.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
hours_entry.insert(0, "Insert here...")

# ---- Row 3 ----

Label(left_frame, text="Importance (1-10):").grid(row=3, column=0, sticky=W, pady=5)
importance_combo = Combobox(left_frame, state="readonly", values= ["Choose here...", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
importance_combo.grid(row=3, column=1, sticky=EW, padx=5, pady=5)
importance_combo.set("Choose here...")

# ---- Row 4 ----

Separator(left_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky= EW, pady=15, padx=5)

# ---- Row 5 ----

submit_button = Button(left_frame, text="Add Activity", command=onn_add_clicked)
submit_button.grid(row=5, sticky=NSEW, columnspan=2, pady=5, padx=5)

# ---- Row 6 ----

edit_button = Button(left_frame, text= "Edit Activity", command=edit_activity)
edit_button.grid(row=6, sticky=NSEW, columnspan=2, pady=5, padx=5)

# ---- Row 7 ----

delete_button = Button(left_frame, text="Delete Activity", command=delete_activity)
delete_button.grid(row=7, sticky=NSEW, columnspan=2, pady=5, padx=5)

# ---- Row 8 ----

Separator(left_frame, orient='horizontal').grid(row=8, column=0, columnspan=2, sticky= EW, pady=15, padx=5)

# ---- Row 9 ----

import_button = Button(left_frame, text="Import CSV")
import_button.grid(row=9, sticky=NSEW, columnspan=2, pady=5, padx=5)

# ---- Row 10 ----

export_button = Button(left_frame, text="Export CSV")
export_button.grid(row=10, sticky=NSEW, columnspan=2, pady=5, padx=5)

# ============================== RIGHT FRAME ===============================

right_frame = LabelFrame(root, text="Dashboard",padding=10)
right_frame.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)

free_time_label = Label(right_frame, text="Free Time for this week: 168 hours", font=("Arial", 14, "bold"))
free_time_label.pack(padx=5, pady=5)

tabs = Notebook(right_frame)
tabs.pack(fill="both", expand=True)

tab1_activities = Frame(tabs)
tab2_optimal_charts = Frame(tabs)
tab3_statistics = Frame(tabs)
tab4_graphics = Frame(tabs)

tabs.add(tab1_activities, text="All Activities")
tabs.add(tab2_optimal_charts, text="Optimal Scheduling")
tabs.add(tab3_statistics, text="Statistics")
tabs.add(tab4_graphics, text="Graphics")


# ---- All Activities Tab ----

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



# EXIT BUTTON --------------------------------------------

exit_button = Button(root, text="Exit Application", command=root.destroy)
exit_button.grid(row=1, column=1, sticky=E, columnspan=2, pady=5, padx=5)


# ROOT.MAINLOOP() -----------------------------------------

root.mainloop()
