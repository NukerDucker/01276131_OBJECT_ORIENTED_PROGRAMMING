class Member:
    def __init__(self, name: str, email: str = None, phone: str = None):
        self.__name = name
        self.__email = email
        self.__phone = phone

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def phone(self):
        return self.__phone


class Notification:
    @staticmethod
    def send(member, message):
        if member.phone:
            print(f'Sending SMS to {member.name}: {message}')
        elif member.email:
            print(f'Sending Email to {member.name}: {message}')


class AppointmentDetails:
    def __init__(self, title: str, location: str, date: str = None):
        self.title = title
        self.location = location
        self.date = date

    def notify(self, members):
        raise NotImplementedError("Subclasses should implement this method.")

    def __str__(self):
        return f'Topic: {self.title}, Location: {self.location}, Date: {self.date}'


class OneTimeAppointment(AppointmentDetails):
    schedule_type = 'OneTime'

    def __init__(self, title: str, location: str, date: str, attendees: list):
        super().__init__(title, location, date)
        self.attendees = attendees

    def add_attendee(self, member):
        self.attendees.append(member)

    def notify(self, members):
        for attendee in self.attendees:
            member = members.get(attendee)
            if member:
                Notification.send(member, f'You have an appointment "{self.title}"')

    def __str__(self):
        attendees = ", ".join(self.attendees)
        return f'{self.schedule_type} - {super().__str__()} Attn: {attendees}'


class WeeklyAppointment(AppointmentDetails):
    schedule_type = 'Weekly'

    def __init__(self, title: str, location: str, day_of_week: str, attendees: list):
        super().__init__(title, location)
        self.day_of_week = day_of_week
        self.attendees = attendees

    def add_attendee(self, member):
        self.attendees.append(member)

    def notify(self, members):
        for attendee in self.attendees:
            member = members.get(attendee)
            if member:
                Notification.send(member, f'You have a weekly appointment "{self.title}" on {self.day_of_week}')

    def __str__(self):
        attendees = ", ".join(self.attendees)
        return f'{self.schedule_type} - {super().__str__()} on {self.day_of_week} Attn: {attendees}'


class Activity(AppointmentDetails):
    schedule_type = 'Activity'

    def notify(self, members):
        for member in members.values():
            Notification.send(member, f'You have an activity "{self.title}"')

    def __str__(self):
        return f'{self.schedule_type} - {super().__str__()}'


class AppointmentScheduler:
    def __init__(self):
        self.appointments = []
        self.activities = []
        self.members = {}

    def add_member(self, name, email, phone=None):
        if name not in self.members:
            self.members[name] = Member(name, email, phone)
        else:
            print(f"Member {name} already exists.")

    def add_appointment(self, appointment: AppointmentDetails):
        self.appointments.append(appointment)

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def view_appointments(self):
        for appointment in self.appointments + self.activities:
            print(appointment)

    def edit_appointment(self, title: str, new_title: str = None, new_location: str = None, new_date: str = None):
        for appointment in self.appointments + self.activities:
            if appointment.title == title:
                if new_title: appointment.title = new_title
                if new_location: appointment.location = new_location
                if new_date: appointment.date = new_date

    def delete_appointment(self, title: str):
        self.appointments = [appt for appt in self.appointments if appt.title != title]
        self.activities = [act for act in self.activities if act.title != title]

    def add_attendee(self, title: str, attendee: str):
        for appointment in self.appointments:
            if appointment.title == title and hasattr(appointment, 'add_attendee'):
                appointment.add_attendee(attendee)

    def search_member_appointments(self, member_name: str):
        for appointment in self.appointments:
            if member_name in appointment.attendees:
                print(appointment)
        for activity in self.activities:
            print(activity)

    def send_notifications(self, title: str):
        for appointment in self.appointments + self.activities:
            if appointment.title == title:
                appointment.notify(self.members)


app = AppointmentScheduler()

# Add Members
app.add_member("John Doe", "john.doe@example.com")
app.add_member("Jane Smith", "jane.smith@example.com")
app.add_member("Robert Johnson", "robert.johnson@example.com", "08-1234-5678")
app.add_member("Emily Davis", "emily.davis@example.com", "08-3456-7890")

# Add Appointments
app.add_appointment(OneTimeAppointment(title="Team Meeting #1", location="Room A", date="2024-03-15", attendees=["Jane Smith", "Robert Johnson", "Emily Davis"]))
app.add_appointment(OneTimeAppointment(title="Team Meeting #2", location="Room B", date="2024-03-17", attendees=["Jane Smith", "Robert Johnson", "Emily Davis"]))
app.add_appointment(WeeklyAppointment(title="Weekly Meeting", location="Room C", day_of_week="Wednesday", attendees=["John Doe", "Robert Johnson", "Emily Davis"]))

# Add Activities
app.add_activity(Activity(title="Company Party", location="Conference Room", date="2024-03-17"))
app.add_activity(Activity(title="Company Visit", location="Conference Room", date="2024-03-17"))

# View appointments
print("# # Test Case 1 : Add Appointment, add activity information, and add appointment information.")
app.view_appointments()
print()
# Edit Appointment
print("Test Case 2 : Edit Appointment")
app.edit_appointment(title="Team Meeting #1", new_title="Team B Meeting #1")
app.edit_appointment(title="Team Meeting #2", new_location="Room C")
app.view_appointments()
print()
# Delete Appointment
print("Test Case 3 : Delete Appointment using topic “Team Meeting #2”")
app.delete_appointment(title="Team Meeting #2")
app.view_appointments()
print()
# Add Attendance
print("Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments")
app.add_attendee("Team B Meeting #1", "John Doe")
app.add_attendee("Weekly Meeting", "Jane Smith")
app.view_appointments()
print()
# Search Attendance
print("Test Case 5 : Search Attendance Search for individual appointments using the name Robert Johnson")
app.search_member_appointments("Robert Johnson")
print()
# Send Notifications
print("Test Case 6 : Notify by using the appointment “Team B Meeting #1”")
app.send_notifications("Team B Meeting #1")
