from selenium import webdriver

from detector import get
from solver import solve

driver = webdriver.Firefox()
driver.get('https://www.epasatiempos.es/sudokus.php')
driver.set_window_size(1000, 1000)
driver.save_screenshot("sudoku.png")
grid = get("sudoku.png")
solution = solve(grid)
i = 0
for m in range(9):
    for n in range(9):
        square = driver.find_element_by_id("c" + str(i))
        square.send_keys(str(solution[m, n]))
        i += 1
python_button = driver.find_element_by_id("btCheck")
python_button.click()
driver.save_screenshot("sudokuSolved.png")
driver.execute_script('document.body.style.MozTransform = "scale(0.60)";')
driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

# driver.close()
