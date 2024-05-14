from tkinter import Toplevel, Label, Entry, Button, filedialog, Tk, OptionMenu, messagebox
import tkinter as tk
from PIL import ImageTk, Image
from pathlib import Path
from database import create_student
from faceRecUtils import FaceRecognition

fr = FaceRecognition()

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.geometry('1600x900')
        self.window.bind('<Escape>', lambda x: window.quit())
        self.window.title(window_title)

        DEFAULT_BG = "#FFFAE6"
        DEFAULT_FG = "#240750"
        self.defaultFont = ("Source Code Pro", 18)

        self.project_title = Label(self.window, text="iDetect", justify='center', font=('Source Code Pro', 40), relief="ridge", bg=DEFAULT_BG, fg=DEFAULT_FG, width=20)
        self.project_title.pack(fill='both')

        self.label = Label(self.window, text="Take Attendance", font=self.defaultFont, bd=4, underline=True)
        self.label.pack()
        
        self.button = Button(self.window, text="Enable Video Feed", font=self.defaultFont, command=fr.run_recognition, cursor="hand",
                                underline=True, fg=DEFAULT_FG, bg=DEFAULT_BG)
        self.button.pack(padx=20, pady=20)
        
        self.register_student_button = Button(self.window, text="Register Student", font=self.defaultFont, command=self.register_student, cursor="hand"
                                                ,fg=DEFAULT_FG, bg=DEFAULT_BG)
        self.register_student_button.pack()

        self.delete_student_button = Button(self.window, text="Delete Student", font=self.defaultFont, command=self.delete_student, cursor="hand"
                                                ,fg=DEFAULT_FG, bg=DEFAULT_BG)
        self.delete_student_button.pack()

        self.view_database_button = Button(self.window, text="View Database", font=self.defaultFont, command=self.view_database, cursor="hand"
                                        ,fg=DEFAULT_FG, bg=DEFAULT_BG)
        self.view_database_button.pack()
        
        self.window.mainloop()

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
        # Implement the functionality to delete a student here
        pass

    def view_database(self):
        # Implement the functionality to view the database here
        pass

    def run_recognition(self):
        # Implement the functionality to run face recognition here
        pass

if __name__ == "__main__":
    WebcamApp(Tk(), "iDetect")
