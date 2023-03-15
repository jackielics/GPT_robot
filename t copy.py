from selenium import webdriver
import time
driver = webdriver.Chrome('D:\Codes\GPT_Robot\chromedriver.exe')

print('页面跳转后重新绑定selenium.')
time.sleep(3)
search_window = driver.current_window_handle  # 此行代码用来定位当前页面
driver.switch_to.window(search_window)
print("打印标题")
print(driver.title)