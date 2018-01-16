import numpy as np
import cv2

cols = 20
rows = 20
grid = np.array([])

def make2DArray(cols, rows):
    array = np.random.rand(rows, cols)
    array = np.array(array * 2, dtype = 'uint8')
    return array

def draw(cols, rows, grid):
    MAX_WIDTH = 600
    MAX_HEIGHT = 600
    INTERVAL = 5
    MARGIN = 5
    WIDTH_EACH = min(40, (MAX_WIDTH - MARGIN * 2 + INTERVAL) / cols - INTERVAL)
    HEIGHT_EACH = min(40, (MAX_HEIGHT - MARGIN * 2 + INTERVAL) / rows - INTERVAL)
    width = cols * (WIDTH_EACH + INTERVAL) - INTERVAL + MARGIN * 2
    height = rows * (HEIGHT_EACH + INTERVAL) - INTERVAL + MARGIN * 2
    img = np.zeros((height, width), dtype = 'uint8')
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] > 0:
                startX = MARGIN + j * (WIDTH_EACH + INTERVAL)
                startY = MARGIN + i * (HEIGHT_EACH + INTERVAL)
                cv2.rectangle(img, \
                              (startX, startY), \
                              (startX + WIDTH_EACH, startY + HEIGHT_EACH), \
                              255, \
                              -1)
    return img
    
def countNeighbor(grid, x, y, cols, rows):
    sum = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) == (x, y):
                continue
            i %= rows
            j %= cols
            sum += grid[i, j]
    return sum
    
def computeNext(cols, rows, grid):
    next = np.zeros((rows, cols), dtype = 'uint8')
    for i in range(rows):
        for j in range(cols):
            # count live neighbors
            neighbors = countNeighbor(grid, i, j, cols, rows)
            #print neighbors,
            state = grid[i, j]
            if state == 0 and neighbors == 3:
                next[i][j] = 1
                #print '1',
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                next[i][j] = 0
                #print '2',
            else:
                next[i][j] = state
                #print '3',
        #print '.'
    #print '=' * 20
    return next
    
if __name__ == '__main__':
    key = 0
    grid = make2DArray(cols, rows)
    cv2.imshow('grid', draw(cols, rows, grid))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    while key != 32:
        old = grid
        grid = computeNext(cols, rows, grid)
        cv2.imshow('old', draw(cols, rows, old))
        cv2.imshow('grid', draw(cols, rows, grid))
        key = cv2.waitKey(50)
    cv2.destroyAllWindows()
