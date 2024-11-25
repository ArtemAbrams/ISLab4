import prettytable
from constraint_propagation import *
from csp import backtracking_recursive, backtracking, init_assignment_default, get_counter_default, default_heuristic
from data_model import MEETING_TIMES
from lcv import lcv_heuristic, get_counter_lcv, init_assignment_lcv, backtracking_lcv
from mrv import get_counter_mrv, init_assignment_mrv, mrv_backtracking
import sys


class Tee:
    """
    Клас для дублювання виводу в консоль і файл.
    """
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()


def sort_result_by_days(result):
    """
    Розподіл результатів по днях тижня.

    :param result: Результати CSP (словник змінних та значень).
    :return: Список занять для кожного дня.
    """
    days = [[] for _ in range(5)]  # Понеділок - П'ятниця
    for var, value in result.items():
        day_index = value // 4
        time_slot = value % 4
        days[day_index].append((var, time_slot))
    return days


def format_schedule(day, slot):
    """
    Форматує розклад для конкретного дня та часової позиції.

    :param day: Список занять для дня.
    :param slot: Часовий слот (індекс).
    :return: Відформатований рядок з заняттями.
    """
    return "\n".join(str(var) for var, time_slot in day if time_slot == slot)


def print_schedule(schedule, days, times, headers):
    """
    Друкує розклад у вигляді таблиці.

    :param schedule: Список днів з заняттями.
    :param days: Назви днів (список).
    :param times: Список часових проміжків.
    :param headers: Заголовки таблиці.
    """
    table = prettytable.PrettyTable(headers)
    for slot_index, time in enumerate(times):
        row = [time] + [format_schedule(schedule[day_index], slot_index) for day_index in range(len(days))]
        table.add_row(row)
    print(table)


def solve_and_print_schedules():
    """
    Виконує алгоритми CSP і друкує результати у вигляді таблиць.
    """
    try:
        # Запускаємо різні підходи CSP
        result_default = backtracking(init_assignment_default(my_csp), my_csp, default_heuristic)
        print(f"Counter for default backtracking: {get_counter_default()}")

        result_rec = backtracking_recursive(init_assignment_default(my_csp), my_csp, default_heuristic)
        print(f"Counter for recursive backtracking: {get_counter_default()}")

        result_lcv = backtracking_lcv(init_assignment_lcv(my_csp), my_csp, lcv_heuristic)
        print(f"Counter for backtracking with LCV: {get_counter_lcv()}")

        result_mrv = mrv_backtracking(init_assignment_mrv(my_csp), my_csp)
        print(f"Counter for backtracking with MRV: {get_counter_mrv()}")

        result_constraint_propagation = constraint_propagation(init_assignment_con(my_csp), my_csp)
        print(f"Counter for backtracking with Constraint Propagation: {get_counter_con()}")

        # Результати останнього алгоритму
        result = result_constraint_propagation
        schedule = sort_result_by_days(result)

        # Друк розкладу
        print_schedule(
            schedule[:3],  # Понеділок, Вівторок, Середа
            ["Monday", "Tuesday", "Wednesday"],
            MEETING_TIMES,
            ["Lesson Time", "Monday", "Tuesday", "Wednesday"]
        )
        print_schedule(
            schedule[3:],  # Четвер, П'ятниця
            ["Thursday", "Friday"],
            MEETING_TIMES,
            ["Lesson Time", "Thursday", "Friday"]
        )
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # Запис результатів у файл 'schedule.txt' і одночасний вивід у консоль
    with open('schedule.txt', 'w') as f:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, f)
        try:
            solve_and_print_schedules()
        finally:
            sys.stdout = original_stdout
