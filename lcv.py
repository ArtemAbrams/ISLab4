from constraint_propagation import csp
from csp_initializer import *

# Глобальні змінні
counter = 0
var_domains = {}

def init_assignment_lcv(csp):
    """
    Ініціалізація порожнього присвоєння для CSP.

    :param csp: CSP-проблема, що містить змінні, домени та обмеження.
    :return: Словник assignment з початковим станом.
    """
    global var_domains, counter
    counter = 0
    assignment = {var: None for var in csp[VARIABLES]}
    var_domains = {var: csp[DOMAINS].copy() for var in csp[VARIABLES]}
    return assignment

def getRoom(csp, assignment, var, value):
    """
    Знаходить підходящу аудиторію для заняття.

    :param csp: CSP-проблема.
    :param assignment: Поточний стан призначень.
    :param var: Змінна (пара) CSP.
    :param value: Значення для змінної (часовий слот).
    :return: Об'єкт Room або None, якщо немає доступної аудиторії.
    """
    rooms = sorted(data.rooms, key=lambda room: room.capacity)  # Сортуємо аудиторії за місткістю
    for room in rooms:
        if room.capacity >= var.number_of_students:  # Перевіряємо місткість
            if all(assignment[k] != value or k.room != room for k in csp[VARIABLES] if assignment[k] is not None):
                return room  # Повертаємо першу доступну аудиторію
    return None

def is_in_domain(var, value):
    """
    Перевіряє, чи знаходиться значення в домені змінної.

    :param var: Змінна CSP.
    :param value: Значення для перевірки.
    :return: True, якщо значення в домені, інакше False.
    """
    return value in var_domains.get(var, [])

def add_domains(assignment, csp, var):
    """
    Оновлює домени інших змінних після призначення значення.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :param var: Змінна, якій було призначено значення.
    """
    global var_domains
    assigned_value = assignment[var]
    for other_var in csp[VARIABLES]:
        if assignment[other_var] is None and other_var != var:
            if other_var.teacher == var.teacher:
                var_domains[other_var] = [v for v in var_domains[other_var] if v != assigned_value]
            if other_var.class_type == var.class_type:
                var_domains[other_var] = [v for v in var_domains[other_var] if v != assigned_value]
            if (other_var.speciality == var.speciality and
                (other_var.class_type == "lecture" or var.class_type == "lecture")):
                var_domains[other_var] = [v for v in var_domains[other_var] if v != assigned_value]

def backtracking_lcv(assignment, csp, heuristic):
    """
    Алгоритм CSP з поверненням, що використовує евристику LCV.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :param heuristic: Функція евристики для вибору змінної.
    :return: Призначення або FAILURE, якщо немає розв'язку.
    """
    global counter
    while not is_complete(assignment):
        var = heuristic(assignment)
        if var is None:
            return FAILURE  # Немає доступних змінних
        for value in var_domains.get(var, []):
            assignment[var] = value
            var.room = getRoom(csp, assignment, var, value)
            counter += 1
            if var.room is not None and is_consistent(assignment, csp[CONSTRAINTS]):
                add_domains(assignment, csp, var)  # Оновлюємо домени інших змінних
                break
            assignment[var] = None
            var.room = None
        else:
            return FAILURE  # Жодне значення не підходить
    return assignment

def lcv_heuristic(assignment):
    """
    Евристика LCV (Least Constraining Value): вибирає змінну, яка найменше обмежує інших.

    :param assignment: Поточний стан призначень.
    :return: Непризначена змінна або None.
    """
    teacher_counts = {}
    for var in csp[VARIABLES]:
        if assignment[var] is None:
            teacher = var.teacher
            teacher_counts[teacher] = teacher_counts.get(teacher, 0) + 1
    # Сортуємо змінні за кількістю залишених занять для викладачів
    unassigned_vars = [var for var in csp[VARIABLES] if assignment[var] is None]
    unassigned_vars.sort(key=lambda var: teacher_counts[var.teacher])
    return unassigned_vars[0] if unassigned_vars else None

def get_counter_lcv():
    """
    Повертає кількість ітерацій алгоритму.

    :return: Лічильник ітерацій.
    """
    global counter
    return counter
