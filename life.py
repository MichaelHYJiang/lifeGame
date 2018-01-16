import numpy as np

cols = 10
rows = 10
grid = np.array([])

def make2DArray(cols, rows):
    array = np.random.rand(rows, cols)
    array = np.array(array * 2, dtpye = 'uint8')
    return array

if __name__ == '__main__':
    grid = make2DArray(cols, rows)