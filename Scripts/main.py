import test_task
import custom_task

solver = test_task.create_solver_connection()

print(custom_task.solve_case(solver, "Белорусская5", "Белорусская2", ["Краснопресненская", "Киевская5", "Октябрьская5", "Комсомольская5"]))
#print(test_task.solve_text_case(solver, "Третьяковская", end="Охотный ряд"))
#print(test_task.solve_text_case(solver, "Охотный ряд"))
