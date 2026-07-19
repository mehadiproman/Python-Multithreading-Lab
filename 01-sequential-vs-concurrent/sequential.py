import time

def task(name, durration):
    print(f"{name} started")

    time.sleep(durration)

    print(f"{name} finished")


start_time= time.perf_counter()

task("Task A", 5)
task("Task B", 5)
task("Task c", 5)


end_time=time.perf_counter()

print(f"Total execution time: {end_time - start_time:.2f} seconds")