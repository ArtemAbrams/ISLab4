DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

MEETING_TIMES = [
    "09:00 - 10:30",
    "10:45 - 12:15",
    "13:00 - 14:30",
    "14:45 - 16:15"
]

AUDITORIUMS = [
    ["A101", 30],
    ["A102", 40],
    ["A103", 50],
    ["B201", 60],
    ["B202", 70],
    ["B203", 80],
    ["C301", 90],
    ["C302", 100],
    ["C303", 110],
    ["D401", 120],
    ["D402", 130],
    ["D403", 140],
    ["E501", 150],
    ["E502", 160],
    ["E503", 170]
]

TEACHERS_DATA = [
    {"name": "Alexander Petrov", "subject": "Mathematics"},
    {"name": "Marina Kovalenko", "subject": "Physics"},
    {"name": "Ihor Sydorenko", "subject": "Programming"},
    {"name": "Svitlana Ivanova", "subject": "Chemistry"},
    {"name": "Andriy Shevchenko", "subject": "Biology"},
    {"name": "Olena Tkachenko", "subject": "Geography"},
    {"name": "Victor Bondar", "subject": "History"},
    {"name": "John Smith", "subject": "Computer Science"},
    {"name": "Emily Davis", "subject": "Electrical Engineering"},
    {"name": "Michael Brown", "subject": "Environmental Science"},
    {"name": "Sarah Wilson", "subject": "Astronomy"},
    {"name": "David Clark", "subject": "Philosophy"},
    {"name": "Emma Johnson", "subject": "Literature"}
]

SUBJECTS_DATA = [
    {"name": "Mathematics", "number_of_students": 100, "groups": 5, "teacher": "Alexander Petrov"},
    {"name": "Physics", "number_of_students": 80, "groups": 4, "teacher": "Marina Kovalenko"},
    {"name": "Programming", "number_of_students": 120, "groups": 6, "teacher": "Ihor Sydorenko"},
    {"name": "Chemistry", "number_of_students": 90, "groups": 3, "teacher": "Svitlana Ivanova"},
    {"name": "Biology", "number_of_students": 70, "groups": 2, "teacher": "Andriy Shevchenko"},
    {"name": "Geography", "number_of_students": 60, "groups": 2, "teacher": "Olena Tkachenko"},
    {"name": "History", "number_of_students": 110, "groups": 5, "teacher": "Victor Bondar"},
    {"name": "Computer Science", "number_of_students": 95, "groups": 4, "teacher": "John Smith"},
    {"name": "Electrical Engineering", "number_of_students": 85, "groups": 3, "teacher": "Emily Davis"},
    {"name": "Environmental Science", "number_of_students": 80, "groups": 3, "teacher": "Michael Brown"},
    {"name": "Astronomy", "number_of_students": 65, "groups": 2, "teacher": "Sarah Wilson"},
    {"name": "Philosophy", "number_of_students": 75, "groups": 3, "teacher": "David Clark"},
    {"name": "Literature", "number_of_students": 90, "groups": 4, "teacher": "Emma Johnson"}
]

SPECIALITIES_DATA = [
    {"name": "Engineering", "subjects": ["Mathematics", "Physics", "Programming", "Computer Science", "Electrical Engineering"]},
    {"name": "Natural Sciences", "subjects": ["Chemistry", "Biology", "Geography", "Environmental Science", "Astronomy"]},
    {"name": "Humanities", "subjects": ["History", "Geography", "Biology", "Philosophy", "Literature"]}
]

class Data:
    def __init__(self):
        self.days = DAYS
        self.meeting_times = MEETING_TIMES
        self.rooms = [Room(name, capacity) for name, capacity in AUDITORIUMS]
        self.subjects = self.init_subjects(SUBJECTS_DATA)
        self.teachers = self.init_teachers(TEACHERS_DATA)
        self.link_subjects_teachers()
        self.specialities = self.init_specialities(SPECIALITIES_DATA)
        self.classes = self.init_classes()

    def init_subjects(self, subjects_data):
        subjects = {}
        for data in subjects_data:
            subject = Subject(
                name=data["name"],
                number_of_students=data["number_of_students"],
                groups=data["groups"],
                teacher_name=data["teacher"]
            )
            subjects[subject.name] = subject
        return subjects

    def init_teachers(self, teachers_data):
        teachers = {}
        for data in teachers_data:
            teacher = Teacher(
                name=data["name"],
                subject_name=data["subject"]
            )
            teachers[teacher.name] = teacher
        return teachers

    def link_subjects_teachers(self):
        for subject in self.subjects.values():
            teacher_name = subject.teacher_name
            teacher = self.teachers.get(teacher_name)
            if teacher:
                subject.teacher = teacher
                teacher.subjects.append(subject)
            else:
                print(f"Teacher {teacher_name} not found for subject {subject.name}")

    def init_specialities(self, specialities_data):
        specialities = []
        for data in specialities_data:
            subjects = [self.subjects[name] for name in data["subjects"] if name in self.subjects]
            speciality = Speciality(
                name=data["name"],
                subjects=subjects
            )
            specialities.append(speciality)
        return specialities

    def init_classes(self):
        classes = []
        for speciality in self.specialities:
            for subject in speciality.subjects:
                # Створення лекції
                lecture = Event(speciality, subject, None, None, None, "lecture")
                classes.append(lecture)
                # Створення практичних занять
                for i in range(subject.groups):
                    class_type = f"Practice {i + 1}"
                    practice_class = Event(speciality, subject, None, None, None, class_type)
                    classes.append(practice_class)
        return classes

class Event:
    def __init__(self, speciality, subject, room, time, day, class_type):
        self.speciality = speciality
        self.subject = subject
        self.teacher = subject.teacher
        self.number_of_students = subject.number_of_students
        self.room = room
        self.time = time
        self.day = day
        self.class_type = class_type

    def __str__(self):
        room_name = self.room.name if self.room else "No room assigned"
        return f"{self.speciality.name}, {self.subject.name}\n{self.teacher.name}, {self.class_type}, {room_name}\n"

class Teacher:
    def __init__(self, name, subject_name):
        self.name = name
        self.subject_name = subject_name
        self.subjects = []

    def __str__(self):
        return self.name

class Subject:
    def __init__(self, name, number_of_students, groups, teacher_name):
        self.name = name
        self.number_of_students = number_of_students
        self.groups = groups
        self.teacher_name = teacher_name
        self.teacher = None

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

class Speciality:
    def __init__(self, name, subjects):
        self.name = name
        self.subjects = subjects
