from csp_initializer import *

csp = my_csp

counter = 0
var_domains = {}
degree_values = {}

# Ініціалізація порожнього присвоєння
def init_assignment_con(csp):
    global var_domains
    global counter
    counter = 0
    assignment = {}
    for var in csp[VARIABLES]:
        assignment[var] = None
        var_domains[var] = csp[DOMAINS].copy()
    return assignment

def getRoom(csp, assignment, var, value):
    rooms = data.rooms  # data.rooms - це список об'єктів Room
    rooms.sort(key=lambda room: room.capacity)  # Сортуємо аудиторії за місткістю

    for r in rooms:
        if r.capacity >= var.number_of_students:
            free = True
            for k in csp[VARIABLES]:
                if assignment[k] is not None:
                    if k.room == r and assignment[k] == value:
                        free = False
                        break
            if free:
                return r
    return None  # Якщо немає доступної аудиторії

# Основний цикл виконується, поки є невирішені змінні.
# Невирішена змінна обирається, і для кожного можливого значення виконується "поширення обмежень".
# Якщо під час спроби присвоєння значення виникає конфлікт, призначення відміняється.
def constraint_propagation(assignment, csp):
    global var_domains
    global counter
    while True:
        if is_complete(assignment):
            return assignment
        var = select_unassigned_variable(csp[VARIABLES], assignment)
        if var is None:
            return FAILURE  # Якщо немає непризначених змінних
        for value in var_domains[var]:
            if is_in_domain(var, value):
                assignment[var] = value
                add_domains(assignment, csp, var)
                if check_for_zero(assignment, csp):
                    var.room = getRoom(csp, assignment, var, value)
                    counter += 1
                    if var.room is not None and is_consistent(assignment, csp[CONSTRAINTS]):
                        break
                    else:
                        assignment[var] = None
                        var.room = None
                        undo(assignment, csp)
                else:
                    assignment[var] = None
        else:
            return FAILURE  # Якщо жодне значення не підходить
    return FAILURE

# Перевіряє, чи залишилося хоча б одне можливе значення для кожної змінної.
def check_for_zero(assignment, csp):
    global var_domains
    for var in csp[VARIABLES]:
        if assignment[var] is None and not any(var_domains[var]):
            return False
    return True

# Перевіряє, чи значення знаходиться у домені для певної змінної.
def is_in_domain(var, value):
    global var_domains
    return value in var_domains[var]

def add_domains(assignment, csp, var):
    global var_domains
    assigned_value = assignment[var]
    for i in csp[VARIABLES]:
        if assignment[i] is None and i != var:
            if i.teacher == var.teacher:
                var_domains[i] = [v for v in var_domains[i] if v != assigned_value]
            if i.class_type == var.class_type:
                var_domains[i] = [v for v in var_domains[i] if v != assigned_value]
            if i.speciality == var.speciality and (i.class_type == "lecture" or var.class_type == "lecture"):
                var_domains[i] = [v for v in var_domains[i] if v != assigned_value]

def undo(assignment, csp):
    global var_domains
    # Відновлюємо домени змінних до початкового стану
    var_domains = {var: csp[DOMAINS].copy() for var in csp[VARIABLES]}
    for var in csp[VARIABLES]:
        if assignment[var] is not None:
            add_domains(assignment, csp, var)

def get_counter_con():
    global counter
    return counter
