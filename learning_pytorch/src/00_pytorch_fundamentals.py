# -*- coding: utf-8 -*-
import torch
import numpy as np

print(torch.__version__)

print("张量".center(50, "-"))
# Scalar
# torch.Tensor 是张量
scalar = torch.tensor(7)
print(scalar)

# 使用ndim属性检查张量的维数
print(scalar.ndim)

# Get the Python number within a tensor (only works with one-element tensors)
# 使用item()方法将张量转换为Python数字
print(scalar.item())

print("向量".center(50, "-"))
# Vector
# 向量
vector = torch.tensor([7, 7])
print(vector)

# 检查向量的维数
print(vector.ndim)

# 检查向量的形状
print(vector.shape)

print("矩阵".center(50, "-"))
# Matrix
#  矩阵
MATRIX = torch.tensor([[7, 8],
                       [9, 10]])
print(MATRIX)

# 检查矩阵的维数
print(MATRIX.ndim)
print(MATRIX[0])

# 检查矩阵的形状
print(MATRIX.shape)

print("三维张量".center(50, "-"))
# Tensor
# TENSOR = torch.tensor([[[1, 2, 3],
#                         [3, 6, 9],
#                         [2, 4, 5]]])
TENSOR = torch.tensor([[[1, 2, 3, 0],
                        [4, 5, 6, 0],
                        [7, 8, 9, 0]],
                       [[7, 8, 9, 0],
                        [10, 11, 12, 0],
                        [13, 14, 15, 0]]])
print(TENSOR)
print(TENSOR[0])
print(TENSOR[1])
print(TENSOR.ndim)
print(TENSOR.shape)

print("张量操作".center(50, "-"))
# Create a random tensor
# 创建一个随机张量
random_tensor = torch.rand(3, 4)
print(random_tensor)

# Create a random tensor with similar shape to an image tensor
# 创建一个与图像张量相似的随机张量
random_image_size_tensor = torch.rand(size=(224, 224, 3))
print(random_image_size_tensor.shape)
print(random_image_size_tensor.ndim)
random_image_size_tensor = torch.rand(224, 224, 3)
print(random_image_size_tensor.shape)

print("张量填充".center(50, "-"))
# Create a tensor of all zeros
# 创建一个全零张量
zeros_tensor = torch.zeros(3, 4)
print(zeros_tensor)
zeros_tensor = torch.zeros(size=(3, 4))
print(zeros_tensor)

print("张量填充".center(50, "-"))
# Create a tensor of all ones
# 创建一个全1张量
ones_tensor = torch.ones(size=(3, 4))
print(ones_tensor)
print(ones_tensor.type())
print(ones_tensor.dtype)

print("张量转换".center(50, "-"))
# Create a range of values 0 to 9
# 创建一个从0到9的数值范围
range_tensor = torch.arange(start=0, end=10, step=1)
print(range_tensor)

# Create a tensor of zeros similar to range_tensor
# 创建一个与range_tensor相似的全零张量
zeros_like_tensor = torch.zeros_like(input=range_tensor)
print(zeros_like_tensor)

# Tensor dtype
print("张量类型".center(50, "-"))
float_32_tensor = torch.tensor(
    # [1, 2, 3],
    [1.0, 2.0, 3.0],
    dtype=None,  # what type is the tensor?
    device=None,  # what device is my tensor on?
    requires_grad=False)  # do we want to track gradients with this tensor?
print(float_32_tensor)
print(float_32_tensor.dtype)
float_16_tensor = float_32_tensor.type(torch.float16)
print(float_16_tensor)
print(float_32_tensor * float_16_tensor)

int_32_tensor = torch.tensor([1, 2, 3], dtype=torch.int32)
print(int_32_tensor)
print(int_32_tensor * float_32_tensor)
notes = (
    "张量注意事项：\n",
    "1-数据类型：torch.dtype\t",
    "2-数据形状：torch.shape\t",
    "3-数据设备：torch.device")

print("".join(notes).center(50, "-"))

print("张量操作".center(50, "-"))
some_tensor = torch.rand(3, 4)
print(f"张量数据类型：{some_tensor.dtype}")
print(f"张量形状：{some_tensor.shape}")
print(f"张量形状：{some_tensor.size()}")
print(f"张量设备：{some_tensor.device}")

print("张量操作：加、减、乘、除、矩阵".center(50, "-"))
tensor = torch.tensor([1, 2, 3])
print(tensor + 10)
print(tensor - 10)
print(tensor * 10)
print(tensor / 10)
print(tensor.add(10), torch.add(tensor, 10))
print(tensor.sub(10), torch.sub(tensor, 10))
print(tensor.mul(10), torch.mul(tensor, 10))
print(tensor.div(10), torch.div(tensor, 10))

