# Data_Collection_Pipeline

Selenium and chromedriver are used in this project to create a python script to automate a browser with the aim of obtaining and storing information. This file contains the progress I made and my understanding throughout the project.

### Milestone 1: Choosing the website
Our family has moved house quite often, so websites like rightmove and zoopla were not foreign to me. Initially I did choose rightmove, however due to issues I had with the website during the project (which will be discussed later) I decided to change to zoopla. This decision was made quite early in the project to prevent having to go through the headache of changing websites and HTML tags weeks into the project. Whilst we're talking about changing, initially I downloaded geckodriver to use on firefox (I'm on ubuntu which has firefox by default) and ended up having to install and switch to chrome and chromedriver due to issues that were specific to using selenium on firefox.

### Milestone 2: Finding the links to each page
When creating the scraper class, I added in the `if __name__ == '__main__'` block right from the beginning even though it was part of a later task in the milestone. Initially my driver and url were not in the init method and were within this block. I visited the website to see what I would need my functions to do and in which order they needed to run. I created functions to open the website, accept cookies, then search whatever needed searching, and iterating through each page to get links to each property.

When I was coding the **accept_cookies()** function, the accept cookies button on rightmove was in a pop-up which was not in another frame. I kept getting errors using `WebDriverWait` about the button I was trying to click was out of bounds since there was a pop-up animation that needed to finish before the button could be clicked. Although I could add a `time.sleep()` to wait for the pop-up animation to finish, I didn't want to since it would slow down the process on fast internet, and may be too fast and give errors on slower internet. I decided to give zoopla a shot and it was working fine so I stuck with it.


### Milestone 3: Retrieving data from each page
This milestone was all about getting the data for each property. The property links in the previous milestone were stored in a list. This list was iterated through to obtain information from each property such as the number of beds, the location etc. Also, unique IDs (UID) and UUIDs were generated for each property. Folders were created for each property using the UID as the folder name. In these folders, a data.json file would contain all the obtained information, and a folder named 'images' would be created in which all the property images would go. These would be downloaded using `urllib.request.urlretrieve()` and the src link for each image.


### Milestone 4: Documentation and testing
I created unittests to test the functions that were causing me issues when coding the scraper and a few others for robustness. At this stage, I had to go back and rewrite a lot of my code since I had tried to format my json files to look nice while reading, but doing so meant I could not read them from python. After this the unittest to test if my json dictionary had all the relevant keys started working properly. For the tests which saw whether a popup had been closed, I simply searched if the xpath for the popup was still there or not. For the test to check whether the page had changed, I compared the expected url with the url of the current page. Finally, for the test to check whether all the images had been downloaded, for a single property I checked the number of files in the 'Images' folder to the number of entries in the image list.