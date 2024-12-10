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
        
class AppointmentDetails:
    def __init__(self, title: str = None, location: str = None, date: str = None, attendees: list = None):
        self.title = title
        self.location = location
        self.date = date
        self.attendees = attendees if attendees else []
        
    def add_attendee(self, member):
        if member not in self.attendees:
            self.attendees.append(member)

class OneTimeAppointment(AppointmentDetails):
    schedule_type = 'OneTime'

class WeeklyAppointment(AppointmentDetails):
    schedule_type = 'Weekly'
    
    def __init__(self, title: str, location: str, date: str = None, day_of_week: str = None, attendees: list = None):
        super().__init__(title, location, date, attendees)
        self.day_of_week = day_of_week

class ActivityDetails(AppointmentDetails):
    schedule_type = 'Activity'

class AppointmentScheduler:
    def __init__(self):
        self.appointments = []
        self.activities = []
        self.members = []
    
    def add_item(self, collection, item):
        if item not in collection:
            collection.append(item)

    def remove_item(self, collection, item):
        if item in collection:
            collection.remove(item)
            
    def add_appointment(self, appointment: AppointmentDetails):
        self.add_item(self.appointments, appointment)
        
    def add_activity(self, activity: ActivityDetails):
        self.add_item(self.activities, activity)
        
    def add_member(self, member: Member):
        self.add_item(self.members, member)
        
    def remove_appointment(self, appointment: AppointmentDetails):
        self.remove_item(self.appointments, appointment)
        
    def remove_activity(self, activity: ActivityDetails):
        self.remove_item(self.activities, activity)
        
    def remove_member(self, member: Member):
        self.remove_item(self.members, member)
    
    def search_member(self, name: str):
        return next((member for member in self.members if member.name == name), None)
    
    def view_appointments(self):
        for appointment in self.appointments:
            attendees = ", ".join(appointment.attendees) if appointment.attendees else "None"
            print(f'{appointment.schedule_type} - Topic: {appointment.title}, Location: {appointment.location}, Date: {appointment.date}, Attendees: {attendees}')
    
    def edit_appointment(self, title: str = None, location: str = None, date: str = None, to=None):
        for appointment in self.appointments:
            if title and appointment.title == title:
                appointment.title = to
            if location and appointment.location == location:
                appointment.location = to
            if date and appointment.date == date:
                appointment.date = to

    def delete_appointment(self, title: str):
        self.appointments = [appt for appt in self.appointments if appt.title != title]
                
    def add_attendee(self, title: str, attendee: str):
        appointment = next((appt for appt in self.appointments if appt.title == title), None)
        if appointment:
            appointment.add_attendee(attendee)
                
    def show_person_in_appointment(self, member):
        name = member.name if isinstance(member, Member) else member
        for appointment in self.appointments:
            if name in appointment.attendees:
                attendees = ", ".join(appointment.attendees)
                print(f'Topic: {appointment.title}, Location: {appointment.location}, Date: {appointment.date}, Attendees: {attendees}')
    
    def send_notifications(self, topic: str, message: str):
        appointment = next((appt for appt in self.appointments if appt.title == topic), None)
        if not appointment:
            return
        
        for attendee in appointment.attendees:
            member = self.search_member(attendee)
            if member:
                if member.phone:
                    print(f'Sending SMS to {attendee}: {message}')
                elif member.email:
                    print(f'Sending Email to {attendee}: {message}')
        
app = AppointmentScheduler()

members = {'John Doe':['john.doe@example.com', ''],
           'Jane Smith':['jane.smith@example.com', ''],
           'Robert Johnson':["robert.johnson@example.com", "08-1234-5678"],
           'Emily Davis':["emily.davis@example.com", "08-3456-7890"]}

for name, info in members.items():
    app.add_member(Member(name, info[0], info[1]))
    
#######################################################################

def seperator():
    print('--------------------------------------------------------------')

# # Test Case 1 : Add Appointment เพิ่มข้อมูล กิจกรรม  และเพิ่มข้อมูลการนัดหมาย 
# 1 : title="Team Meeting #1", location="Room A" , date="2024-03-15", Jane Smith, Robert Johnson,  Emily Davis
# 2 : title="Team Meeting #2", location="Room B" , date="2024-03-17", Jane Smith, Robert Johnson และ Emily Davis
# 3 : title="Weekly Meeting", location="Room C" , day_of_week="Wednesday"
# Activity
# 4 : title="Company Party", location="Conference Room", date="2024-03-17"
# 5 : title="Company Visit", location="Conference Room", date="2024-03-17"

