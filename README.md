# Data_Collection_Pipeline

Selenium and chromedriver were used in this project to create a python script to automate a browser with the aim of obtaining and storing information. This file contains the progress and understanding made throughout the project.

### Milestone 1 & 2: Choosing the website
Our family has moved house quite often, so websites like rightmove and zoopla were not foreign to me. Initially I did choose rightmove, however due to issues I had with the website during the project (which will be discussed later) I decided to change to zoopla. This decision was made quite early in the project to prevent having to go through the headache of changing websites and HTML tags weeks into the project. Initially I downloaded geckodriver to use on firefox and ended up having to install and switch to chrome and chromedriver due to issues that were specific to using selenium on firefox.

### Milestone 3: Finding the links to each page
When creating the scraper class, the `if __name__ == '__main__'` block was added right from the beginning even though it was part of a later task in the milestone. Initially my driver and url were not in the init method and were within this block. Visiting the website provided insight as to what the functions needed to do and in which order they needed to run. Functions were created to open the website, accept cookies, then search whatever needed searching, and iterating through each page to get links to each property.

When the `accept_cookies()` function was being coded, the button on rightmove was in a pop-up which was not in another frame. Errors kept appearing using `WebDriverWait` telling that the target button was out of bounds since there was a pop-up animation that needed to finish before the button could be clicked. Although a `time.sleep()` to wait for the pop-up animation to finish would work, it would slow down the process on fast internet, and may not pause long enough and still give errors on slower internet. That is when zoopla became the website of choice for the project.


### Milestone 4: Retrieving data from each page
This milestone was all about getting the data for each property. The property links in the previous milestone were stored in a list. This list was iterated through to obtain information from each property such as the number of beds, the location etc. Also, unique IDs (UID) and UUIDs were generated for each property. Folders were created for each property using the UID as the folder name. In these folders, a data.json file would contain all the obtained information, and a folder named 'images' would be created in which all the property images would go. These would be downloaded using `urllib.request.urlretrieve()` and the src link for each image.


### Milestone 5: Documentation and testing
Unittests were created to test the functions that were causing issues when coding the scraper and a few others for robustness. At this stage, a lot of the code had to be rewritten since the json files were in an inappropriate format so could not be read from python. After this, the unittest to test if the json dictionary had all the relevant keys started working properly. For the tests which saw whether a popup had been closed, the xpath was searched for and if it could not be found the test was successful. For the test to check whether the page had changed, the expected url with the url of the current page were compared. Finally, for the test to check whether all the images had been downloaded, for a single property the number of files in the 'Images' folder was compared to the number of entries in the image list.


### Milestone 6: Scalably storing the data
Amazon Web Service (AWS) was used for its s3 and RDS services. All data.json and img.jpg files were uploaded directly from python to the s3 bucket I created at the beginning of this milestone using boto3. All the tabular data (i.e. the data.json contents) was converted into a panda dataframe and uploaded to the free tier RDS database that was also created at the beginning of this milestone. This was also done directly from python using psycopg2 and sqlalchemy. Although this data couldn't be seen in the AWS RDS database itself, pgAdmin4 was used to be able to view the tables and perform queries with the data.


### Milestone 7 & 8: Preventing rescraping, containerising and running on cloud:
A list was made which stored the UIDs of the properties which had been scraped. The UID of the current property being viewed was checked against this list and if it was already present, the scraper skipped the property. The scraper was containerised using docker for which an image was made which installed all dependecies and ran the main code. The image was pushed to docker hub to be available to be pulled. An AWS EC2 free tier instance was made and connected to on which docker was installed and the script was able to run.


### Milestone 9: Monitoring and alerting
On the EC2 instance, prometheus was set up to monitor itself, docker and the hardware via node exporter. This was done by adding jobs to the prometheus.yml file, and metric addresses to the daemon.json file. When prometheus was running successfully, expressions could be written and queried to specify what needed monitoring. Grafana was then installed on the local system, and the server was started. In the configuration, it was specified that grafana should monitor the url at which prometheus was running for the EC2 instance. On the dashboard, a panel was made to monitor the docker metrics, and another was made to monitor the OS metrics.