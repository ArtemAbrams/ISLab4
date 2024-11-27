# Імпортуємо або використовуємо клас Data з вашої моделі даних
from data_model import Data

data = Data()
classes = data.classes

# Масив чисел від 0 до 29 (кількість можливих часових слотів)
meeting_times = list(range(30))

# Константи для CSP
DOMAINS = "DOMAINS"
VARIABLES = "VARIABLES"
CONSTRAINTS = "CONSTRAINTS"
FAILURE = "FAILURE"

# Перевіряє, чи всі змінні мають значення
def is_complete(assignment):
    """
    Перевіряє, чи всі змінні у CSP мають значення.

    :param assignment: Словник призначень.
    :return: True, якщо всі змінні призначені, False інакше.
    """
    return None not in assignment.values()

# Вибирає першу непризначену змінну зі списку змінних
def select_unassigned_variable(variables, assignment):
    """
    Вибір непризначеної змінної для подальшого присвоєння.

    :param variables: Список змінних CSP.
    :param assignment: Словник призначень.
    :return: Перша змінна без значення або None.
    """
    return next((var for var in variables if assignment[var] is None), None)

# Перевіряє, чи поточне присвоєння задовольняє всі обмеження
def is_consistent(assignment, constraints):
    """
    Перевіряє, чи задовольняє поточне призначення всі обмеження.

    :param assignment: Словник призначень.
    :param constraints: Список функцій обмежень.
    :return: True, якщо всі обмеження виконуються, False інакше.
    """
    return all(not constraint(assignment) for constraint in constraints)

# Повертає список класів із призначеними значеннями
def get_assigned_variables(assignment):
    """
    Повертає список змінних, яким уже призначено значення.

    :param assignment: Словник призначень.
    :return: Список змінних із ненульовими значеннями.
    """
    return [var for var in assignment if assignment[var] is not None]

# Функції обмежень

def same_teacher(assignment):
    """
    Обмеження: викладач не може вести дві пари одночасно.

    :param assignment: Словник призначень.
    :return: True, якщо обмеження порушується, False інакше.
    """
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and i.teacher == j.teacher and assignment[i] == assignment[j]:
                return True
    return False

def same_speciality(assignment):
    """
    Обмеження: спеціальність не може мати дві лекції чи лекцію і практику одночасно.

    :param assignment: Словник призначень.
    :return: True, якщо обмеження порушується, False інакше.
    """
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and i.speciality.name == j.speciality.name and assignment[i] == assignment[j]:
                if i.class_type == "lecture" or j.class_type == "lecture":
                    return True
    return False

def groups_conflict(assignment):
    """
    Обмеження: групи не можуть мати однакові практичні заняття одночасно.

    :param assignment: Словник призначень.
    :return: True, якщо обмеження порушується, False інакше.
    """
    assigned_vars = get_assigned_variables(assignment)
    for i in assigned_vars:
        for j in assigned_vars:
            if i != j and i.class_type == j.class_type and assignment[i] == assignment[j]:
                return True
    return False

# CSP-проблема
my_csp = {
    VARIABLES: classes,
    DOMAINS: meeting_times,
    CONSTRAINTS: [same_teacher, same_speciality, groups_conflict]
}
