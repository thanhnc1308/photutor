from time import sleep, perf_counter
from threading import Thread


def task(id):
    print(f'Starting task {id}...')
    sleep(1)
    print('done')


threads = []
start_time = perf_counter()
for i in range(1, 11):
    t = Thread(target=task, args=(i,))
    threads.append(t)
    t.start()
    # t.join()
for t in threads:
    t.join()
end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
