## Python下的PCL 

### 1. 安装
使用 `.whl` 进行安装, 很久没有官方的更新; 或者使用源码编译, 较为复杂, 且环境老旧.

>几个参考链接:     
[点云处理工具——python-pcl安装教程](https://blog.csdn.net/weixin_44456692/article/details/114885727)    
[python 可视化点云工具 python-pcl](https://zhuanlan.zhihu.com/p/72116675)    


[Python-PCL官方文档](https://python-pcl-fork.readthedocs.io/en/rc_patches4/tutorial/index.html)    
官方文章给出了基本的安装教程和解释, 但是没能提供代码范例和使用规范的指导, 且同样老旧.

### 2. C++绑定

工具和方法很多很杂

https://zhuanlan.zhihu.com/p/143356193

- ctypes

- CFFI

- PyBind11     
  一个综合起来很棒的选择.

- Cython

### 3. 其他点云处理选项-Open3D

[Open3D](http://www.open3d.org/docs/release/) 是 intel 于2018年推出的一个开源3D数据处理软件, 同时提供了对 C++ 和 Python 的官方支持, 同时能够实现 Windows, Linux 和 MacOS 的跨平台应用. 一些可视化的独立软件还不太支持 Windows.    
总体上, 比 python-pcl 要好一些, 尽管功能不如 PCL 全面, 但是胜在配置方便, 对Python支持更好, 且有 Intel 背书, 跨平台和Python-C++的通用性更强, 可以考虑使用 Open3D 进行一些数据和方法实验, 然后整合到我们需要的工作中.






