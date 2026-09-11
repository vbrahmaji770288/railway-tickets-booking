import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import webbrowser


# ============================================================
# BERTH CLASS
# ============================================================

class Berth:
    """
    Stores berth/seat information.
    """

    BERTH_TYPES = [
        "Lower Berth",
        "Middle Berth",
        "Upper Berth",
        "Side Lower Berth",
        "Side Upper Berth"
    ]

    @staticmethod
    def get_berth_type(seat_number, travel_class):
        """
        Assign berth type based on seat number.

        GEN has no berth allocation.

        1AC and 2AC:
        Middle berth is not used.

        3AC and SL:
        Lower -> Middle -> Upper -> Side Lower -> Side Upper
        """

        if travel_class == "GEN":
            return "No Berth"

        # 1AC and 2AC do not use Middle Berth
        if travel_class in ["1AC", "2AC"]:
            berth_cycle = [
                "Lower Berth",
                "Upper Berth",
                "Side Lower Berth",
                "Side Upper Berth"
            ]

        else:
            berth_cycle = [
                "Lower Berth",
                "Middle Berth",
                "Upper Berth",
                "Side Lower Berth",
                "Side Upper Berth"
            ]

        return berth_cycle[(seat_number - 1) % len(berth_cycle)]


# ============================================================
# TRAIN CLASS
# ============================================================

class Train:
    """
    Stores train details, seats and fares.
    """

    def __init__(self, number, name, source, destination,
                 seat_counts, fares):

        self.number = number
        self.name = name
        self.source = source
        self.destination = destination

        # Example:
        # {"1AC": 10, "2AC": 20, ...}
        self.seat_counts = seat_counts.copy()

        # Fare for each class
        self.fares = fares.copy()

        # Number of confirmed seats already booked
        self.booked_seats = {
            travel_class: 0
            for travel_class in seat_counts
        }

        # RAC quota
        self.rac_quota = {
            travel_class: 5
            for travel_class in seat_counts
        }

        # Number of RAC tickets booked
        self.rac_booked = {
            travel_class: 0
            for travel_class in seat_counts
        }

        # Waiting list count
        self.waiting_list = {
            travel_class: 0
            for travel_class in seat_counts
        }

    def available_seats(self, travel_class):
        """
        Return remaining confirmed seats.
        """

        return (
            self.seat_counts[travel_class]
            - self.booked_seats[travel_class]
        )

    def available_rac(self, travel_class):
        """
        Return remaining RAC quota.
        """

        return (
            self.rac_quota[travel_class]
            - self.rac_booked[travel_class]
        )


# ============================================================
# PASSENGER CLASS
# ============================================================

class Passenger:
    """
    Stores passenger information.
    """

    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone


# ============================================================
# TICKET CLASS
# ============================================================

class Ticket:
    """
    Stores complete ticket information.
    """

    def __init__(
        self,
        pnr,
        train,
        passenger,
        travel_class,
        seat_number,
        berth_type,
        status,
        journey_date,
        journey_time,
        fare,
        wl_number=None
    ):

        self.pnr = pnr
        self.train = train
        self.passenger = passenger
        self.travel_class = travel_class
        self.seat_number = seat_number
        self.berth_type = berth_type
        self.status = status
        self.journey_date = journey_date
        self.journey_time = journey_time
        self.fare = fare
        self.wl_number = wl_number


# ============================================================
# ACCOUNT CLASS
# ============================================================

class Account:
    """
    Stores user login information.
    """

    accounts = {
        "admin": "admin123"
    }

    @classmethod
    def create_account(cls, username, password):

        if username in cls.accounts:
            return False, "Username already exists."

        cls.accounts[username] = password

        return True, "Account created successfully."


# ============================================================
# MAIN APPLICATION
# ============================================================

class RailwayApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Railway Ticket Booking System")
        self.root.geometry("1250x750")
        self.root.minsize(1100, 650)

        # ----------------------------------------------------
        # Application data
        # ----------------------------------------------------

        self.trains = self.create_trains()

        self.tickets = []

        self.current_user = None

        # PNR starts from a random number
        self.pnr_counter = random.randint(100000, 999999)

        # Login screen
        self.show_login()


    # ========================================================
    # CREATE TRAIN DATA
    # ========================================================

    def create_trains(self):

        trains = [

            Train(
                "12723",
                "Telangana Express",
                "Hyderabad",
                "New Delhi",

                {
                    "1AC": 10,
                    "2AC": 20,
                    "3AC": 30,
                    "SL": 50,
                    "GEN": 100
                },

                {
                    "1AC": 2500,
                    "2AC": 1600,
                    "3AC": 1100,
                    "SL": 600,
                    "GEN": 250
                }
            ),

            Train(
                "12760",
                "Charminar Express",
                "Hyderabad",
                "Chennai",

                {
                    "1AC": 8,
                    "2AC": 15,
                    "3AC": 25,
                    "SL": 40,
                    "GEN": 80
                },

                {
                    "1AC": 2200,
                    "2AC": 1400,
                    "3AC": 950,
                    "SL": 500,
                    "GEN": 200
                }
            ),

            Train(
                "12701",
                "Hussain Sagar Express",
                "Hyderabad",
                "Mumbai",

                {
                    "1AC": 8,
                    "2AC": 18,
                    "3AC": 28,
                    "SL": 45,
                    "GEN": 90
                },

                {
                    "1AC": 2300,
                    "2AC": 1500,
                    "3AC": 1000,
                    "SL": 550,
                    "GEN": 220
                }
            )
        ]

        return trains


    # ========================================================
    # CLEAR SCREEN
    # ========================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()
    def open_railway_website(self):
         
        webbrowser.open("https://www.irctc.co.in/")


    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def show_login(self):

        self.clear_screen()

        frame = ttk.Frame(self.root, padding=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame,
            text="Railway Ticket Booking System",
            font=("Arial", 22, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(
            frame,
            text="Login",
            font=("Arial", 16, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Username:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )

        self.login_username = ttk.Entry(frame, width=30)
        self.login_username.grid(
            row=2, column=1, padx=10, pady=10
        )

        ttk.Label(frame, text="Password:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        self.login_password = ttk.Entry(
            frame,
            width=30,
            show="*"
        )

        self.login_password.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Button(
            frame,
            text="Login",
            command=self.login
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=15
        )

        ttk.Button(
            frame,
            text="Create Account",
            command=self.show_register
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=5
        )

        ttk.Label(
            frame,
            text="Demo Login: admin / admin123"
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            pady=10
        )
        ttk.Label(
            frame,
            text="Demo Login: admin / admin123"
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            pady=10
         )

        ttk.Button(
            frame,
            text="Visit IRCT Website",
            command=self.open_railway_website
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=10
        )


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )
            return

        if (
            username in Account.accounts
            and Account.accounts[username] == password
        ):

            self.current_user = username

            messagebox.showinfo(
                "Success",
                "Login successful!"
            )

            self.show_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )


    # ========================================================
    # REGISTER SCREEN
    # ========================================================

    def show_register(self):

        self.clear_screen()

        frame = ttk.Frame(self.root, padding=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame,
            text="Create Account",
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )

        ttk.Label(
            frame,
            text="Username:"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.register_username = ttk.Entry(
            frame,
            width=30
        )

        self.register_username.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Label(
            frame,
            text="Password:"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.register_password = ttk.Entry(
            frame,
            width=30,
            show="*"
        )

        self.register_password.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Button(
            frame,
            text="Create Account",
            command=self.register
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=15
        )

        ttk.Button(
            frame,
            text="Back to Login",
            command=self.show_login
        ).grid(
            row=4,
            column=0,
            columnspan=2
        )


    # ========================================================
    # REGISTER
    # ========================================================

    def register(self):

        username = self.register_username.get().strip()
        password = self.register_password.get().strip()

        if not username or not password:

            messagebox.showerror(
                "Error",
                "Username and password cannot be empty."
            )

            return

        if len(password) < 4:

            messagebox.showerror(
                "Error",
                "Password must contain at least 4 characters."
            )

            return

        success, message = Account.create_account(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.show_login()

        else:

            messagebox.showerror(
                "Error",
                message
            )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_screen()

        # ----------------------------------------------------
        # Top heading
        # ----------------------------------------------------

        heading = ttk.Frame(self.root)
        heading.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            heading,
            text="Railway Ticket Booking System",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ttk.Button(
            heading,
            text="Logout",
            command=self.show_login
        ).pack(side="right")

        ttk.Label(
            heading,
            text=f"Welcome, {self.current_user}"
        ).pack(side="right", padx=20)

        # ----------------------------------------------------
        # Notebook
        # ----------------------------------------------------

        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.train_tab = ttk.Frame(notebook)
        self.booking_tab = ttk.Frame(notebook)
        self.ticket_tab = ttk.Frame(notebook)

        notebook.add(
            self.train_tab,
            text="Available Trains"
        )

        notebook.add(
            self.booking_tab,
            text="Book Ticket"
        )

        notebook.add(
            self.ticket_tab,
            text="Booked Tickets"
        )

        self.create_train_tab()
        self.create_booking_tab()
        self.create_ticket_tab()


    # ========================================================
    # TRAIN TAB
    # ========================================================

    def create_train_tab(self):

        ttk.Label(
            self.train_tab,
            text="Available Trains",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        columns = (
            "number",
            "name",
            "source",
            "destination",
            "1AC",
            "2AC",
            "3AC",
            "SL",
            "GEN"
        )

        self.train_tree = ttk.Treeview(
            self.train_tab,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "number": "Train No.",
            "name": "Train Name",
            "source": "Source",
            "destination": "Destination",
            "1AC": "1AC",
            "2AC": "2AC",
            "3AC": "3AC",
            "SL": "SL",
            "GEN": "GEN"
        }

        for column in columns:

            self.train_tree.heading(
                column,
                text=headings[column]
            )

            self.train_tree.column(
                column,
                width=110
            )

        self.train_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.refresh_train_tree()


    # ========================================================
    # REFRESH TRAIN TREE
    # ========================================================

    def refresh_train_tree(self):

        for item in self.train_tree.get_children():
            self.train_tree.delete(item)

        for train in self.trains:

            self.train_tree.insert(
                "",
                "end",
                values=(
                    train.number,
                    train.name,
                    train.source,
                    train.destination,
                    train.available_seats("1AC"),
                    train.available_seats("2AC"),
                    train.available_seats("3AC"),
                    train.available_seats("SL"),
                    train.available_seats("GEN")
                )
            )


    # ========================================================
    # BOOKING TAB
    # ========================================================

    def create_booking_tab(self):

        main_frame = ttk.Frame(
            self.booking_tab,
            padding=15
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Passenger Details
        # ----------------------------------------------------

        passenger_frame = ttk.LabelFrame(
            main_frame,
            text="Passenger Details",
            padding=15
        )

        passenger_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Label(
            passenger_frame,
            text="Passenger Name:"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.name_entry = ttk.Entry(
            passenger_frame,
            width=25
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        ttk.Label(
            passenger_frame,
            text="Age:"
        ).grid(row=0, column=2, padx=10, pady=8)

        self.age_spin = ttk.Spinbox(
            passenger_frame,
            from_=1,
            to=120,
            width=10
        )

        self.age_spin.grid(
            row=0,
            column=3,
            padx=10,
            pady=8
        )

        ttk.Label(
            passenger_frame,
            text="Gender:"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.gender_combo = ttk.Combobox(
            passenger_frame,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            state="readonly",
            width=22
        )

        self.gender_combo.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        ttk.Label(
            passenger_frame,
            text="Phone:"
        ).grid(row=1, column=2, padx=10, pady=8)

        self.phone_entry = ttk.Entry(
            passenger_frame,
            width=25
        )

        self.phone_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        # ----------------------------------------------------
        # Journey Details
        # ----------------------------------------------------

        journey_frame = ttk.LabelFrame(
            main_frame,
            text="Journey Details",
            padding=15
        )

        journey_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Label(
            journey_frame,
            text="Train:"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.train_combo = ttk.Combobox(
            journey_frame,
            values=[
                f"{train.number} - {train.name}"
                for train in self.trains
            ],
            state="readonly",
            width=30
        )

        self.train_combo.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        self.train_combo.bind(
            "<<ComboboxSelected>>",
            self.update_class_details
        )

        ttk.Label(
            journey_frame,
            text="Journey Date:"
        ).grid(row=0, column=2, padx=10, pady=8)

        self.date_entry = ttk.Entry(
            journey_frame,
            width=20
        )

        self.date_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=8
        )

        ttk.Label(
            journey_frame,
            text="Journey Time:"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.time_entry = ttk.Entry(
            journey_frame,
            width=20
        )

        self.time_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        ttk.Label(
            journey_frame,
            text="Class:"
        ).grid(row=1, column=2, padx=10, pady=8)

        self.class_combo = ttk.Combobox(
            journey_frame,
            values=[
                "1AC",
                "2AC",
                "3AC",
                "SL",
                "GEN"
            ],
            state="readonly",
            width=20
        )

        self.class_combo.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        self.class_combo.bind(
            "<<ComboboxSelected>>",
            self.update_berths
        )

        # ----------------------------------------------------
        # Berth & Ticket Count
        # ----------------------------------------------------

        ttk.Label(
            journey_frame,
            text="Berth Preference:"
        ).grid(row=2, column=0, padx=10, pady=8)

        self.berth_combo = ttk.Combobox(
            journey_frame,
            state="readonly",
            width=20
        )

        self.berth_combo.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        ttk.Label(
            journey_frame,
            text="Number of Tickets:"
        ).grid(row=2, column=2, padx=10, pady=8)

        self.ticket_spin = ttk.Spinbox(
            journey_frame,
            from_=1,
            to=10,
            width=10
        )

        self.ticket_spin.set(1)

        self.ticket_spin.grid(
            row=2,
            column=3,
            padx=10,
            pady=8
        )

        # ----------------------------------------------------
        # Book Button
        # ----------------------------------------------------

        ttk.Button(
            main_frame,
            text="BOOK TICKET",
            command=self.book_ticket
        ).pack(
            pady=15
        )

        # ----------------------------------------------------
        # Information
        # ----------------------------------------------------

        self.booking_info = ttk.Label(
            main_frame,
            text="Select a train and class.",
            font=("Arial", 11)
        )

        self.booking_info.pack(pady=5)


    # ========================================================
    # UPDATE CLASS INFORMATION
    # ========================================================

    def update_class_details(self, event=None):

        selected = self.train_combo.get()

        if not selected:
            return

        train_number = selected.split(" - ")[0]

        train = self.get_train(train_number)

        if train:

            self.booking_info.config(
                text=(
                    f"1AC: ₹{train.fares['1AC']} | "
                    f"2AC: ₹{train.fares['2AC']} | "
                    f"3AC: ₹{train.fares['3AC']} | "
                    f"SL: ₹{train.fares['SL']} | "
                    f"GEN: ₹{train.fares['GEN']}"
                )
            )


    # ========================================================
    # UPDATE BERTH TYPES
    # ========================================================

    def update_berths(self, event=None):

        travel_class = self.class_combo.get()

        if travel_class == "GEN":

            self.berth_combo["values"] = ["No Berth"]
            self.berth_combo.set("No Berth")

        elif travel_class in ["1AC", "2AC"]:

            values = [
                "Auto",
                "Lower Berth",
                "Upper Berth",
                "Side Lower Berth",
                "Side Upper Berth"
            ]

            self.berth_combo["values"] = values
            self.berth_combo.set("Auto")

        else:

            values = [
                "Auto",
                "Lower Berth",
                "Middle Berth",
                "Upper Berth",
                "Side Lower Berth",
                "Side Upper Berth"
            ]

            self.berth_combo["values"] = values
            self.berth_combo.set("Auto")


    # ========================================================
    # GET TRAIN
    # ========================================================

    def get_train(self, train_number):

        for train in self.trains:

            if train.number == train_number:
                return train

        return None


    # ========================================================
    # GENERATE PNR
    # ========================================================

    def generate_pnr(self):

        self.pnr_counter += 1

        return str(self.pnr_counter)


    # ========================================================
    # VALIDATE DATE
    # ========================================================

    def validate_date(self, date_text):

        try:

            datetime.strptime(
                date_text,
                "%d-%m-%Y"
            )

            return True

        except ValueError:

            return False


    # ========================================================
    # VALIDATE TIME
    # ========================================================

    def validate_time(self, time_text):

        try:

            datetime.strptime(
                time_text,
                "%H:%M"
            )

            return True

        except ValueError:

            return False


    # ========================================================
    # BOOK TICKET
    # ========================================================

    def book_ticket(self):

        # ----------------------------------------------------
        # Get passenger information
        # ----------------------------------------------------

        name = self.name_entry.get().strip()
        age_text = self.age_spin.get().strip()
        gender = self.gender_combo.get()
        phone = self.phone_entry.get().strip()

        # ----------------------------------------------------
        # Get journey information
        # ----------------------------------------------------

        train_selection = self.train_combo.get()
        journey_date = self.date_entry.get().strip()
        journey_time = self.time_entry.get().strip()
        travel_class = self.class_combo.get()
        berth_preference = self.berth_combo.get()
        ticket_count_text = self.ticket_spin.get().strip()

        # ----------------------------------------------------
        # Validate name
        # ----------------------------------------------------

        if not name:

            messagebox.showerror(
                "Validation Error",
                "Please enter passenger name."
            )

            return

        if not all(
            character.isalpha() or character.isspace()
            for character in name
        ):

            messagebox.showerror(
                "Validation Error",
                "Name should contain only letters."
            )

            return

        # ----------------------------------------------------
        # Validate age
        # ----------------------------------------------------

        try:

            age = int(age_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Age must be a number."
            )

            return

        if age < 1 or age > 120:

            messagebox.showerror(
                "Validation Error",
                "Age must be between 1 and 120."
            )

            return

        # ----------------------------------------------------
        # Validate gender
        # ----------------------------------------------------

        if not gender:

            messagebox.showerror(
                "Validation Error",
                "Please select gender."
            )

            return

        # ----------------------------------------------------
        # Validate phone
        # ----------------------------------------------------

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showerror(
                "Validation Error",
                "Phone number must contain exactly 10 digits."
            )

            return

        # ----------------------------------------------------
        # Validate train
        # ----------------------------------------------------

        if not train_selection:

            messagebox.showerror(
                "Validation Error",
                "Please select a train."
            )

            return

        train_number = train_selection.split(" - ")[0]

        train = self.get_train(train_number)

        if not train:

            messagebox.showerror(
                "Error",
                "Selected train not found."
            )

            return

        # ----------------------------------------------------
        # Validate date
        # ----------------------------------------------------

        if not journey_date:

            messagebox.showerror(
                "Validation Error",
                "Please enter journey date."
            )

            return

        if not self.validate_date(journey_date):

            messagebox.showerror(
                "Validation Error",
                "Date format must be DD-MM-YYYY."
            )

            return

        # ----------------------------------------------------
        # Validate time
        # ----------------------------------------------------

        if not journey_time:

            messagebox.showerror(
                "Validation Error",
                "Please enter journey time."
            )

            return

        if not self.validate_time(journey_time):

            messagebox.showerror(
                "Validation Error",
                "Time format must be HH:MM."
            )

            return

        # ----------------------------------------------------
        # Validate class
        # ----------------------------------------------------

        if travel_class not in [
            "1AC",
            "2AC",
            "3AC",
            "SL",
            "GEN"
        ]:

            messagebox.showerror(
                "Validation Error",
                "Please select a valid class."
            )

            return

        # ----------------------------------------------------
        # Validate ticket count
        # ----------------------------------------------------

        try:

            ticket_count = int(ticket_count_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Ticket count must be a number."
            )

            return

        if ticket_count < 1 or ticket_count > 10:

            messagebox.showerror(
                "Validation Error",
                "Ticket count must be between 1 and 10."
            )

            return

        # ----------------------------------------------------
        # Passenger object
        # ----------------------------------------------------

        passenger = Passenger(
            name,
            age,
            gender,
            phone
        )

        booking_results = []

        # ----------------------------------------------------
        # Book requested tickets
        # ----------------------------------------------------

        for i in range(ticket_count):

            # ================================================
            # CONFIRMED
            # ================================================

            if train.available_seats(travel_class) > 0:

                train.booked_seats[travel_class] += 1

                seat_number = train.booked_seats[travel_class]

                # Automatic berth
                automatic_berth = Berth.get_berth_type(
                    seat_number,
                    travel_class
                )

                # Manual berth preference
                if travel_class == "GEN":

                    berth_type = "No Berth"

                elif (
                    berth_preference
                    and berth_preference != "Auto"
                ):

                    berth_type = berth_preference

                else:

                    berth_type = automatic_berth

                status = "CNF"

                pnr = self.generate_pnr()

                fare = train.fares[travel_class]

                ticket = Ticket(
                    pnr,
                    train.number,
                    passenger,
                    travel_class,
                    seat_number,
                    berth_type,
                    status,
                    journey_date,
                    journey_time,
                    fare
                )

                self.tickets.append(ticket)

                booking_results.append(
                    f"PNR {pnr}: CNF - "
                    f"Seat {seat_number}, "
                    f"{berth_type}"
                )

            # ================================================
            # RAC
            # ================================================

            elif train.available_rac(travel_class) > 0:

                train.rac_booked[travel_class] += 1

                rac_number = train.rac_booked[travel_class]

                pnr = self.generate_pnr()

                status = "RAC"

                # RAC gets side lower/shared berth
                berth_type = "RAC Berth"

                fare = train.fares[travel_class]

                ticket = Ticket(
                    pnr,
                    train.number,
                    passenger,
                    travel_class,
                    f"RAC-{rac_number}",
                    berth_type,
                    status,
                    journey_date,
                    journey_time,
                    fare
                )

                self.tickets.append(ticket)

                booking_results.append(
                    f"PNR {pnr}: RAC - "
                    f"RAC Number {rac_number}"
                )

            # ================================================
            # WAITING LIST
            # ================================================

            else:

                train.waiting_list[travel_class] += 1

                wl_number = train.waiting_list[travel_class]

                pnr = self.generate_pnr()

                status = "WL"

                fare = train.fares[travel_class]

                ticket = Ticket(
                    pnr,
                    train.number,
                    passenger,
                    travel_class,
                    f"WL-{wl_number}",
                    "No Berth",
                    status,
                    journey_date,
                    journey_time,
                    fare,
                    wl_number
                )

                self.tickets.append(ticket)

                booking_results.append(
                    f"PNR {pnr}: WL - "
                    f"Waiting Number {wl_number}"
                )

        # ----------------------------------------------------
        # Refresh train display
        # ----------------------------------------------------

        self.refresh_train_tree()

        self.refresh_ticket_tree()

        # ----------------------------------------------------
        # Show result
        # ----------------------------------------------------

        result = "\n".join(booking_results)

        messagebox.showinfo(
            "Booking Result",
            f"Booking completed successfully!\n\n{result}"
        )

        # Clear form
        self.clear_booking_form()


    # ========================================================
    # CLEAR BOOKING FORM
    # ========================================================

    def clear_booking_form(self):

        self.name_entry.delete(0, tk.END)

        self.age_spin.set(1)

        self.gender_combo.set("")

        self.phone_entry.delete(0, tk.END)

        self.train_combo.set("")

        self.date_entry.delete(0, tk.END)

        self.time_entry.delete(0, tk.END)

        self.class_combo.set("")

        self.berth_combo.set("")

        self.ticket_spin.set(1)

        self.booking_info.config(
            text="Select a train and class."
        )


    # ========================================================
    # TICKET TAB
    # ========================================================

    def create_ticket_tab(self):

        ttk.Label(
            self.ticket_tab,
            text="Booked Tickets",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        columns = (
            "pnr",
            "train",
            "class",
            "name",
            "age",
            "gender",
            "berth",
            "seat",
            "status",
            "date",
            "time",
            "fare"
        )

        self.ticket_tree = ttk.Treeview(
            self.ticket_tab,
            columns=columns,
            show="headings",
            height=18
        )

        headings = {
            "pnr": "PNR",
            "train": "Train",
            "class": "Class",
            "name": "Passenger",
            "age": "Age",
            "gender": "Gender",
            "berth": "Berth",
            "seat": "Seat No.",
            "status": "Status",
            "date": "Journey Date",
            "time": "Journey Time",
            "fare": "Fare"
        }

        widths = {
            "pnr": 80,
            "train": 70,
            "class": 60,
            "name": 130,
            "age": 50,
            "gender": 70,
            "berth": 130,
            "seat": 80,
            "status": 70,
            "date": 100,
            "time": 90,
            "fare": 80
        }

        for column in columns:

            self.ticket_tree.heading(
                column,
                text=headings[column]
            )

            self.ticket_tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            self.ticket_tab,
            orient="vertical",
            command=self.ticket_tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.ticket_tab,
            orient="horizontal",
            command=self.ticket_tree.xview
        )

        self.ticket_tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.ticket_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 0)
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        ttk.Button(
            self.ticket_tab,
            text="Refresh Tickets",
            command=self.refresh_ticket_tree
        ).pack(pady=10)


    # ========================================================
    # REFRESH TICKET TREE
    # ========================================================

    def refresh_ticket_tree(self):

        if not hasattr(self, "ticket_tree"):
            return

        for item in self.ticket_tree.get_children():

            self.ticket_tree.delete(item)

        for ticket in self.tickets:

            passenger = ticket.passenger

            self.ticket_tree.insert(
                "",
                "end",
                values=(
                    ticket.pnr,
                    ticket.train,
                    ticket.travel_class,
                    passenger.name,
                    passenger.age,
                    passenger.gender,
                    ticket.berth_type,
                    ticket.seat_number,
                    ticket.status,
                    ticket.journey_date,
                    ticket.journey_time,
                    f"₹{ticket.fare}"
                )
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = RailwayApp(root)

    root.mainloop()