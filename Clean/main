from Clean.cleaner import CleanerModel
import time


def basic_cleaner():
    model = CleanerModel(10, 8, 8, 0.90)
    max_exec_time = 15
    model.initial_time = time.time()

    for i in range(max_exec_time):
        model.step()
        print('Progreso de Limpieza:', str(round(model.porcentaje_celdas_limpias() * 100, 2)) + '%')

    print(model.total_movimiento())
    model.final_time = time.time()
    model.program_execution_time()
