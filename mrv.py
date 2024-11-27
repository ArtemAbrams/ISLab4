from csp_initializer import *

# Глобальні змінні
mrv_domains = {}
counter = 0

def init_assignment_mrv(csp):
    """
    Ініціалізація порожнього присвоєння для CSP з використанням MRV.

    :param csp: CSP-проблема, що містить змінні, домени та обмеження.
    :return: Словник assignment з початковим станом.
    """
    global mrv_domains, counter
    counter = 0
    assignment = {var: None for var in csp[VARIABLES]}
    mrv_domains = {var: csp[DOMAINS].copy() for var in csp[VARIABLES]}
    return assignment

def mrv_backtracking(assignment, csp):
    """
    Алгоритм CSP з поверненням, що використовує евристику MRV.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :return: Призначення або FAILURE, якщо немає розв'язку.
    """
    global counter, mrv_domains

    if is_complete(assignment):
        return assignment

    var = find_mrv(assignment, csp)
    if var is None:
        return FAILURE

    for value in mrv_domains[var]:
        assignment[var] = value
        counter += 1
        save_domains = mrv_domains.copy()  # Збереження стану доменів для відкату
        add_to_mrv_domains(assignment, csp, var)

        if is_consistent(assignment, csp[CONSTRAINTS]):
            result = mrv_backtracking(assignment, csp)
            if result != FAILURE:
                return result

        # Відкат призначення
        assignment[var] = None
        mrv_domains = save_domains

    return FAILURE

def undo(assignment, csp):
    """
    Скидає домени змінних до початкового стану.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    """
    global mrv_domains
    mrv_domains = {var: csp[DOMAINS].copy() for var in csp[VARIABLES]}
    for assigned_var, value in assignment.items():
        if value is not None:
            add_to_mrv_domains(assignment, csp, assigned_var)

def add_to_mrv_domains(assignment, csp, var):
    """
    Оновлює домени змінних після призначення значення.

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :param var: Змінна, якій було призначено значення.
    """
    global mrv_domains
    assigned_value = assignment[var]

    for other_var in csp[VARIABLES]:
        if assignment[other_var] is None and other_var != var:
            if other_var.teacher == var.teacher or \
               other_var.class_type == var.class_type or \
               (other_var.speciality == var.speciality and
                (other_var.class_type == "lecture" or var.class_type == "lecture")):
                mrv_domains[other_var] = [
                    v for v in mrv_domains[other_var] if v != assigned_value
                ]

def find_mrv(assignment, csp):
    """
    Знаходить змінну з мінімальним залишковим доменом (MRV).

    :param assignment: Поточний стан призначень.
    :param csp: CSP-проблема.
    :return: Змінна з найменшим доменом або None.
    """
    global mrv_domains
    unassigned_vars = [var for var in csp[VARIABLES] if assignment[var] is None]
    if not unassigned_vars:
        return None

    # Знаходимо змінну з мінімальним доменом
    return min(unassigned_vars, key=lambda var: len(mrv_domains[var]))

def get_counter_mrv():
    """
    Повертає кількість ітерацій алгоритму.

    :return: Лічильник ітерацій.
    """
    global counter
    return counter

def is_complete(assignment):
    """
    Перевіряє, чи всі змінні мають значення.

    :param assignment: Словник призначень.
    :return: True, якщо всі змінні призначені, False інакше.
    """
    return None not in assignment.values()

def is_consistent(assignment, constraints):
    """
    Перевіряє, чи поточне присвоєння задовольняє всі обмеження.

    :param assignment: Словник призначень.
    :param constraints: Список функцій обмежень.
    :return: True, якщо всі обмеження виконуються, False інакше.
    """
    return all(not constraint(assignment) for constraint in constraints)