print("张量操作：矩阵".center(50, "-"))
tensor = torch.tensor([1, 2, 3])
print(f"矩阵乘法：{tensor * tensor}")
print(f"矩阵乘法：{tensor @ tensor}")
print(f"矩阵乘法：{torch.matmul(tensor, tensor)}")

notes = (
    "矩阵乘法注意事项：\n",
    "1-数据形状：前一个矩阵的形状要能和后一个矩阵的形状匹配,如(3,2) @ (2,3)\n"
)
print("".join(notes).center(50, "-"))

print("矩阵乘法".center(50, "-"))
tensor_a = torch.tensor([[1, 2],
                         [3, 4],
                         [5, 6]])
tensor_b = torch.tensor([[7, 8],
                         [9, 10],
                         [11, 12]])
print(f"矩阵B 的形状：{tensor_b.shape}")
tensor_b = tensor_b.T
print(f"矩阵B 的形状：{tensor_b.shape}")
print(f"矩阵乘法：{tensor_a @ tensor_b}")
print(f"矩阵乘法：{torch.matmul(tensor_a, tensor_b)}")
print(f"矩阵乘法：{torch.mm(tensor_a, tensor_b)}")

print("矩阵操作：min、max、mean、sum".center(50, "-"))
tensor = torch.arange(0, 100, 10)
print(f"张量：{tensor}")
print(f"张量最大值：{tensor.max()}")
print(f"张量最小值：{tensor.min()}")
# print(f"张量平均值：{tensor.mean()}")  # 均值计算需要注意数据的类型,长整型无法计算，需要转换为浮点型
print(f"张量平均值：{tensor.float().mean()}")
print(f"张量平均值：{torch.mean(tensor.type(torch.float32))}")
print(f"张量平均值：{tensor.sum()}")

print("矩阵操作：矩阵索引".center(50, "-"))
print(f"矩阵最小值索引：{tensor.argmin()}")
print(f"矩阵最大值索引：{tensor.argmax()}，最大值为：{tensor.max()}")

print("矩阵操作：矩阵形状变形--reshape,view,stack,squeeze,unsqueeze".center(50, "-"))
tensor = torch.arange(0, 100, 10)
print(f"张量：{tensor}")
print(f"张量形状：{tensor.shape}")
tensor_reshape = tensor.reshape(1, 10)
print(f"张量变形-reshape：{tensor_reshape}")
print(f"张量变形形状：{tensor_reshape.shape}")
tensor_view = tensor.view(1, 10)
print(f"张量变形-view：{tensor_view}")
print(f"张量变形形状：{tensor_view.shape}")
# tensor_view和tensor是同一个张量，内存地址相同，如果对tensor_view进行修改，tensor也会跟着修改
tensor_view[0][0] = 100
print(f"张量-view：{tensor_view}")
print(f"张量：{tensor}")
# tensor_stack = torch.stack([tensor, tensor])  # 维度默认为0
tensor_stack = torch.stack([tensor, tensor], dim=1)
print(f"张量堆叠-stack\n：{tensor_stack}")
print(f"张量堆叠形状：{tensor_stack.shape}")

print("张量操作：张量变形--squeeze,unsqueeze".center(50, "-"))
tensor_squeeze = tensor_reshape.squeeze()
print(f"张量：{tensor_reshape},  维度为：{tensor_reshape.dim()}, 形状为：{tensor_reshape.shape}")
print(f"张量变形-squeeze：{tensor_squeeze}")
print(f"张量变形形状：{tensor_squeeze.shape}， 维度为：{tensor_squeeze.dim()}")
print("squeeze是对维度为1的维度进行压缩，压缩后维度会减少".center(50, "-"))

tensor_unsqueeze = tensor_reshape.unsqueeze(dim=2)
print(f"张量：{tensor_reshape},  维度为：{tensor_reshape.dim()}, 形状为：{tensor_reshape.shape}")
print(f"张量变形-unsqueeze：{tensor_unsqueeze}")
print(f"张量变形形状：{tensor_unsqueeze.shape}， 维度为：{tensor_unsqueeze.dim()}")
print("unsqueeze是对维度为1的维度进行压缩，压缩后维度会增加".center(50, "-"))

print("张量操作：张量变形--permute".center(50, "-"))
tensor_permute = tensor_reshape.permute(1, 0)
print(f"张量：{tensor_reshape},  维度为：{tensor_reshape.dim()}, 形状为：{tensor_reshape.shape}")
print(f"张量变形-permute：{tensor_permute}")
print(f"张量变形形状：{tensor_permute.shape}， 维度为：{tensor_permute.dim()}")
print("permute是对维度进行重新排列，维度的顺序可以任意".center(50, "-"))
print("permute和原来的tensor共享内存，所以改变一个，另一个也会改变".center(50, "-"))

