Introduction
I developed the IMDb Top 250 Movies Scraper using Python to automate the extraction of detailed information about the top 250 movies listed on IMDb. By leveraging Selenium for web automation and pyodbc for database interactions, this tool efficiently gathers comprehensive data and stores it in a SQL Server database. The primary goal is to visualize this data in Power BI, creating insightful reports such as "Movies Rating through Rating-Count," "Director Rating Count out of IMDb Rating in Top 250 Movies," "Stars Rating in Top 250 Movies through IMDb Rating," and various "Top Box Office" dashboards.
Use Case
The primary use case for this scraper is to fetch and visualize key metrics of IMDb's Top 250 movies. Specifically, I aimed to extract the following details for each movie:
•	Title
•	Year
•	Runtime
•	Movie Time
•	Description
•	Stars
•	Directors
Once extracted, this data is stored in a SQL Server database, which serves as the data source for Power BI. The visualization objectives include:
1.	Movies Rating through Rating-Count Report: Analyze the distribution of IMDb ratings against the number of ratings each movie has received.
2.	Director Rating Count out of IMDb Rating in Top 250 Movies: Assess the performance of directors based on the IMDb ratings of their movies within the Top 250 list.
3.	Stars Rating in Top 250 Movies through IMDb Rating: Evaluate the performance of actors and actresses by analyzing their movies' IMDb ratings.
4.	Top Box Office Dashboards:
o	Top Box Office Weekly Gross Out of Total Gross in Total Number of Weeks Report: Track weekly gross earnings of top movies against their total gross over multiple weeks.
o	Maximum Rating Count out of IMDb Rating in Box Office: Identify movies with the highest number of ratings in relation to their IMDb ratings within box office performances.
o	Stars Rating Count out of Total IMDb Rating in Box Office: Analyze how actors' or actresses' movies perform in terms of IMDb ratings within the box office segment.
o	Directors Rating Count out of Total IMDb Rating in Box Office: Assess directors' performance based on the IMDb ratings of their box office movies.