# Output Expect
# Topic : Team Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room B on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
    
app.add_appointment(OneTimeAppointment(title="Team Meeting #1", location="Room A" , date="2024-03-15", attendees=['Jane Smith','Robert Johnson', 'Emily Davis']))
app.add_appointment(OneTimeAppointment(title="Team Meeting #2", location="Room B" , date="2024-03-17", attendees=['Jane Smith','Robert Johnson', 'Emily Davis']))

app.add_appointment(WeeklyAppointment(title="Weekly Meeting", location="Room C" , date="2024-03-17", day_of_week="Wednesday"))

app.add_activity(ActivityDetails(title="Company Party", location="Conference Room", date="2024-03-17"))
app.add_activity(ActivityDetails(title="Company Visit", location="Conference Room", date="2024-03-17"))

print("Test Case 1 : Add Appointment เพิ่มข้อมูล กิจกรรม  และเพิ่มข้อมูลการนัดหมาย ")
app.view_appointments()            # แสดง Appointment ทั้งหมด
seperator()

'''----------------------------------------------------------------------------------------------------------'''

# # Test Case 2 : Edit Appointment แก้ไข การนัดหมาย/กิจกรรม 
# เปลี่ยนชื่อ การนัดหมาย รายครั้ง #1 จาก “Team Meeting #1” เป็น “Team B Meeting #1”
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room C on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 2 : Edit Appointment แก้ไข การนัดหมาย/กิจกรรม ")
app.edit_appointment(title="Team Meeting #1",to="Team B Meeting #1")
app.edit_appointment(location="Room B",to="Room C")
app.view_appointments()            # แสดง Appointment ทั้งหมด
seperator()

'''----------------------------------------------------------------------------------------------------------'''

# # Test Case 3 : Delete Appointment ลบ การนัดหมาย/กิจกรรม โดยใช้ topic “Team Meeting #2” 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 3 : Delete Appointment ลบ การนัดหมาย/กิจกรรม โดยใช้ topic “Team Meeting #2”")
app.delete_appointment(title="Team Meeting #2")
app.view_appointments()            # แสดง Appointment ทั้งหมด
seperator()

'''----------------------------------------------------------------------------------------------------------'''
# # Test Case 4 : Add Attendance ผู้ได้รับการนัดหมาย สำหรับ การนัดหมายรายครั้ง และ การนัดหมายรายสัปดาห์ ดังนี้
# -	การนัดหมาย รายครั้ง #1 (“Team B Meeting #1”) เพิ่ม John Doe
# -	การนัดหมาย รายสัปดาห์ “Weekly Meeting” เพิ่ม Jane Smith
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 4 : Add Attendance ผู้ได้รับการนัดหมาย สำหรับ การนัดหมายรายครั้ง และ การนัดหมายรายสัปดาห์")
app.add_attendee("Team B Meeting #1", 'John Doe')
app.add_attendee("Weekly Meeting", 'Jane Smith')
app.view_appointments()            # แสดง Appointment ทั้งหมด
seperator()

'''----------------------------------------------------------------------------------------------------------'''
# # Test Case 5 : Search Attendance ค้นหาการนัดหมายรายบุคคล โดยใช้ชื่อ “Robert Johnson” 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
print("Test Case 5 : Search Attendance ค้นหาการนัดหมายรายบุคคล โดยใช้ชื่อ Robert Johnson")
john = app.search_member("Robert Johnson")
app.show_person_in_appointment(john)
app.show_person_in_appointment("Robert Johnson")
seperator()

'''----------------------------------------------------------------------------------------------------------'''
# # Test Case 6 : แจ้ง Notification โดยใช้การนัดหมาย “Team B Meeting #1”
# Output Expect
# Sending email notification to: jane.smith@example.com with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
# Sending SMS notification to : 08-3456-7890 with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
print("""Test Case 6 : แจ้ง Notification โดยใช้การนัดหมาย “Team B Meeting #1""")
app.send_notifications("Team B Meeting #1","invite for meeting")