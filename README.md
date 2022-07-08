# Data_Collection_Pipeline

This file contains the progress I made and my understanding throughout the project.

### Milestone 1: Choosing the website
Our family has moved house quite often, so websites like rightmove and zoopla were not foreign to me. Initially I did choose rightmove, however due to issues I had with the website during the project (which will be discussed later) I decided to change to zoopla. This decision was made quite early in the project to prevent having to go through the headache of changing websites and HTML tags weeks into the project. Whilst we're talking about changing, initially I downloaded geckodriver to use on firefox (I'm on ubuntu which has firefox by default) and ended up having to install and switch to chrome and chromedriver due to issues that were specific to using selenium on firefox.

### Milestone 2: Finding the links to each page
When creating the scraper class, I added in the `if __name__ == '__main__'` block right from the beginning even though it was part of a later task in the milestone. Initially my driver and url were not in the init method and were within this block. I visited the website to see what I would need my functions to do and in which order they needed to run. This led to the following functions:

- **accept_cookies():** This is the first function that I coded and is when I decided to switch to zoopla. The accept cookies button on rightmove was in a pop-up which was not in another frame. I kept getting errors using `WebDriverWait` about the button I was trying to click was out of bounds since there was a pop-up animation that needed to finish before the button could be clicked. Although I could add a `time.sleep()` to wait for the pop-up animation to finish, I didn't want to since it would slow down the process on fast internet, and maybe be too fast and give errors on slower internet. I decided to give zoopla a shot and it was working fine so I stuck with it.

- **search_ng8():** This wouldn't work on firefox and it was a known bug which had not yet been fixed which is why I decided at this point to switch to chrome and chromedriver.

-**get_property_links():** This would get the links of all the properties on that page (25 per full page) and would store them in a list.

-**get_property_info():** This will get the information such as the price, location, number of bedrooms etc of the property, but the function hasn't been coded yet.

-**change_page():** This clicks the next page button to get the next set of property links.

-**start():** This links all of the previous functions together and adds a loop to keep clicking the next page button and finding properties until all property links have been obtained in a bigger property list.