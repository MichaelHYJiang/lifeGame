import numpy as np

def make2DArray(cols, rows):
    array = np.random.rand(rows, cols)
    array = np.array(array * 2, dtpye = 'uint8')
    return array

if __name__ == '__main__':
    grid = make2DArray(10, 10)