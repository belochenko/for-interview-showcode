# analytics

The system for collecting jobs data from the https://jobs.dou.ua/ website (using Selenium).

# About

The system collects the following data about vacancies:

Category of the job (for example, "Python", "Java", etc.)
 - Job title
 - Company name
 - Location
 - Requirements
 - Additional skills
 - Duty
 
It is possible to run the system in full mode or by steps:

 - Collect links to job categories available on the website.
 - Collect links to job openings for each category.
 - Collect vacancy data using the links collected in step 2.

There are two possible destinations for storing data: `MongoDB database` and `CSV file`. Users can choose the place where they want to store temporary and final outputs of the system.

# How to install and run
1. Install dependencies into the virtual environment: `pip install -r requirements.txt`.
2. Provide the path to the WebDriver in `config.py` file (you should install webdriver first). For example, you can download WebDriver for Chrome here - https://chromedriver.chromium.org/downloads .
3. Specify the type of temporary and destination storages in config.py file (variables TEMP_STORAGE and DESTINATION). There are two possible options: mongo and csv.
4. Now the system is ready for use. To run in full mode, execute the file `run.py` or `python run.py` in terminal.
