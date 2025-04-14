# How to Replicate the Data

All of the neccessary scripts to scrape the data are contained within the folder "web_scrape_code"

Please run the files in this order:
1) batting_web_scraping_code.py
2) batting_nationality_scrape.py
3) bowling_web_scraping_code.py
4) bowling_nationality_scrape.py

It is important to leave a minimum of 30 minutes between running these scripts, as the source website may temporarily IP ban the terminal, and therefore the code will not work. In the event of an IP ban, it typically is lifted after 45 minutes, and then you will need to re-run the file during which the ban occured. 

You can check whether each file has successfully downloaded by checking in the folder "scraped_data", which is where the csv files are stored.

After scraping all of the data using the code contained in those files, you will need to run "data_cleaning.py", which is containd in the main directory. This file will merge all of the scraped data into one csv file named "ilt20_final_player_statistics_2025.csv" which is also saved in the main directory, and then edit perform other tasks such as renaming column headers and dropping redundant columns.

The file "ilt20_data_analysis.ipynb" contains all of the code which was used in the creation of the blog post, such as making the graphs.


