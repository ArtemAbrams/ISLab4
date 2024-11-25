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

    for value in mrv_domains.get(var, []):
        if is_in_domain(value, mrv_domains[var]):
            assignment[var] = value
            counter += 1
            add_to_mrv_domains(assignment, csp, var)

            if is_consistent(assignment, csp[CONSTRAINTS]):
                result = mrv_backtracking(assignment, csp)
                if result != FAILURE:
                    return result

            # Скидаємо призначення, якщо не вдалося знайти розв'язок
            assignment[var] = None
            undo(assignment, csp)

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

def is_in_domain(value, domain):
    """
    Перевіряє, чи знаходиться значення в домені змінної.

    :param value: Значення для перевірки.
    :param domain: Домен змінної.
    :return: True, якщо значення в домені, інакше False.
    """
    return value in domain

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
            if other_var.teacher == var.teacher:
                mrv_domains[other_var] = [v for v in mrv_domains[other_var] if v != assigned_value]
            if other_var.class_type == var.class_type:
                mrv_domains[other_var] = [v for v in mrv_domains[other_var] if v != assigned_value]
            if (other_var.speciality == var.speciality and
                (other_var.class_type == "lecture" or var.class_type == "lecture")):
                mrv_domains[other_var] = [v for v in mrv_domains[other_var] if v != assigned_value]

def domain_len(domain):
    """
    Повертає кількість елементів у домені.

    :param domain: Домен змінної.
    :return: Кількість непорожніх значень у домені.
    """
    return len([v for v in domain if v is not None])

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

    # Знаходимо змінну з мінімальною довжиною домену
    return min(unassigned_vars, key=lambda var: domain_len(mrv_domains[var]))

def get_counter_mrv():
    """
    Повертає кількість ітерацій алгоритму.

    :return: Лічильник ітерацій.
    """
    global counter
    return counter
