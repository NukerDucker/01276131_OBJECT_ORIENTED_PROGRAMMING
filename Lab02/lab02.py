class Teacher:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def getName(self):
        return self.name
    
class Student:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.subject_list = []

    def addToSubject(self, subject, grade=None):
        for subject_info in self.subject_list:
            if subject_info[0] == subject:
                subject_info[1] = grade
                return
        self.subject_list.append([subject, grade])


    def setGrade(self, subject_name: str, grade):
        for i, subject_info in enumerate(self.subject_list):
            if subject_info[0].name == subject_name:
                self.subject_list[i] = (subject_info[0], grade)
                return

    def getName(self):
        return self.name

    def getID(self):
        return self.id
    
    def getSubject(self):
        return [subject_info for subject_info in self.subject_list]
    
class Subject:
    def __init__(self, id: str, name: str, credit: int, teacher: str = None):
        self.id = id
        self.name = name
        self.credit = credit
        self.student_list = []
        self.teacher = teacher

    def addStudent(self, student):
        if student not in self.student_list:
            self.student_list.append(student)
        
    def removeStudent(self, student: str):
        if student in self.student_list:
            self.student_list.remove(student)
        
    def addTeacher(self, teacher: str):
        if teacher or teacher == None:
            self.teacher = teacher

    def removeTeacher(self, teacher: str):
        if self.teacher == teacher:
            self.teacher = None

    def getTeacher(self):
        return self.teacher
        
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getStudent_list(self):
        return self.student_list if self.student_list else None
    
    def getStudentCount(self):
        return len(self.student_list) if self.student_list else 0

student_list = []
subject_list = []
teacher_list = []
enrollment_list = []

def search_subject_by_id(subject_id: str):
    return next((subject for subject in subject_list if subject.id == subject_id), None)

def search_student_by_id(student_id):
    return next((student for student in student_list if student.id == student_id), None)

def enroll_to_subject(student: Student, subject: Subject):
    try:
        if (student, subject) in enrollment_list:
            return "Already Enrolled"
        enrollment_list.append((student, subject))
        student.addToSubject(subject)
        subject.addStudent(student)
        return "Done"
    except Exception:
        return "Error"
    
def drop_from_subject(student: Student, subject: Subject):
    if not isinstance(student, Student) or not isinstance(subject, Subject):
        return "Error"
    try:
        if (student, subject) in enrollment_list:
            return "Not Found"
        enrollment_list.remove((student, subject))
        subject.removeStudent(student)
        student.removeFromSubject(subject)
        return "Done"
    except Exception:
        return "Error"
    
def search_enrollment_subject_student(subject, student):
    if (student, subject) in enrollment_list:
        return (subject, student)
    return "Not Found"

def search_student_enroll_in_subject(subject):
    try:
        return subject.getStudent_list()
    except Exception:
        return "Error"

def search_subject_that_student_enrolled(student):
    try:
        return student.getSubject() if student else "Not Found"
    except Exception:
        return "Error"

def assign_grade(student, subject, grade):
    try:
        return student.setGrade(subject.name, grade) if student and subject else "Not Found"
    except Exception:
        return "Error"

def get_teacher_teach(subject_search):
    return subject_search.getTeacher() if subject_search else "Not Found"

def get_no_of_student_enrolled(subject):
    try:
        return subject.getStudentCount() if subject else "Not Found"
    except Exception:
        return "Error"

def get_student_record(student):
    if not student:
        return {}
    return {subject[0].id: [subject[0].name, subject[1]] for subject in student.getSubject()}

def grade_to_count(grade):
    grade_mapping = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
    return grade_mapping.get(grade, 0)

def get_student_GPS(student):
    student_record = get_student_record(student)
    total_credit = 0
    total_grade = 0
    for subject in student_record:
        total_credit += search_subject_by_id(subject).credit
        total_grade += grade_to_count(student_record[subject][1]) * search_subject_by_id(subject).credit
    return total_grade / total_credit

def list_student_enrolled_in_subject(subject_id):
    subject = search_subject_by_id(subject_id)
    if subject is None:
        return "Subject not found"
    filter_student_list = search_student_enroll_in_subject(subject)
    student_dict = {}
    for enrollment in filter_student_list:
        student_dict[enrollment.getID()] = enrollment.getName()
    return student_dict

def list_subject_enrolled_by_student(student_id):
    student = search_student_by_id(student_id)
    if student is None:
        return "Student not found"
    filter_subject_list = search_subject_that_student_enrolled(student)
    subject_dict = {}
    for enrollment in filter_subject_list:
        subject_dict[enrollment.subject.getID()] = enrollment.subject.getName()
    return subject_dict

#######################################################################################

#สร้าง instance พื้นฐาน
def create_instance():
    students = [
        ('66010001', "Keanu Welsh"),
        ('66010002', "Khadijah Burton"),
        ('66010003', "Jean Caldwell"),
        ('66010004', "Jayden Mccall"),
        ('66010005', "Owain Johnston"),
        ('66010006', "Isra Cabrera"),
        ('66010007', "Frances Haynes"),
        ('66010008', "Steven Moore"),
        ('66010009', "Zoe Juarez"),
        ('66010010', "Sebastien Golden")
    ]
    
    subjects = [
        ('CS101', "Computer Programming 1", 3),
        ('CS102', "Computer Programming 2", 3),
        ('CS103', "Data Structure", 3)
    ]

    teachers = [
        ('T001', "Mr. Welsh"),
        ('T002', "Mr. Burton"),
        ('T003', "Mr. Smith")
    ]
    
    subject_list.extend([Subject(id, name, credit) for id, name, credit in subjects])
    teacher_list.extend([Teacher(id, name) for id, name in teachers])
    student_list.extend([Student(id, name) for id, name in students])

    subject_list[0].addTeacher(teacher_list[0])
    subject_list[1].addTeacher(teacher_list[1]) 
    subject_list[2].addTeacher(teacher_list[2])

