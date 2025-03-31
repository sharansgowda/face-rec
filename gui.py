from tkinter import Toplevel, Label, Entry, Button, filedialog, Tk, OptionMenu, messagebox, Frame
import tkinter as tk
from tkinter.ttk import Treeview, Style
from PIL import ImageTk, Image
from pathlib import Path
from database import create_student, delete_student, get_name_from_usn, update_credentials, get_all_student, get_student, return_tk_image
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
        
        # Define color scheme
        self.PRIMARY_COLOR = "#4A6FDC"        # Main blue
        self.SECONDARY_COLOR = "#1B2845"      # Dark blue
        self.ACCENT_COLOR = "#FF6B6B"         # Accent red
        self.BG_COLOR = "#ECDFCC"             # Light background
        self.TEXT_COLOR = "#333333"           # Dark text
        self.HIGHLIGHT_COLOR = "#82C0CC"      # Highlight color
        
        # Define fonts
        self.TITLE_FONT = ("Helvetica", 42, "bold")
        self.HEADER_FONT = ("Helvetica", 24)
        self.BUTTON_FONT = ("Helvetica", 16)
        self.TEXT_FONT = ("Helvetica", 14)
        
        # Configure window
        self.window.configure(bg=self.BG_COLOR)
        
        # Create main frames
        self.header_frame = Frame(self.window, bg=self.SECONDARY_COLOR, height=100)
        self.header_frame.pack(fill='x')
        
        self.content_frame = Frame(self.window, bg=self.BG_COLOR)
        self.content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Create title
        self.project_title = Label(
            self.header_frame, 
            text="iDetect", 
            font=self.TITLE_FONT, 
            bg=self.SECONDARY_COLOR, 
            fg="white",
            pady=20
        )
        self.project_title.pack()
        
        # Create subtitle
        self.subtitle = Label(
            self.content_frame,
            text="Facial Recognition Attendance System",
            font=self.HEADER_FONT,
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            pady=10
        )
        self.subtitle.pack()
        
        # Create button frame
        self.button_frame = Frame(self.content_frame, bg=self.BG_COLOR)
        self.button_frame.pack(pady=30)
        
        # Create buttons
        button_configs = [
            ("Take Attendance", fr.run_recognition, "📸"),
            ("Register Student", self.register_student, "👤"),
            ("Update Student", self.update_student, "✏️"),
            ("View Student Detail", self.view_student_detail, "🔍"),
            ("Delete Student", self.delete_student, "🗑️"),
            ("View Database", self.view_database, "📊")
        ]
        
        for i, (text, command, icon) in enumerate(button_configs):
            button = self.create_styled_button(
                self.button_frame, 
                f"{icon} {text}", 
                command
            )
            row, col = divmod(i, 2)
            button.grid(row=row, column=col, padx=20, pady=15)
        
        # Create footer
        self.footer = Label(
            self.window,
            text="© 2025 iDetect - Facial Recognition Attendance System",
            font=("Helvetica", 10),
            bg=self.SECONDARY_COLOR,
            fg="white",
            pady=10
        )
        self.footer.pack(side="bottom", fill="x")
        
        self.window.mainloop()
    
    def create_styled_button(self, parent, text, command):
        """Create a styled button with hover effects"""
        button = Button(
            parent,
            text=text,
            font=self.BUTTON_FONT,
            command=command,
            cursor="hand2",
            bg=self.PRIMARY_COLOR,
            fg="black",
            width=25,
            height=2,
            relief="flat",
            borderwidth=0
        )
        
        # Add hover effects
        button.bind("<Enter>", lambda e, b=button: self.on_button_hover(b))
        button.bind("<Leave>", lambda e, b=button: self.on_button_leave(b))
        
        return button
    
    def on_button_hover(self, button):
        button.config(bg=self.HIGHLIGHT_COLOR)
    
    def on_button_leave(self, button):
        button.config(bg=self.PRIMARY_COLOR)
    
    def create_form_window(self, title):
        """Create a standardized form window"""
        form_window = Toplevel(self.window)
        form_window.title(title)
        form_window.configure(bg=self.BG_COLOR)
        form_window.geometry("800x600")
        
        # Add header
        header = Label(
            form_window,
            text=title,
            font=self.HEADER_FONT,
            bg=self.SECONDARY_COLOR,
            fg="white",
            pady=10
        )
        header.pack(fill="x")
        
        content_frame = Frame(form_window, bg=self.BG_COLOR, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        return form_window, content_frame
    
    def create_form_field(self, parent, row, label_text, entry_width=30, readonly=False):
        """Create a standardized form field with label and entry"""
        label = Label(
            parent, 
            text=label_text, 
            font=self.TEXT_FONT, 
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            anchor="e",
            width=15
        )
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        
        entry = Entry(
            parent,
            font=self.TEXT_FONT,
            width=entry_width,
            bd=2,
            relief="groove"
        )
        
        if readonly:
            entry.config(state='readonly', readonlybackground="#ECECEC")
            
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        
        return label, entry
    
    def create_form_button(self, parent, text, command, row, col, columnspan=2):
        """Create a standardized form button"""
        button = Button(
            parent,
            text=text,
            font=self.TEXT_FONT,
            command=command,
            cursor="hand2",
            bg=self.PRIMARY_COLOR,
            fg="white",
            width=15,
            relief="flat",
            borderwidth=0
        )
        
        button.grid(row=row, column=col, columnspan=columnspan, padx=10, pady=20)
        
        # Add hover effects
        button.bind("<Enter>", lambda e, b=button: self.on_button_hover(b))
        button.bind("<Leave>", lambda e, b=button: self.on_button_leave(b))
        
        return button

    def register_student(self):
        form_window, form_frame = self.create_form_window("Register Student")
        
        def select_image() -> Path:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )
            SCALE: float = 0.2
            if file_path:
                image = Image.open(file_path)
                _image = image.resize((int(image.width * SCALE), int(image.height * SCALE)), resample=Image.Resampling.LANCZOS)
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
            error_label.config(text="")

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
                form_window.destroy()
            except Exception as e:
                # Show error message if registration fails
                messagebox.showerror("Error", f"Failed to register student: {e}")

        # Create fields
        _, name_entry = self.create_form_field(form_frame, 0, "Name:")
        _, usn_entry = self.create_form_field(form_frame, 1, "USN:")
        _, course_entry = self.create_form_field(form_frame, 2, "Course:")
        _, year_join_entry = self.create_form_field(form_frame, 3, "Year of Joining:")
        _, section_entry = self.create_form_field(form_frame, 4, "Section:")
        
        # Gender dropdown
        gender_label = Label(form_frame, text="Gender:", font=self.TEXT_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor="e", width=15)
        gender_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        
        genders = ["Male", "Female", "Others"]
        gender_var = tk.StringVar()
        gender_var.set(genders[0])
        
        gender_option = OptionMenu(form_frame, gender_var, *genders)
        gender_option.config(font=self.TEXT_FONT, bg="white", width=10)
        gender_option.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # Image selection
        select_image_button = Button(
            form_frame, 
            text="Select Image", 
            command=select_image,
            font=self.TEXT_FONT,
            bg=self.SECONDARY_COLOR,
            fg="white",
            relief="flat"
        )
        select_image_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        # Image preview and file path
        image_preview_frame = Frame(form_frame, bg=self.BG_COLOR, bd=2, relief="groove", width=300, height=300)
        image_preview_frame.grid(row=0, column=2, rowspan=6, padx=20, pady=10)
        
        image_label = Label(image_preview_frame, bg=self.BG_COLOR)
        image_label.pack(padx=10, pady=10)
        
        file_path_label = Label(form_frame, text="", font=("Helvetica", 10), fg=self.TEXT_COLOR, bg=self.BG_COLOR, wraplength=300)
        file_path_label.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Error label
        error_label = Label(form_frame, text="", font=self.TEXT_FONT, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        error_label.grid(row=7, column=0, columnspan=3, sticky='ew', padx=10, pady=10)
        
        # Register button
        register_button = self.create_form_button(form_frame, "Register", validate_and_register, 8, 0, 3)

    def view_student_detail(self):
        form_window, form_frame = self.create_form_window("View Student Detail")
        
        def set_entry_text(e: tk.Entry, text: str):
            e.config(state='normal')
            e.delete(0, tk.END)
            e.insert(0, text)
            e.config(state='readonly')

        def clear_errors():
            error_label.config(text="")

        def search_student():
            clear_errors()
            usn = usn_entry.get()
            if not usn:
                error_label.config(text="USN not entered.")
                return

            try:
                usn = int(usn)
            except ValueError:
                error_label.config(text="Enter a valid USN.")
                return

            try:
                student = get_student(usn)
                if student:
                    set_entry_text(name_entry, student.name)
                    set_entry_text(course_entry, student.course)
                    set_entry_text(year_join_entry, str(student.year_join))
                    set_entry_text(section_entry, student.section)
                    set_entry_text(gender_entry, student.gender)
                    set_entry_text(attendance_entry, str(student.attendance))
                    
                    # show the image
                    try:
                        img = return_tk_image(usn, 0.3)
                        image_label.config(image=img)
                        image_label.image = img
                    except Exception as e:
                        print(f"Error loading image: {e}")
                else:
                    error_label.config(text="No student found with this USN.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve student details: {e}")

        # Search field
        usn_frame = Frame(form_frame, bg=self.BG_COLOR)
        usn_frame.pack(pady=10)
        
        usn_label = Label(usn_frame, text="Enter USN:", font=self.TEXT_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        usn_label.pack(side="left", padx=10)
        
        usn_entry = Entry(usn_frame, font=self.TEXT_FONT, width=10)
        usn_entry.pack(side="left", padx=10)
        usn_entry.focus()
        
        search_button = Button(
            usn_frame, 
            text="Search", 
            command=search_student,
            font=self.TEXT_FONT,
            bg=self.PRIMARY_COLOR,
            fg="white",
            relief="flat"
        )
        search_button.pack(side="left", padx=10)
        
        # Main content
        content_container = Frame(form_frame, bg=self.BG_COLOR)
        content_container.pack(fill="both", expand=True, pady=20)
        
        # Left frame for details
        details_frame = Frame(content_container, bg=self.BG_COLOR)
        details_frame.pack(side="left", padx=20, fill="y")
        
        # Create read-only fields
        _, name_entry = self.create_form_field(details_frame, 0, "Name:", readonly=True)
        _, course_entry = self.create_form_field(details_frame, 1, "Course:", readonly=True)
        _, year_join_entry = self.create_form_field(details_frame, 2, "Year of Joining:", readonly=True)
        _, section_entry = self.create_form_field(details_frame, 3, "Section:", readonly=True)
        _, gender_entry = self.create_form_field(details_frame, 4, "Gender:", readonly=True)
        _, attendance_entry = self.create_form_field(details_frame, 5, "Attendance:", readonly=True)
        
        # Right frame for image
        image_frame = Frame(content_container, bg=self.BG_COLOR, bd=2, relief="groove", width=300, height=300)
        image_frame.pack(side="right", padx=20, fill="both", expand=True)
        
        image_label = Label(image_frame, bg=self.BG_COLOR)
        image_label.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Error label
        error_label = Label(form_frame, text="", font=self.TEXT_FONT, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        error_label.pack(pady=10)

    def delete_student(self):
        form_window, form_frame = self.create_form_window("Delete Student")
        
        def delete():
            usn = usn_entry.get()
            if not usn:
                error_label.config(text="USN not entered.")
                return
                
            try:
                usn = int(usn)
            except ValueError:
                error_label.config(text="Enter a valid USN.")
                return
                
            try:
                student_name = get_name_from_usn(usn)
                if not student_name:
                    error_label.config(text="No student found with this USN.")
                    return
                    
                if messagebox.askokcancel("Warning", f"Are you sure you want to delete {student_name} with USN {usn}?"):
                    # Call the delete_student function
                    delete_student(usn)
                    # Show success message
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    # Close the delete window
                    form_window.destroy()
            except Exception as e:
                # Show error message if deletion fails
                messagebox.showerror("Error", f"Failed to delete student: {e}")

        # Create warning frame
        warning_frame = Frame(form_frame, bg=self.ACCENT_COLOR, bd=2, relief="groove")
        warning_frame.pack(fill="x", padx=20, pady=20)
        
        warning_label = Label(
            warning_frame,
            text="⚠️ Warning: This action cannot be undone.",
            font=self.TEXT_FONT,
            bg=self.ACCENT_COLOR,
            fg="white",
            pady=10
        )
        warning_label.pack()
        
        # USN frame
        usn_frame = Frame(form_frame, bg=self.BG_COLOR)
        usn_frame.pack(pady=30)
        
        usn_label = Label(usn_frame, text="Enter USN to delete:", font=self.TEXT_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        usn_label.pack(side="top", pady=10)
        
        usn_entry = Entry(usn_frame, font=self.TEXT_FONT, width=15, justify="center")
        usn_entry.pack(side="top", pady=10)
        usn_entry.focus()
        
        # Error label
        error_label = Label(form_frame, text="", font=self.TEXT_FONT, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        error_label.pack(pady=10)
        
        # Delete button
        delete_button = Button(
            form_frame,
            text="Delete Student",
            command=delete,
            font=self.TEXT_FONT,
            bg=self.ACCENT_COLOR,
            fg="white",
            width=15,
            relief="flat",
            borderwidth=0
        )
        delete_button.pack(pady=20)

    def update_student(self):
        form_window, form_frame = self.create_form_window("Update Student")
        
        def clear_errors():
            error_label.config(text="")
            
        def load_student():
            clear_errors()
            usn = usn_entry.get()
            if not usn:
                error_label.config(text="USN not entered.")
                return

            try:
                usn = int(usn)
            except ValueError:
                error_label.config(text="Enter a valid USN.")
                return

            try:
                student = get_student(usn)
                if student:
                    # Pre-fill the fields with current data
                    name_entry.delete(0, tk.END)
                    name_entry.insert(0, student.name)
                    
                    course_entry.delete(0, tk.END)
                    course_entry.insert(0, student.course)
                    
                    year_join_entry.delete(0, tk.END)
                    year_join_entry.insert(0, str(student.year_join))
                    
                    section_entry.delete(0, tk.END)
                    section_entry.insert(0, student.section)
                    
                    gender_var.set(student.gender)
                    
                    # Show student image
                    try:
                        img = return_tk_image(usn, 0.3)
                        image_label.config(image=img)
                        image_label.image = img
                    except Exception as e:
                        print(f"Error loading image: {e}")
                        
                    # Enable update button
                    update_button.config(state="normal")
                else:
                    error_label.config(text="No student found with this USN.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve student details: {e}")

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
                form_window.destroy()
            except Exception as e:
                # Show error message if update fails
                messagebox.showerror("Error", f"Failed to update student details: {e}")

        # Search frame
        search_frame = Frame(form_frame, bg=self.BG_COLOR)
        search_frame.pack(pady=10)
        
        usn_label = Label(search_frame, text="Enter USN:", font=self.TEXT_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        usn_label.pack(side="left", padx=10)
        
        usn_entry = Entry(search_frame, font=self.TEXT_FONT, width=10)
        usn_entry.pack(side="left", padx=10)
        usn_entry.focus()
        
        load_button = Button(
            search_frame, 
            text="Load Student", 
            command=load_student,
            font=self.TEXT_FONT,
            bg=self.PRIMARY_COLOR,
            fg="white",
            relief="flat"
        )
        load_button.pack(side="left", padx=10)
        
        # Main content
        content_container = Frame(form_frame, bg=self.BG_COLOR)
        content_container.pack(fill="both", expand=True, pady=20)
        
        # Left frame for details
        details_frame = Frame(content_container, bg=self.BG_COLOR)
        details_frame.pack(side="left", padx=20, fill="y")
        
        # Create editable fields
        _, name_entry = self.create_form_field(details_frame, 0, "Name:")
        _, course_entry = self.create_form_field(details_frame, 1, "Course:")
        _, year_join_entry = self.create_form_field(details_frame, 2, "Year of Joining:")
        _, section_entry = self.create_form_field(details_frame, 3, "Section:")
        
        # Gender dropdown
        gender_label = Label(details_frame, text="Gender:", font=self.TEXT_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR, anchor="e", width=15)
        gender_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        
        genders = ["Male", "Female", "Others"]
        gender_var = tk.StringVar()
        gender_var.set(genders[0])
        
        gender_option = OptionMenu(details_frame, gender_var, *genders)
        gender_option.config(font=self.TEXT_FONT, bg="white", width=10)
        gender_option.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Right frame for image
        image_frame = Frame(content_container, bg=self.BG_COLOR, bd=2, relief="groove", width=300, height=300)
        image_frame.pack(side="right", padx=20, fill="both", expand=True)
        
        image_label = Label(image_frame, bg=self.BG_COLOR)
        image_label.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Error label
        error_label = Label(form_frame, text="", font=self.TEXT_FONT, fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        error_label.pack(pady=10)
        
        # Update button
        update_button = Button(
            form_frame,
            text="Update Student",
            command=update,
            font=self.TEXT_FONT,
            bg=self.PRIMARY_COLOR,
            fg="white",
            width=15,
            relief="flat",
            borderwidth=0,
            state="disabled"  # Initially disabled until student is loaded
        )
        update_button.pack(pady=20)

    def view_database(self):
        view_window, content_frame = self.create_form_window("Student Database")
        view_window.geometry("1200x700")  # Make this window larger
        
        def show_students():
            try:
                students = get_all_student()
                if students:
                    # Clear the treeview
                    for item in tree.get_children():
                        tree.delete(item)
                        
                    # Add data to treeview
                    for student in students:
                        tree.insert("", "end", values=(
                            student.usn,
                            student.name,
                            student.course,
                            student.year_join,
                            student.section,
                            student.gender,
                            student.attendance,
                            student.last_attendance_time
                        ))
                else:
                    messagebox.showinfo("Info", "No student records found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch database: {e}")
        
        # Create a frame for the treeview
        tree_frame = Frame(content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create the treeview
        columns = ("USN", "Name", "Course", "Year", "Section", "Gender", "Attendance", "Last Attendance")
        tree = Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            # Set column widths
            if col in ["USN", "Year", "Section"]:
                tree.column(col, width=80, anchor="center")
            elif col in ["Gender", "Attendance"]:
                tree.column(col, width=100, anchor="center")
            elif col == "Last Attendance":
                tree.column(col, width=200, anchor="center")
            else:
                tree.column(col, width=150, anchor="w")
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        # Add horizontal scrollbar
        h_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Create button frame
        button_frame = Frame(content_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=10)
        
        # Create buttons
        refresh_button = Button(
            button_frame,
            text="Refresh Data",
            command=show_students,
            font=self.TEXT_FONT,
            bg=self.PRIMARY_COLOR,
            fg="white",
            relief="flat",
            padx=20
        )
        refresh_button.pack(side="left", padx=10)
        
        close_button = Button(
            button_frame,
            text="Close",
            command=view_window.destroy,
            font=self.TEXT_FONT,
            bg=self.SECONDARY_COLOR,
            fg="white",
            relief="flat",
            padx=20
        )
        close_button.pack(side="left", padx=10)
        
        # Load data initially
        show_students()


if __name__ == "__main__":
    WebcamApp(Tk(), "iDetect")