print("数据索引：torch.index_select".center(50, "-"))
tensor = torch.arange(1, 10).reshape(1, 3, 3)
print(f"张量：{tensor},  \n\t\t维度为：{tensor.dim()}, 形状为：{tensor.shape}")
print("0维度的张量", tensor[0])
print("1维度的张量", tensor[:, 0])  # tensor[0][0] = tensor[:, 0] = tensor[0, 0]
print("2维度的张量", tensor[:, :, 0])

print("pytorch和numpy之间的转换".center(50, "-"))
notes = (
    "numpy转tenor：torch.from_numpy(ndarray)",
    "tensor转numpy：tensor.numpy()",
)
array = np.arange(1.0, 10.0)
tensor = torch.from_numpy(array).type(torch.float32)  # numpy转为tensor时，默认类型为float64
print(f"numpy: {array}, tensor: {tensor}")
print(f"numpy类型：{array.dtype}")
array = array + 1
print(f"numpy: {array}, tensor: {tensor}")

tensor = torch.arange(1.0, 10.0)
array = tensor.numpy()  # tensor 转 numpy时，默认类型为float32
print(f"numpy: {array}, tensor: {tensor}")
print(f"numpy类型：{array.dtype}")
tensor = tensor + 1
print(f"numpy: {array}, tensor: {tensor}")  # 他们之间互相转换时，不共享内存，所以改变一个，另一个不会改变

print("随机张量".center(50, "-"))
tensor = torch.rand(3, 3)
print(f"随机张量：{tensor}")
random_tensor_A = torch.rand(3, 3)
random_tensor_B = torch.rand(3, 3)
print(f"随机张量A：{random_tensor_A}")
print(f"随机张量B：{random_tensor_B}")
print(random_tensor_A.equal(random_tensor_B))

# 随机种子是调整随机数生成器的参数，使得每次运行程序时生成的随机数相同
print("随机种子".center(50, "-"))
RANDOM_SEED = 77
torch.manual_seed(RANDOM_SEED)
random_tensor_C = torch.rand(3, 3)

torch.manual_seed(RANDOM_SEED)
random_tensor_D = torch.rand(3, 3)
print(f"随机种子C：{random_tensor_C}")
print(f"随机种子D：{random_tensor_D}")
print(random_tensor_C.equal(random_tensor_D))

print("在GPU上运行".center(50, "-"))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"设备：{device}")
print(torch.cuda.device_count())

print("在设备上运行张量".center(50, "-"))
# tensor = torch.tensor([1, 2, 3],  dtype=torch.float64, device=device)
tensor = torch.tensor([1, 2, 3])
print(f"在设备上运行张量：{tensor},  设备：{tensor.device}")
# 把张量移到GPU或者CPU
tensor_on_equilibrium = tensor.to(device)
print(f"在设备上运行张量：{tensor_on_equilibrium},  设备：{tensor_on_equilibrium.device}")

notes = (
    "如果张量在GPU上，无法将tensor转换成numpy，因为numpy只能运行在CPU上"
)
print(f"{notes}".center(50, "-"))
tensor.cpu().numpy()

print("\nExercise\n".center(50, "-"))
tensor_random = torch.rand(7, 7)
print(f"随机张量1：{tensor_random}")
tensor_random_2 = torch.rand(1, 7)
print(f"随机张量2：{tensor_random_2}")
res_mul = torch.matmul(tensor_random, tensor_random_2.T)
print(f"矩阵乘法：{res_mul}")
RANDOM_SEED = 0
torch.manual_seed(RANDOM_SEED)
tensor_random = torch.rand(2, 3, device=device)
print(f"随机张量1：{tensor_random}")
torch.manual_seed(RANDOM_SEED)
torch_random_2 = torch.rand(2, 3, device=device)
print(f"随机张量2：{tensor_random_2}")
res_mul = torch.matmul(tensor_random, torch_random_2.T)
print(f"矩阵乘法：{res_mul}")
res_max = torch.max(res_mul)
print(f"矩阵乘法最大值：{res_max}")
res_argmax = torch.argmax(res_mul)
print(f"矩阵乘法最大值索引：{res_argmax}")
res_min = torch.min(res_mul)
print(f"矩阵乘法最小值：{res_min}")
res_argmin = torch.argmin(res_mul)
print(f"矩阵乘法最小值索引：{res_argmin}")

tensor_random = torch.rand([1, 1, 1, 10])
print(f"随机张量：{tensor_random}")
print(f"随机张量形状：{tensor_random.shape}")
tensor_squeeze = tensor_random.squeeze()
print(f"张量：{tensor_squeeze}")
print(f"张量形状：{tensor_squeeze.shape}")