# # ลงทะเบียน
def register():
    enroll_to_subject(student_list[0], subject_list[0])  # 001 -> CS101
    enroll_to_subject(student_list[0], subject_list[1])  # 001 -> CS102
    enroll_to_subject(student_list[0], subject_list[2])  # 001 -> CS103
    enroll_to_subject(student_list[1], subject_list[0])  # 002 -> CS101
    enroll_to_subject(student_list[1], subject_list[1])  # 002 -> CS102
    enroll_to_subject(student_list[1], subject_list[2])  # 002 -> CS103
    enroll_to_subject(student_list[2], subject_list[0])  # 003 -> CS101
    enroll_to_subject(student_list[2], subject_list[1])  # 003 -> CS102
    enroll_to_subject(student_list[2], subject_list[2])  # 003 -> CS103
    enroll_to_subject(student_list[3], subject_list[0])  # 004 -> CS101
    enroll_to_subject(student_list[3], subject_list[1])  # 004 -> CS102
    enroll_to_subject(student_list[4], subject_list[0])  # 005 -> CS101
    enroll_to_subject(student_list[4], subject_list[2])  # 005 -> CS103
    enroll_to_subject(student_list[5], subject_list[1])  # 006 -> CS102
    enroll_to_subject(student_list[5], subject_list[2])  # 006 -> CS103
    enroll_to_subject(student_list[6], subject_list[0])  # 007 -> CS101
    enroll_to_subject(student_list[7], subject_list[1])  # 008 -> CS102
    enroll_to_subject(student_list[8], subject_list[2])  # 009 -> CS103


create_instance()
register()


### Test Case #1 : test enroll_to_subject complete ###
student_enroll = list_student_enrolled_in_subject('CS101')
print("Test Case #1 : test enroll_to_subject complete")
print("Answer : {'66010001': 'Keanu Welsh', '66010002': 'Khadijah Burton', '66010003': 'Jean Caldwell', '66010004': 'Jayden Mccall', '66010005': 'Owain Johnston', '66010007': 'Frances Haynes'}")
print(student_enroll)
print("")

### Test case #2 : test enroll_to_subject in case of invalid argument
print("Test case #2 : test enroll_to_subject in case of invalid argument")
print("Answer : Error")
print(enroll_to_subject('66010001','CS101'))
print("")

### Test case #3 : test enroll_to_subject in case of duplicate enrolled
print("Test case #3 : test enroll_to_subject in case of duplicate enrolled")
print("Answer : Already Enrolled")
print(enroll_to_subject(student_list[0], subject_list[0]))
print("")

### Test case #4 : test drop_from_subject in case of invalid argument 
print("Test case #4 : test drop_from_subject in case of invalid argument")
print("Answer : Error")
print(drop_from_subject('66010001', 'CS101'))
print("")

### Test case #5 : test drop_from_subject in case of not found 
print("Test case #5 : test drop_from_subject in case of not found")
print("Answer : Not Found")
print(drop_from_subject(student_list[8], subject_list[0]))
print("")

### Test case #6 : test drop_from_subject in case of drop successful
print("Test case #6 : test drop_from_subject in case of drop successful")
print("Answer : {'66010002': 'Khadijah Burton', '66010003': 'Jean Caldwell', '66010004': 'Jayden Mccall', '66010005': 'Owain Johnston', '66010007': 'Frances Haynes'}")
drop_from_subject(student_list[0], subject_list[0])
print(list_student_enrolled_in_subject(subject_list[0].getID()))
print("")

### Test case #7 : test search_student_enrolled_in_subject
print("Test case #7 : test search_student_enrolled_in_subject")
print("Answer : ['66010002','66010003','66010004','66010005','66010007']")
lst = search_student_enroll_in_subject(subject_list[0])
print([i.getID() for i in lst])
print("")

### Test case #8 : get_no_of_student_enrolled
print("Test case #8 get_no_of_student_enrolled")
print("Answer : 5")
print(get_no_of_student_enrolled(subject_list[0]))
print("")

### Test case #9 : search_subject_that_student_enrolled
print("Test case #9 search_subject_that_student_enrolled")
print("Answer : ['CS102','CS103']")
lst = search_subject_that_student_enrolled(student_list[0])
print([i[0].getID() for i in lst])
print("")

### Test case #10 : get_teacher_teach
print("Test case #10 get_teacher_teach")
print("Answer : Mr. Welsh")
print(get_teacher_teach(subject_list[0]).getName())
print("")

### Test case #11 : search_enrollment_subject_student
print("Test case #11 search_enrollment_subject_student")
print("Answer : CS101 66010002")
enroll = search_enrollment_subject_student(subject_list[0],student_list[1])
print(enroll[0].getID(), enroll[1].getID())
print("")

### Test case #12 : assign_grade
print("Test case #12 assign_grade")
print("Answer : Done")
assign_grade(student_list[1],subject_list[0],'A')
assign_grade(student_list[1],subject_list[1],'B')
print(assign_grade(student_list[1],subject_list[2],'C'))
print("")

### Test case #13 : get_student_record
print("Test case #13 get_student_record")
print("Answer : {'CS101': ['Computer Programming 1', 'A'], 'CS102': ['Computer Programming 2', 'B'], 'CS103': ['Data Structure', 'C']}")
print(get_student_record(student_list[1]))
print("")

### Test case #14 : get_student_GPS
print("Test case #14 get_student_GPS")
print("Answer : 3.0")
print(get_student_GPS(student_list[1]))
