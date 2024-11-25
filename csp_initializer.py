# Імпортуємо або використовуємо клас Data з вашої моделі даних
from data_model import Data

data = Data()
classes = data.classes

# Масив чисел від 0 до 29 (кількість можливих часових слотів)
meeting_times = list(range(30))

DOMAINS = "DOMAINS"
VARIABLES = "VARIABLES"
CONSTRAINTS = "CONSTRAINTS"
FAILURE = "FAILURE"

# Перевіряє, чи всі змінні мають значення
def is_complete(assignment):
    return None not in assignment.values()

# Вибирає непризначену змінну зі списку змінних
def select_unassigned_variable(variables, assignment):
    for var in variables:
        if assignment[var] is None:
            return var

# Перевіряє, чи поточне присвоєння задовольняє всі обмеження
def is_consistent(assignment, constraints):
    for constraint in constraints:
        if constraint(assignment):
            return False
    return True

def equal(a, b):
    return a is not None and b is not None and a == b

# Повертає список класів, які мають призначені значення
def get_assigned_variables(assignment):
    return [var for var in assignment if assignment[var] is not None]

# Функції обмежень

# Викладач не може вести дві пари одночасно
def same_teacher(assignment):
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and equal(i.teacher, j.teacher) and assignment[i] == assignment[j]:
                return True
    return False

# Спеціальність не може мати дві лекції або лекцію та практику одночасно
def same_speciality(assignment):
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and equal(i.speciality.name, j.speciality.name) and assignment[i] == assignment[j]:
                if i.class_type == "lecture" or j.class_type == "lecture":
                    return True
    return False

# Групи не можуть мати однакові практичні заняття одночасно
def groups_conflict(assignment):
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and equal(i.class_type, j.class_type) and assignment[i] == assignment[j]:
                return True
    return False

my_csp = {
    VARIABLES: classes,
    DOMAINS: meeting_times,
    CONSTRAINTS: [same_teacher, same_speciality, groups_conflict]
}
