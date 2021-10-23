import pyscr_test_task
import pyscr_custom_task
import pyscr_solver_logic

solver = pyscr_solver_logic.create_solver_connection()

print(pyscr_custom_task.solve_case(solver, "Белорусская5", "Белорусская2",
                             points=["Краснопресненская", "Киевская5", "Октябрьская5", "Комсомольская5"]))
print(pyscr_custom_task.solve_case(solver, "Белорусская5",
                             points=["Краснопресненская", "Киевская5", "Октябрьская5", "Комсомольская5"]))
print(pyscr_test_task.solve_text_case(solver, "Третьяковская", "Охотный ряд"))
print(pyscr_test_task.solve_text_case(solver, "Охотный ряд"))
