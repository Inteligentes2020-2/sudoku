from selenium import webdriver

from detector import get

driver = webdriver.Firefox()
driver.get('https://www.epasatiempos.es/sudokus.php')
driver.set_window_size(1000, 1000)
driver.save_screenshot("sudoku.png")
grid = get("sudoku.png")
print(grid)


driver.close()
