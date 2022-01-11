



import os
from multiprocessing import Pool


def safe_readline(f):
    pos = f.tell()
    while True:
        try:
            return f.readline()
        except UnicodeDecodeError:
            pos -= 1
            f.seek(pos)


def async_kd_tokenizer(filename, worker_id, num_workers):
    with open(filename, 'r') as f:
        size = os.fstat(f.fileno()).st_size  # 指针操作，所以无视文件大小
        print(f'size {size}')
        chunk_size = size // num_workers
        offset = worker_id * chunk_size
        end = offset + chunk_size
        f.seek(offset)
        print(f'offset {offset}')
        if offset > 0:
            safe_readline(f)  # drop first incomplete line
        lines = []
        line = f.readline()
        while line:
            line = line.replace(" ", '').replace("\n", '')
            if not line:
                line = f.readline()
                continue
            lines.append(line)
            if f.tell() > end:
                break
            line = f.readline()
    return lines


def encode_file(path, workers=4):
    assert os.path.exists(path)
    results = []
    workers_thread = []
    pool = Pool(processes=workers)

    params = [[path, i, workers] for i in range(workers)]
    iw = pool.imap(async_kd_tokenizer, params)


    for w in range(workers):
        print(next(iw))
        # result = w
        # results += result.get(timeout=100)
    return results

# https://blog.csdn.net/weixin_43922901/article/details/109072215
# https://www.liujiangblog.com/course/python/79
# https://docs.python.org/zh-cn/3/library/multiprocessing.html

# '/home/aboo/PycharmProjects/data/曲面6-2.txt'
results = encode_file('../ProjectSrc/pz.txt', workers=4)
print(results)





# import open3d as o3d
# import numpy as np
# import time
# from timeit import default_timer as timer
#
#
#
# file_name = "/home/aboo/PycharmProjects/data/曲面6-2.txt"
#
#
#
# import pandas as pd
#
# start = time.time()
# read_csv_data = pd.read_csv(file_name, header=None, na_filter=False,
#                             delim_whitespace=True)
# print(time.time() - start)
#
#
#
# start = time.time()
# trans_data = read_csv_data.to_numpy().reshape([-1,3])
# print(time.time() - start)
#
# print(trans_data[:10])
#
#
# from multiprocessing import Pool
# import os
# def csv_reader(filename):
#     data = pd.read_csv(filename, header=None,na_filter=False,delim_whitespace=True)
#     return data.to_numpy()
#
# start = time.time()
# cores = os.cpu_count()
# pool = Pool(cores)
# data_list = pool.map(csv_reader, file_name)
# print(time.time() - start)
