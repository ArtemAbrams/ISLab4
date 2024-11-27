from csp_initializer import *

csp = my_csp

# Глобальні змінні
counter = 0
var_domains = {}

# Ініціалізація порожнього присвоєння
def init_assignment_con(csp):
    global var_domains, counter
    counter = 0
    assignment = {var: None for var in csp[VARIABLES]}
    var_domains = {var: csp[DOMAINS].copy() for var in csp[VARIABLES]}
    return assignment

# Знаходження відповідної аудиторії
def get_room(csp, assignment, var, value):
    rooms = sorted(data.rooms, key=lambda room: room.capacity)  # Сортуємо за місткістю
    for room in rooms:
        if room.capacity >= var.number_of_students:
            if all(
                assignment[k] != value or k.room != room
                for k in csp[VARIABLES] if assignment[k] is not None
            ):
                return room
    return None  # Немає доступної аудиторії

# Основний алгоритм поширення обмежень
def constraint_propagation(assignment, csp):
    global counter
    while True:
        if is_complete(assignment):
            return assignment

        var = select_unassigned_variable(csp[VARIABLES], assignment)
        if var is None:
            return FAILURE  # Немає непризначених змінних

        for value in var_domains[var]:
            if is_in_domain(var, value):
                assignment[var] = value
                propagate_constraints(assignment, csp, var)

                if check_domains_not_empty():
                    var.room = get_room(csp, assignment, var, value)
                    counter += 1

                    if var.room and is_consistent(assignment, csp[CONSTRAINTS]):
                        break
                # Якщо обмеження порушені або немає доступних аудиторій
                rollback_assignment(assignment, var)
        else:
            return FAILURE  # Жодне значення не підходить
    return FAILURE

# Перевірка, чи залишилися доступні домени
def check_domains_not_empty():
    global var_domains
    return all(var_domains[var] for var in var_domains)

# Перевірка, чи значення в домені
def is_in_domain(var, value):
    global var_domains
    return value in var_domains[var]

# Поширення обмежень на домени
def propagate_constraints(assignment, csp, var):
    global var_domains
    assigned_value = assignment[var]

    for neighbor in csp[VARIABLES]:
        if assignment[neighbor] is None and neighbor != var:
            if neighbor.teacher == var.teacher:
                var_domains[neighbor] = [
                    v for v in var_domains[neighbor] if v != assigned_value
                ]
            if neighbor.class_type == var.class_type:
                var_domains[neighbor] = [
                    v for v in var_domains[neighbor] if v != assigned_value
                ]
            if (neighbor.speciality == var.speciality and
                (neighbor.class_type == "lecture" or var.class_type == "lecture")):
                var_domains[neighbor] = [
                    v for v in var_domains[neighbor] if v != assigned_value
                ]

# Відкат змін після невдалої спроби
def rollback_assignment(assignment, var):
    global var_domains
    assignment[var] = None
    var.room = None
    # Повторно ініціалізуємо домени
    var_domains = {v: csp[DOMAINS].copy() for v in csp[VARIABLES]}
    for assigned_var in csp[VARIABLES]:
        if assignment[assigned_var] is not None:
            propagate_constraints(assignment, csp, assigned_var)

# Лічильник ітерацій
def get_counter_con():
    global counter
    return counter
