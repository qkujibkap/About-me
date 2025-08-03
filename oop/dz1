class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        avg_grade = self._average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {avg_grade:.1f}\n'
            f'Курсы в процессе изучения: {courses_in_progress}\n'
            f'Завершенные курсы: {finished_courses}'
        )

    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()


    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
    
    def __str__(self):
        avg_grade = self._average_grade()
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {avg_grade:.1f}'
        )    

    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'
    
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    
    
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
print(isinstance(lecturer, Mentor)) # True
print(isinstance(reviewer, Mentor)) # True
print(lecturer.courses_attached)    # []
print(reviewer.courses_attached)    # []



lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
 
student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
 
print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка
 
print(lecturer.grades)  # {'Python': [7]}  

student.courses_in_progress += ['Git']
student.finished_courses +=['Введение в программирование']

print('reviewer')
print(reviewer)
print('lecturer')
print(lecturer)
print('student')
print(student)


# Создание экземпляров
student1 = Student('Ольга', 'Алёхина', 'Ж')
student2 = Student('Максим', 'Иванов', 'М')

student1.courses_in_progress += ['Python', 'Git']
student2.courses_in_progress += ['Python', 'Java']
student1.finished_courses += ['Введение в программирование']
student2.finished_courses += ['ООП']

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Сергей', 'Сидоров')
lecturer1.courses_attached += ['Python']
lecturer2.courses_attached += ['Java']

reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Анна', 'Кузнецова')
reviewer1.courses_attached += ['Python']
reviewer2.courses_attached += ['Java']

# Оценки от reviewer'ов студентам
reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student2, 'Java', 7)

# Оценки лекторам от студентов
student1.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer1, 'Python', 9)
student2.rate_lecture(lecturer2, 'Java', 8)

print('student1')
print(student1)
print('student2')
print(student2)
print('lecturer1')
print(lecturer1)
print('lecturer2')
print(lecturer2)
print('reviewer1')
print(reviewer1)
print('reviewer2')
print(reviewer2)
print()

# Функции
def average_hw_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades += student.grades[course]
    return sum(all_grades) / len(all_grades) if all_grades else 0

def average_lecture_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades += lecturer.grades[course]
    return sum(all_grades) / len(all_grades) if all_grades else 0

print(f"Средняя оценка за ДЗ по курсу Python: {average_hw_grade([student1, student2], 'Python'):.1f}")
print(f"Средняя оценка за лекции по курсу Python: {average_lecture_grade([lecturer1, lecturer2], 'Python'):.1f}")
print(f"Средняя оценка за лекции по курсу Java: {average_lecture_grade([lecturer1, lecturer2], 'Java'):.1f}")