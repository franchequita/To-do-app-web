import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TestTodoApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        os.makedirs('screenshots', exist_ok=True)

        cls.driver = webdriver.Safari()
        cls.driver.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        
        self.driver.get("http://localhost:8000")
        self.driver.execute_script("localStorage.clear();")
        self.driver.refresh()
        time.sleep(1)

    def tearDown(self):
    
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        test_name = self._testMethodName
        filename = f"screenshots/{test_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)

    def test_01_add_task(self):
       
        input_el = self.driver.find_element(By.ID, "task-input")
        input_el.send_keys("Tarea de prueba")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")
        self.assertEqual(len(tasks), 1)

    def test_02_edit_task(self):
       
        self.driver.find_element(By.ID, "task-input").send_keys("Tarea a editar")
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[text()='Editar']").click()
        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.send_keys("Tarea editada")
        alert.accept()
        time.sleep(1)
        task_text = self.driver.find_element(By.CSS_SELECTOR, "#task-list li span").text
        self.assertEqual(task_text, "Tarea editada")

    def test_03_complete_task(self):
      
        self.driver.find_element(By.ID, "task-input").send_keys("Completar tarea")
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[text()='Completar']").click()
        time.sleep(1)
        li = self.driver.find_element(By.CSS_SELECTOR, "#task-list li")
        self.assertIn("completed", li.get_attribute("class"))

    def test_04_delete_task(self):
        
        self.driver.find_element(By.ID, "task-input").send_keys("Tarea a eliminar")
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[text()='Eliminar']").click()
        time.sleep(1)
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")
        self.assertEqual(len(tasks), 0)

    def test_05_empty_alert(self):
        
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        text = self.driver.find_element(By.ID, "alert").text
        self.assertIn("no puede estar vacía", text)

    def test_06_task_counter(self):
       
        for i in range(3):
            inp = self.driver.find_element(By.ID, "task-input")
            inp.send_keys(f"T{i+1}")
            self.driver.find_element(By.CSS_SELECTOR, "form button").click()
            time.sleep(1)
        counter = self.driver.find_element(By.ID, "task-counter").text
        self.assertIn("3", counter)

    def test_07_persistence(self):
      
        self.driver.find_element(By.ID, "task-input").send_keys("Persistencia")
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)
        tasks = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")
        self.assertEqual(len(tasks), 1)

    def test_08_drag_and_drop(self):
     
        for name in ["T1", "T2"]:
            self.driver.find_element(By.ID, "task-input").send_keys(name)
            self.driver.find_element(By.CSS_SELECTOR, "form button").click()
            time.sleep(1)
        items = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")
        source, target = items[0], items[1]
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)
        reordered = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")[0].text
        self.assertEqual(reordered, "T1")

    def test_09_responsive_layout(self):
        
        self.driver.set_window_size(375, 667)
        time.sleep(1)
        el = self.driver.find_element(By.ID, "task-input")
        self.assertTrue(el.is_displayed())

    def test_10_css_design(self):
      
        container = self.driver.find_element(By.CLASS_NAME, "container")
        radius = container.value_of_css_property("border-radius")
        self.assertIn("15px", radius)

if __name__ == "__main__":
    unittest.main(verbosity=2)
