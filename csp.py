from constraint_propagation import csp
from csp_initializer import VARIABLES, FAILURE, is_consistent, CONSTRAINTS, is_complete, data, DOMAINS, my_csp

# Глобальні змінні для відстеження
counter = 0
var_domains = {}

def init_assignment_default(csp):
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
        if room.capacity >= var.number_of_students:  # Перевірка місткості
            if all(assignment[k] != value or k.room != room for k in csp[VARIABLES] if assignment[k] is not None):
                return room  # Повертаємо першу доступну аудиторію
    return None

def backtracking(assignment, csp, heuristic):
    """
    Алгоритм CSP з поверненням.

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
        for value in var_domains[var]:
            assignment[var] = value
            var.room = getRoom(csp, assignment, var, value)
            counter += 1
            if var.room is not None and is_consistent(assignment, csp[CONSTRAINTS]):
                break  # Переходимо до наступної змінної
            assignment[var] = None
            var.room = None
        else:
            return FAILURE  # Жодне значення не підходить
    return assignment

def backtracking_recursive(assignment, csp, heuristic):
    """
    Рекурсивний алгоритм CSP з поверненням.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :param heuristic: Функція евристики для вибору змінної.
    :return: Призначення або FAILURE, якщо немає розв'язку.
    """
    global counter
    if is_complete(assignment):
        return assignment
    var = heuristic(assignment)
    if var is None:
        return FAILURE
    for value in var_domains[var]:
        assignment[var] = value
        var.room = getRoom(csp, assignment, var, value)
        counter += 1
        if var.room is not None and is_consistent(assignment, csp[CONSTRAINTS]):
            result = backtracking_recursive(assignment, csp, heuristic)
            if result != FAILURE:
                return result
        assignment[var] = None
        var.room = None
    return FAILURE

def get_counter_default():
    """
    Повертає кількість ітерацій алгоритму.

    :return: Лічильник ітерацій.
    """
    global counter
    return counter

def default_heuristic(assignment):
    """
    Проста евристика: вибирає першу непризначену змінну.

    :param assignment: Поточний стан призначень.
    :return: Перша непризначена змінна або None, якщо всі змінні призначені.
    """
    for var in csp[VARIABLES]:
        if assignment[var] is None:
            return var
    return None
