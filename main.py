from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from detector import get

driver = webdriver.Firefox()
driver.get('https://www.epasatiempos.es/sudokus.php')
driver.set_window_size(1000, 1000)
driver.save_screenshot("sudoku.png")
grid = get("sudoku.png")
print(grid)

i = 0
for m in range(9):
    for n in range(9):
        square = driver.find_element_by_id("c" + str(i))
        square.send_keys(str(grid[m, n]))
        i += 1
python_button = driver.find_element_by_id("btCheck")
python_button.click()

# driver.close()
