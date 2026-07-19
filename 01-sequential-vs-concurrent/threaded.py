import time
import threading

def task(name, duration):
    print(f"{name} started")

    time.sleep(duration)

    print(f"{name} finished")

start_time = time.perf_counter()

thread_a = threading.Thread(target=task, args=("Task A", 2))
thread_b = threading.Thread(target=task, args=("Task B", 2))
thread_c = threading.Thread(target=task, args=("Task C", 2))


thread_a.start()
thread_b.start()
thread_c.start()

thread_a.join()
thread_b.join()
thread_c.join()

end_time = time.perf_counter()

print(f"Total execution time: {end_time-start_time:.2f} seconds")




