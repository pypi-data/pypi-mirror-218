import concurrent.futures

parallel_threads = concurrent.futures.ThreadPoolExecutor()
parallel_processes = concurrent.futures.ProcessPoolExecutor()

def func(x):
    print(x)

# multi-threading can be launched from anywhere 
# parallel_threads.map(func, [1, 2, 3, 4, 5])  

def run_multiprocessing():
    #! any multiprocessing must be launched from a function 
    parallel_processes.map(func, [1, 2, 3, 4, 5])
    
def wait_on_multiprocessing():
    sessions = [1, 2, 3, 4, 5]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(func, sessions)
    print('Done')
    
if __name__ == "__main__":
    #! or from an if "__main__" block  such as this 
    wait_on_multiprocessing()  
    
