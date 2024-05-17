from tkinter import Toplevel, Label, Entry, Button, filedialog, Tk, OptionMenu, messagebox
import tkinter as tk
from tkinter.ttk import Treeview
from PIL import ImageTk, Image
from pathlib import Path
from database import create_student, delete_student, get_name_from_usn, update_credentials, get_all_student
from faceRecUtils import FaceRecognition
from time import sleep
from prettytable import PrettyTable

fr = FaceRecognition()


class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.geometry('1600x900')
        self.window.bind('<Escape>', lambda x: window.quit())
        self.window.title(window_title)

        DEFAULT_BG = "#FFFAE6"
        DEFAULT_FG = "#240750"
        DEF_BUTTON_WIDTH = 30
        self.defaultFont = ("Source Code Pro", 18)

        self.project_title = Label(self.window, text="iDetect", justify='center', font=('Source Code Pro', 40), relief="ridge", bg=DEFAULT_BG, fg=DEFAULT_FG)
        self.project_title.pack(fill='both')

        self.button = Button(self.window, text="Take Attendance", font=self.defaultFont, command=fr.run_recognition, cursor="hand",
                             underline=True, fg=DEFAULT_FG, bg=DEFAULT_BG, width=DEF_BUTTON_WIDTH)
        self.button.pack(padx=20, pady=20)

        self.register_student_button = Button(self.window, text="Register Student", font=self.defaultFont, command=self.register_student, cursor="hand", fg=DEFAULT_FG, bg=DEFAULT_BG, width=DEF_BUTTON_WIDTH)
        self.register_student_button.pack()

        self.update_student_button = Button(self.window, text="Update Student", font=self.defaultFont, command=self.update_student, cursor="hand", fg=DEFAULT_FG, bg=DEFAULT_BG, width=DEF_BUTTON_WIDTH)
        self.update_student_button.pack()

        self.delete_student_button = Button(self.window, text="Delete Student", font=self.defaultFont, command=self.delete_student, cursor="hand", fg=DEFAULT_FG, bg=DEFAULT_BG, width=DEF_BUTTON_WIDTH)
        self.delete_student_button.pack()

        self.view_database_button = Button(self.window, text="View Database", font=self.defaultFont, command=self.view_database, cursor="hand", fg=DEFAULT_FG, bg=DEFAULT_BG, width=DEF_BUTTON_WIDTH)
        self.view_database_button.pack()

        # self.buzzer_button = tk.Button(self.window, text="SHAMPAL", font=self.defaultFont, command=self.play_buzzer, cursor="hand")
        # self.buzzer_button.pack(anchor=tk.CENTER, fill=tk.BOTH, side=tk.BOTTOM)

        self.window.mainloop()

    # def play_buzzer(self):
    #     self.board.digital[13].write(1)
    #     sleep(1)
    #     self.board.digital[13].write(0)

    def register_student(self):
        register_window = Toplevel(self.window)
        register_window.title("Register Student")

        def select_image() -> Path:
            file_path = filedialog.askopenfilename()
            SCALE: float = 0.2
            if file_path:
                image = Image.open(file_path)
                _image = image.resize((int(image.height * SCALE), int(image.width * SCALE)), resample=Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(_image)
                image_label.config(image=photo)
                image_label.image = photo               # Keep reference to prevent garbage collection
                file_path_label.config(text=file_path)

        def validate_and_register():
            name = name_entry.get()
            usn = usn_entry.get()
            course = course_entry.get()
            year_join = year_join_entry.get()
            section = section_entry.get()
            gender = gender_var.get()

            # Clear previous error messages
            clear_errors()

            # Validate fields
            if not name:
                error_label.config(text="Name is required")
                return
            if not usn:
                error_label.config(text="USN is required")
                return
            if not course:
                error_label.config(text="Course is required")
                return
            if not year_join:
                error_label.config(text="Year of Joining is required")
                return
            if not section:
                error_label.config(text="Section is required")
                return
            if not gender:
                error_label.config(text="Gender is required")
                return

            # Convert year_join to int
            try:
                year_join = int(year_join)
            except ValueError:
                error_label.config(text="Invalid input for Year of Joining")
                return

            # Convert usn to int
            try:
                usn = int(usn)
            except ValueError:
                error_label.config(text="Invalid input for USN")
                return

            file_path = file_path_label.cget("text")

            try:
                if not file_path:
                    error_label.config(text="Please select an image")
                    return
                # Register the student
                create_student(usn, name, course, year_join, section, gender, file_path)
                # Show success message
                messagebox.showinfo("Success", "Student registered successfully!")
                # Close the register window
                register_window.destroy()
            except Exception as e:
                # Show error message if registration fails
                messagebox.showerror("Error", f"Failed to register student: {e}")

        def clear_errors():
            error_label.config(text="")

        name_label = Label(register_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry = Entry(register_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        usn_label = Label(register_window, text="USN:")
        usn_label.grid(row=1, column=0, padx=10, pady=10)
        usn_entry = Entry(register_window)
        usn_entry.grid(row=1, column=1, padx=10, pady=10)

        course_label = Label(register_window, text="Course:")
        course_label.grid(row=2, column=0, padx=10, pady=10)
        course_entry = Entry(register_window)
        course_entry.grid(row=2, column=1, padx=10, pady=10)

        year_join_label = Label(register_window, text="Year of Joining:")
        year_join_label.grid(row=3, column=0, padx=10, pady=10)
        year_join_entry = Entry(register_window)
        year_join_entry.grid(row=3, column=1, padx=10, pady=10)

        section_label = Label(register_window, text="Section:")
        section_label.grid(row=4, column=0, padx=10, pady=10)
        section_entry = Entry(register_window)
        section_entry.grid(row=4, column=1, padx=10, pady=10)

        gender_label = Label(register_window, text="Gender:")
        gender_label.grid(row=5, column=0, padx=10, pady=10)
        genders = ["Male", "Female", "Others"]
        gender_var = tk.StringVar()
        gender_var.set(genders[0])
        gender_option = OptionMenu(register_window, gender_var, *genders)
        gender_option.grid(row=5, column=1, padx=10, pady=10)

        select_image_button = Button(register_window, text="Select Image", command=select_image)
        select_image_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        image_label = Label(register_window)
        image_label.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        # After creating the image_label
        file_path_label = Label(register_window, text="", font=("Source Code Pro", 12), fg="beige")
        file_path_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        error_label = Label(register_window, text="", font=("Source Code Pro", 14), fg="red")
        error_label.grid(row=9, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        register_button = Button(register_window, text="Register", command=validate_and_register)
        register_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def delete_student(self):
        delete_window = Toplevel(self.window)
        delete_window.title("Delete Student")

        def delete():
            usn = usn_entry.get()
            if messagebox.askokcancel("Warning", f"Are you sure you want to delete {get_name_from_usn(usn)} with USN {usn}?"):
                try:
                    # Call the delete_student function
                    delete_student(usn)
                    # Show success message
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    # Close the delete window
                    delete_window.destroy()
                except Exception as e:
                    # Show error message if deletion fails
                    messagebox.showerror("Error", f"Failed to delete student: {e}")

        usn_label = Label(delete_window, text="Enter USN to delete:")
        usn_label.grid(row=0, column=0, padx=10, pady=10)
        usn_entry = Entry(delete_window)
        usn_entry.grid(row=0, column=1, padx=10, pady=10)

        delete_button = Button(delete_window, text="Delete", command=delete)
        delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def update_student(self):
        update_window = Toplevel(self.window)
        update_window.title("Update Student")

        def update():
            # Get the USN of the student to be updated
            usn = usn_entry.get()
            updates = {}

            # Get the details of the student to be updated
            if name_entry.get():
                updates['name'] = name_entry.get()
            if course_entry.get():
                updates['course'] = course_entry.get()
            if year_join_entry.get():
                updates['year_join'] = year_join_entry.get()
            if section_entry.get():
                updates['section'] = section_entry.get()
            if gender_var.get():
                updates['gender'] = gender_var.get()

            try:
                # Call the update_credentials function
                update_credentials(usn, **updates)
                # Show success message
                messagebox.showinfo("Success", "Student details updated successfully!")
                # Close the update window
                update_window.destroy()
            except Exception as e:
                # Show error message if update fails
                messagebox.showerror("Error", f"Failed to update student details: {e}")

        usn_label = Label(update_window, text="Enter USN to update:")
        usn_label.grid(row=0, column=0, padx=10, pady=10)
        usn_entry = Entry(update_window)
        usn_entry.grid(row=0, column=1, padx=10, pady=10)

        name_label = Label(update_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = Entry(update_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        course_label = Label(update_window, text="Course:")
        course_label.grid(row=2, column=0, padx=10, pady=10)
        course_entry = Entry(update_window)
        course_entry.grid(row=2, column=1, padx=10, pady=10)

        year_join_label = Label(update_window, text="Year of Joining:")
        year_join_label.grid(row=3, column=0, padx=10, pady=10)
        year_join_entry = Entry(update_window)
        year_join_entry.grid(row=3, column=1, padx=10, pady=10)

        section_label = Label(update_window, text="Section:")
        section_label.grid(row=4, column=0, padx=10, pady=10)
        section_entry = Entry(update_window)
        section_entry.grid(row=4, column=1, padx=10, pady=10)

        gender_label = Label(update_window, text="Gender:")
        gender_label.grid(row=5, column=0, padx=10, pady=10)
        genders = ["Male", "Female", "Others"]
        gender_var = tk.StringVar()
        gender_option = OptionMenu(update_window, gender_var, *genders)
        gender_option.grid(row=5, column=1, padx=10, pady=10)

        update_button = Button(update_window, text="Update", command=update)
        update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def view_database(self):
        view_window = Toplevel(self.window)
        view_window.title("View Database")

        # def show_students():
        #     try:
        #         students = get_all_student()
        #         if students:
        #             text = ""
        #             for student in students:
        #                 text += f"USN: {student.usn:03d}, Name: {student.name}, Course: {student.course}, Year of Joining: {student.year_join}, Section: {student.section}, Gender: {student.gender}\n"
        #             database_text.config(state="normal")
        #             database_text.delete("1.0", "end")
        #             database_text.insert("1.0", text)
        #             database_text.config(state="disabled")
        #         else:
        #             database_text.config(state="normal")
        #             database_text.delete("1.0", "end")
        #             database_text.insert("1.0", "No data found")
        #             database_text.config(state="disabled")
        #     except Exception as e:
        #         messagebox.showerror("Error", f"Failed to fetch database: {e}")

        def show_students():
            try:
                students = get_all_student()
                if students:
                    table = PrettyTable()
                    table.field_names = ["USN", "Name", "Course", "Year of Joining", "Section", "Gender", "Attendance", "Last attendance time"]
                    for student in students:
                        table.add_row([student.usn, student.name, student.course, student.year_join, student.section, student.gender, student.attendance, student.last_attendance_time])
                    text = table.get_string()
                    database_text.config(state="normal")
                    database_text.delete("1.0", "end")
                    database_text.insert("1.0", text)
                    database_text.config(state="disabled")
                else:
                    database_text.config(state="normal")
                    database_text.delete("1.0", "end")
                    database_text.insert("1.0", "No data found")
                    database_text.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch database: {e}")

        database_text = tk.Text(view_window, wrap="word", height=20, width=140, font=('Source Code Pro', 16))
        database_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        database_text.config(state="normal")

        refresh_button = Button(view_window, text="Refresh", command=show_students)
        refresh_button.grid(row=1, column=0, padx=10, pady=10)

        close_button = Button(view_window, text="Close", command=view_window.destroy)
        close_button.grid(row=1, column=1, padx=10, pady=10)


if __name__ == "__main__":
    WebcamApp(Tk(), "iDetect")
