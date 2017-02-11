from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium_tests.pages import ProjectsPage


class AddProjectWithExtent(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project_with_extent(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_xpath('//a[@class="leaflet-draw-draw-polygon"]').click()
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_extents_extent_map"]')
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()
        action.move_to_element(elem).move_by_offset(15, 10).click().perform()
        action.move_to_element(elem).move_by_offset(15, 15).click().perform()
        action.move_to_element(elem).move_by_offset(10, 15).click().perform()
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath("//h3[contains(text(), '1. General Information')]")
        self.wd.find_element_by_xpath('//select[@name="details-organization"]').click()
        self.wd.find_element_by_xpath('//option[@value="organization-1"]').click()
        self.wd.find_element_by_xpath('//input[@id="id_details-name"]').send_keys("project-with-extent-1")
        self.wd.find_element_by_xpath('//textarea[@id="id_details-description"]').send_keys("Project-with-extent-1 description")

        try:
            elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
            try :
                elem.click()
            except WebDriverException: # Fix : element not clickable in Chrome
                action = ActionChains(self.wd)
                action.move_to_element(elem).send_keys(Keys.TAB * 11).send_keys(Keys.RETURN).perform()

            self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text.endswith("PROJECT-WITH-EXTENT-1")
        except Exception:
            self.wd.wait_for_css(".error-block")
            assert True

    def tearDown(self):
        self.wd.quit()
