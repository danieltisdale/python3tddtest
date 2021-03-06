from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
	
	def test_can_start_a_list_for_one_user(self):
		# Daniel has heard about a cool new online to-do app. He goes
		# to check out its homepage
		self.browser.get(self.live_server_url)

		# He notices the page title and header mention to-do lists
		self.assertIn ('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# He is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

		# He types "Buy apples" into a text box (Daniel's hobby
		# is cooking)
		inputbox.send_keys('Buy apples')

		# When he hits enter, the page updates, and now the page lists
		# "1: Buy apples" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy apples')

		# There is still a text box inviting him to add another item. He
		# enters "Use apples to make an applie pie"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on his list
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy apples')

		# Daniel wonders whether the site will remember his list. Then he sees
		# that the site has generated a unique URL for him -- there is some
		# explanatory text to that effect.

		# He visits that URL - his to-do list is still there.

		# Satisfied, he goes back to sleep

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Daniel starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#He notices that his list has a unique URL
		daniel_list_url = self.browser.current_url
		self.assertRegex(daniel_list_url, '/lists/.+')

		# Now a new user, Elise, comes to the site

		## We use a new browser session to make sure that no information
		## of Daniel's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()
		# Elise visits the home page. There's no sign of Daniel's
		# list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Elise starts a new list by entering a new item. She
		# is less interesting than Daniel...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Elise gets his own unique URL
		elise_list_url = self.browser.current_url
		self.assertRegex(elise_list_url, '/lists/.+')
		self.assertNotEqual(elise_list_url, daniel_list_url)

		# Again, there is no trace of Daniel's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfied, they both go back to sleep