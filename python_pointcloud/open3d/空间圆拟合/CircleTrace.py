import numpy as np


class CircleTrace():
    def __init__(self, x, y, z):
        self.PlaneMatrix = np.zeros((3, 4))
        self.Circle2DMatrix = np.zeros((3, 4))
        self.PlaneParam = np.zeros((3, 1))  # 平面方程参数系数
        self.Circle2DParam = np.zeros((3, 1))
        self.TransforMatrix = np.eye(3)
        self.InitPoint = np.array([x, y, z])
        self.Points = [[x], [y], [z]]
        self.lenght = 1
        self.angle = 0
        self.start2D = []  # 平面的起点
        self.end2D = []  # 平面的终点
        self.center2D = []  # 平面的中心
        self.center3D = []
        self.radius = None

    def AddPoints(self, x, y, z):
        """添加新的点"""
        self.Points[0].append(x)
        self.Points[1].append(y)
        self.Points[2].append(z)
        self.lenght += 1

    def SolveMatrix(self, M):
        # M是拟合矩阵 np.array类型 3行4列
        # Ax = b
        A = M[:, 0:3]
        b = M[:, 3]
        x = np.linalg.solve(A, b)
        return x

    def CalPlane(self):
        """
        计算平面参数
        :return:
        """
        if self.lenght < 3:
            return
        x = np.array(self.Points[0])
        y = np.array(self.Points[1])
        z = np.array(self.Points[2])
        f = -np.ones((self.lenght, 1))
        xx = np.matmul(x, x.transpose())
        xy = np.matmul(x, y.transpose())
        xz = np.matmul(x, z.transpose())
        yy = np.matmul(y, y.transpose())
        yz = np.matmul(y, z.transpose())
        zz = np.matmul(z, z.transpose())
        xf = np.matmul(x, f)
        xf = xf[0]
        yf = np.matmul(y, f)
        yf = yf[0]
        zf = np.matmul(z, f)
        zf = zf[0]
        self.PlaneMatrix = np.array([[xx, xy, xz, xf],
                                     [xy, yy, yz, yf],
                                     [xz, yz, zz, zf]])
        self.PlaneParam = self.SolveMatrix(self.PlaneMatrix)

    def Project2Plane(self, p):
        """
        把点投影到平面 p为输入 array型 输出也为array型
        :param p:
        :return: q 为平面上的点坐标
        """

        k = -(np.dot(self.PlaneParam, p) + 1) / np.dot(self.PlaneParam, self.PlaneParam)
        q = k * self.PlaneParam + p
        return q

    def Transformation(self):
        """
        坐标变换  M 为平面到空间的变换矩阵
        :return:
        """
        n = self.PlaneParam / np.linalg.norm(self.PlaneParam)
        p = np.array([0, 0, 0])

        m = self.Project2Plane(p) - self.Project2Plane(self.InitPoint)
        m = m / np.linalg.norm(m)
        mn = np.cross(m, n)  # m n 叉乘结果
        M = np.vstack((m, mn, n))
        self.TransforMatrix = M  # np.transpose(M)

    def CalCircle(self):
        """
        计算圆方程
        :return:
        """
        if self.lenght < 3:
            return
        self.CalPlane()
        self.Transformation()
        self.Circle2DParam = np.zeros((3, 1))
        projects = np.array(self.Points)
        projects = np.matmul(self.TransforMatrix, projects)
        self.start2D = [projects[0][0], projects[1][0]]
        self.end2D = [projects[0][self.lenght - 1], projects[1][self.lenght - 1]]
        # print("投影\n",projects)
        x, y = projects[0], projects[1]
        z = -np.ones((self.lenght, 1))
        f = x * x + y * y
        xx = np.matmul(x, x.transpose())
        xy = np.matmul(x, y.transpose())
        yy = np.matmul(y, y.transpose())
        xz, yz, zz = np.matmul(x, z), np.matmul(y, z), np.matmul(z.transpose(), z)
        xz, yz, zz = xz[0], yz[0], zz[0, 0]
        xf = np.matmul(x, f.transpose())
        yf = np.matmul(y, f.transpose())
        zf = np.matmul(f, z)
        zf = zf[0]
        self.Circle2DMatrix = np.array([[xx, xy, xz, xf],
                                        [xy, yy, yz, yf],
                                        [xz, yz, zz, zf]])
        # 计算圆方程的参数 A B C
        self.Circle2DParam = self.SolveMatrix(self.Circle2DMatrix)

    def Get2DCenterRadius(self):
        """
        获取圆方程的2D参数 a b r
        :return:
        """
        A, B, C = self.Circle2DParam[0], self.Circle2DParam[1], self.Circle2DParam[2]
        a, b = A / 2, B / 2
        r = np.sqrt(a * a + b * b - C)
        self.center2D = [a, b]
        self.radius = r
        return a, b, r

    def Get3DCenterRadiusNormal(self):
        """
        计算3D圆的圆心 半径 法向量
        :return:
        """
        # 获取2D方程参数
        self.Get2DCenterRadius()
        self.center3D = np.matmul(self.TransforMatrix.T, [*self.center2D, 0])
        print(self.center3D, self.radius)

        return self.center3D, self.radius, self.PlaneParam

    def CalAngle(self, x, y, z):
        # 求角度 一个一个输入数据 就可以得到一个一个数据的角度
        self.AddPoints(x, y, z)
        if self.lenght < 3:
            return 0
        self.CalCircle()
        self.Get2DCenterRadius()
        p0 = [self.start2D[0] - self.center2D[0], self.start2D[1] - self.center2D[1]]
        pn = [self.end2D[0] - self.center2D[0], self.end2D[1] - self.center2D[1]]
        self.angle = np.arccos(
            (p0[0] * pn[0] + p0[1] * pn[1]) / (self.radius * self.radius)) * 180 / np.pi
        self.Get3DCenterRadiusNormal()
        return self.angle


# 示例
P = [[2188.451664, -285.69591, -544.760544],
     [2188.103167, -293.84986, -562.230538],
     [2187.869931, -298.208673, -544.793633],
     [2188.263317, -289.879161, -562.268553]]

cl = CircleTrace(P[0][0], P[0][1], P[0][2])
l = len(P) - 1
for i in range(l):
    print(cl.CalAngle(P[i + 1][0], P[i + 1][1], P[i + 1][2]))

print("圆平面圆心\n", cl.center2D)
print("空间圆心\n", cl.center3D)
print("圆半径\n", cl.radius)
print("点到平面的变换矩阵\n", cl.TransforMatrix)

print(np.matmul(P, cl.TransforMatrix))
