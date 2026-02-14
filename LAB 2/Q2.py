class Staff:
    def __init__(self, name, staff_id, department):
        self.name = name
        self.staff_id = staff_id
        self.department = department

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Department: {self.department}")


class Teacher(Staff):
    def __init__(self, name, staff_id, department, courses, salary):
        super().__init__(name, staff_id, department)
        self.courses = courses
        self.salary = salary

    def teach(self):
        print(f"{self.name} is teaching {', '.join(self.courses)}.")

    def display_info(self):
        super().display_info()
        print(f"Courses: {', '.join(self.courses)}")
        print(f"Salary: {self.salary}")


class AdminStaff(Staff):
    def __init__(self, name, staff_id, department, role, working_hours):
        super().__init__(name, staff_id, department)
        self.role = role
        self.working_hours = working_hours

    def perform_task(self):
        print(f"{self.name} is performing administrative tasks as a {self.role}.")

    def display_info(self):
        super().display_info()
        print(f"Role: {self.role}")
        print(f"Working Hours: {self.working_hours}")


class ResearchAssistant(Staff):
    def __init__(self, name, staff_id, department, research_topic, stipend):
        super().__init__(name, staff_id, department)
        self.research_topic = research_topic
        self.stipend = stipend

    def work_on_research(self):
        print(f"{self.name} is working on research in {self.research_topic}.")

    def display_info(self):
        super().display_info()
        print(f"Research Topic: {self.research_topic}")
        print(f"Stipend: {self.stipend}")


teacher = Teacher("Ali","T101","Computer Science",["AI", "Machine Learning"],80000)

admin = AdminStaff("John","A201","Administration","Office Manager",40)

research_assistant = ResearchAssistant("Raza", "R301","Computer Science","Natural Language Processing",2000)

teacher.teach()
admin.perform_task()
research_assistant.work_on_research()

print("\n--- Staff Details ---")
teacher.display_info()
print()
admin.display_info()
print()
research_assistant.display_info()
