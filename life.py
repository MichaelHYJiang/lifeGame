import numpy as np
import cv2
import time
import sys

cols = 80
rows = 80
grid = np.array([])

def make2DArray(cols, rows):
    array = np.random.rand(rows, cols)
    array = np.array(array * 2, dtype = 'uint8')
    return array
    
def gliderGun(cols, rows, startX = 0, startY = 0):
    array = np.zeros((rows, cols), dtype = 'uint8')
    array[startY + 5 : startY + 7, startX + 1 : startX + 3] = 1
    array[startY + 5 : startY + 8, startX + 11] = 1
    array[(startY + 4, startY + 8), startX + 12] = 1
    array[(startY + 3, startY + 9), startX + 13 : startX + 15] = 1
    array[startY + 6, startX + 15] = 1
    array[(startY + 4, startY + 8), startX + 16] = 1
    array[startY + 5 : startY + 8, startX + 17] = 1
    array[startY + 6, startX + 18] = 1
    array[startY +3 : startY + 6, startX + 21: startX + 23] = 1
    array[(startY + 2, startY + 6), startX + 23] = 1
    array[(startY + 1, startY + 2, startY + 6, startY + 7), startX + 25] = 1
    array[startY + 3 : startY + 5, startX + 35 : startX + 37] = 1
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
            state = grid[i, j]
            if state == 0 and neighbors == 3:
                next[i][j] = 1
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                next[i][j] = 0
            else:
                next[i][j] = state
    return next
    
if __name__ == '__main__':
    key = 0
    #grid = make2DArray(cols, rows)
    grid = gliderGun(cols, rows, int(np.random.rand() * (rows - 36)), int(np.random.rand() * (cols - 10)))
    cv2.imshow('grid', draw(cols, rows, grid))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    old = grid
    cycle = 0
    MAX_CYCLE = 10
    gen = 0.0
    while key != 32:
        older = old
        old = grid
        grid = computeNext(cols, rows, grid)
        cv2.imshow('grid', draw(cols, rows, grid))
        key = cv2.waitKey(10)
        diff = abs(older - grid).sum()
        thresh = 0
        if diff <= thresh:
            cycle += 1
        else:
            cycle = 0
        gen += 1
        if key == 27 or cycle > MAX_CYCLE: # pressing esc or reaching maximum cycle times, it'll reset
            grid = make2DArray(cols, rows)
            old = grid
            t = time.localtime()
            print 'reset at %s.%s.%s %s:%s:%s' % (str(t.tm_year).zfill(4), \
                                                  str(t.tm_mon).zfill(2), \
                                                  str(t.tm_mday).zfill(2), \
                                                  str(t.tm_hour).zfill(2), \
                                                  str(t.tm_min).zfill(2), \
                                                  str(t.tm_sec).zfill(2)),
            print 'exist %d generations' % int(gen)
            gen = 0
    cv2.destroyAllWindows()
