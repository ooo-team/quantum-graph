import test_task
import custom_task

solver = test_task.create_solver_connection()

print(test_task.solve_text_case("Третьяковская", solver))
print(test_task.solve_text_case("Охотный ряд", solver))
