import numpy as np 
from tensor import Tensor
from graph import draw_dot

# a = Tensor([2.])
# b = Tensor([3.])
# c = a * 3
# print(c, type(c.data), c.shape)
#draw_dot(c, filename="img/graph_inspect", inspect=True)
#draw_dot(c, filename="img/graph")

# a = Tensor.eye(3)
# b = Tensor.full((3,3),2.)
# c = a * b
# d = c.sum()
# d.backward()
# print(d)
# draw_dot(d, filename="img/graph_inspect", inspect=True)
# draw_dot(d, filename="img/graph")
# print(a)
# print(b)


# a = Tensor.full((2,2),2.)
# print(a)
# b = -a 
# loss = b.sum()
# print(b)
# print(loss)
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = Tensor.full((2, 2), 2.)
# b = [[3., 3.], [3., 3.]] + a
# loss = b.sum()
# print(a
# )
# print(b)
# print(loss)
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)


# a = Tensor(2.)
# print(a)
# print(a.shape)
# b = Tensor([3.])
# print(b)
# print(b.shape)
# c = a * b
# c.backward()
# draw_dot(c, filename="img/graph_inspect", inspect=True)
# a = Tensor.full((3,3,3),3)
# b = Tensor([[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]]])
# c = a * b
# loss = c.sum()
# print(a)
# print(b)
# print(c)
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = Tensor.full((3,3),3)
# b = 1 - a
# loss = b.sum()
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = Tensor(2.)
# b = Tensor(3.)
# loss = a * b
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = Tensor.full((3,3),3)
# b = 4 - a
# loss = b.sum()
# loss.backward()
# print(a)
# print(b)
# print(loss)
# draw_dot(loss, filename="img/graph_inspect", inspect=True)
# c = Tensor.randn(0,1,(3,3))
# d = Tensor.uniform(-1,1,(3,3))
# e = c * d
# loss = e.sum()
# loss.backward()
# print(c)
# print(d)
# print(loss)
# draw_dot(loss, filename="img/graph_inspect", inspect=True)
a = Tensor.normal(0, 1, (3,3), dtype=np.float32)
b = Tensor.uniform(-1,1,(3,3), dtype=np.float128)
c = b * a
loss = c.sum()
loss.backward()
draw_dot(loss, filename="img/graph_inspect", inspect=True)
