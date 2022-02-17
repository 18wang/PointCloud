import os, time
from multiprocessing import Pipe, Process


# 进程函数
def func(name):
    time.sleep(1)
    print('父进程的id为:', os.getppid(), "--------", '子进程的id为:', os.getpid())


# 创建五个进程
if __name__ == '__main__':
    job = []
    for i in range(5):
        p = Process(target=func, args=(i,))
        # 把新的进程添加到列表里
        job.append(p)
        p.start()
    for i in job:
        i.join()
