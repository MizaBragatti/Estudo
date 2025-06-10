import numpy as np



# Matriz 0-D
arr = np.array(42)
print(arr)
print(np.__version__)
print(type(arr))
print(arr.ndim)

# Matriz 1-D
arr = np.array([1,2,3,4,5])
print(arr)
print(arr.ndim)

# Matriz 2-D
arr = np.array([[1,2,3],[4,5,6]])
print(arr)
print(arr.ndim)

# Matriz 3-D
arr = np.array([[[1,2,3],[4,5,6]], [[1,2,3],[4,5,6]]])
print(arr)
print(arr.ndim)

arr = np.array([1,2,3,4], ndmin=5)
print(arr)
print(arr.ndim)

arr = np.array([1,2,3,4,5])
print(arr)
print(arr[1])

arr = np.array([[1,2,3],[4,5,6]])
print(arr)
print(arr[0,2])

arr = np.array([[[1,2,3],[4,5,6]], [[1,2,3],[4,5,6]]])
print(arr)
print(arr[0,0,2])

arr = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(arr)
print(arr[1,-1])

arr = np.array([1,2,3,4,5,6,7])
print(arr)
print(arr[1:5])
print(arr[4:])
print(arr[:4])
print(arr[-4:-1])
print(arr[1:5:2])
print(arr[::2])

arr = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(arr)
print(arr[1, 1:4])
print(arr[0:2, 2])
print(arr[0:2, 1:4])