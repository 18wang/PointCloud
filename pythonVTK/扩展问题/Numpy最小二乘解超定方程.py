import numpy as np

a=[
[2,4],
[3,-5],
[1,2],
[2,1]
]
b=[11,3,6,7]


sourceB = [(7.585427284240723, 80.56999969482422, 15.773756980895996),
           (5.928020477294922, 62.28000259399414, 16.790550231933594),
           (5.928020477294922, 62.28000259399414, 16.790550231933594),
           (5.017560005187988, 18.18000602722168, 15.702924728393555)]

targetB = [(0.325641006231308, -5.2979230880737305, -7.01727294921875),
           (-2.119680881500244, -23.541898727416992, -8.159164428710938),
           (-2.119680881500244, -23.541898727416992, -8.159164428710938),
           (-4.523909091949463, -66.13926696777344, 7.910912990570068)]


sourceB = np.concatenate((np.asarray(sourceB), np.ones(len(sourceB)).reshape((-1, 1))),
                         axis=1)
targetB = np.concatenate((np.asarray(targetB), np.ones(len(targetB)).reshape((-1, 1))),
                         axis=1)

a =np.linalg.lstsq(sourceB, targetB, rcond=-1)
ans = a[0].T

print(ans)


"""
https://blog.csdn.net/reasonyuanrobot/article/details/91819711
https://blog.csdn.net/u011341856/article/details/107758182

"""