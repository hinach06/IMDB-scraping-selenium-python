import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import pyodbc
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def scrape_imdb_top_250():
    url = 'https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht'
    
    # Set up the Chrome WebDriver using WebDriver Manager
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    
    # Click the button to trigger the detailed view
    try:
        # Locate the button by ID and click it
        button = driver.find_element(By.ID, 'list-view-option-detailed')
        button.click()
        time.sleep(2)  # Wait for the page to load the detailed view
    except Exception as e:
        print(f"Error clicking the button: {e}")

    # Find all movies listed in the Top 250 table
    movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__c')

    movie_list = []

    for movie in movies:
        # Extract title
        title_column = movie.find_element(By.CLASS_NAME, 'ipc-title__text')
        full_title = title_column.text.strip()

        # Check if the title contains a period before splitting
        if '.' in full_title:
            title = full_title.split('.', 1)[1].strip()
        else:
            title = full_title  # If no period, use the entire title
                
        # Extract IMDb rating
        imdb_rating = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--rating').text.strip()
        imdb_rating = float(imdb_rating) if imdb_rating else None
        
        # Weekly Gross (assuming it's the first occurrence)
        Weekly_Gross = movie.find_element(By.XPATH, '(.//span[contains(@class, "sc-8f57e62c-2") and (contains(text(), "$") or contains(text(), "M"))])[1]').text.strip() if movie.find_elements(By.XPATH, '(.//span[contains(@class, "sc-8f57e62c-2") and (contains(text(), "$") or contains(text(), "M"))])[1]') else 'N/A'
        

        # Total Gross (assuming it's the second occurrence)
        Total_Gross = movie.find_element(By.XPATH, '(.//span[contains(@class, "sc-8f57e62c-2") and (contains(text(), "$") or contains(text(), "M"))])[2]').text.strip() if movie.find_elements(By.XPATH, '(.//span[contains(@class, "sc-8f57e62c-2") and (contains(text(), "$") or contains(text(), "M"))])[2]') else 'N/A'        
        
        # Locate the ul tag with class 'sc-8f57e62c-0', then target the 3rd li inside it
        li_element = movie.find_element(By.XPATH, '(.//ul[contains(@class, "sc-8f57e62c-0")]/li[3])')

        # Within that li, target the span with class 'sc-8f57e62c-2 ftiqYS'
        week_release_text = li_element.find_element(By.XPATH, './/span[contains(@class, "sc-8f57e62c-2 ftiqYS")]').text.strip()

        # Convert the extracted text to an integer if it's a valid number
        Weeks_Release = None if not week_release_text.isdigit() else int(week_release_text)
        
        # Extract rating count
        rating_count = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-rating-star--voteCount') else 'N/A'

        # Extract description
        description = movie.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div') else 'N/A'

        # Extract director
        director = movie.find_element(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-director-item"]').text.strip() if movie.find_element(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-director-item"]') else 'N/A'

        # Extract starring 
        stars = [star.text.strip() for star in movie.find_elements(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-cast-item"]')]
        
        # Extract image URL
        image_url = 'N/A'
        try:
            image_element = movie.find_element(By.XPATH, './/div/img[@class="ipc-image"]')
            image_url = image_element.get_attribute('src')  # Extract the 'src' attribute from the image tag

            # Validate image URL (you can add more sophisticated validation if needed)
            if image_url is None or image_url.strip() == '':
                image_url = 'N/A'  # Assign 'N/A' if the image URL is missing or invalid
        except:
            pass  # Assign 'N/A' if the image element is not found

        # Append the scraped data to the movie list
        movie_list.append({
            'Title': title,
            'Weekend Gross': Weekly_Gross,
            'Total Gross': Total_Gross,
            'Week Release': Weeks_Release,
            'IMDb Rating': imdb_rating,
            'Rating Count': rating_count,
            'Description': description,
            'Director': director,
            'Stars': ", ".join(stars),
            'Poster': image_url
        })

    driver.quit()

    return movie_list


# # Function to insert data into SQL Server
def insert_into_database(movies):
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-9KTVBNA;'  # my sql server name
        'DATABASE=IMDBMOVIES;'  # my sql database name
        'UID=sa;'
        'PWD=nainach'
    )
    
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(''' 
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IMDB_Top_BoxOffice_Movies ' AND xtype='U')
    BEGIN
        CREATE TABLE IMDB_Top_BoxOffice_Movies  (
            id INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing primary key
            Title NVARCHAR(255) NOT NULL,      -- Title of the movie
            Weekly_Gross NVARCHAR(10),               -- Weekend Gross
            Total_Gross NVARCHAR(10),               -- Total Gross
            Weeks_Release INT,                      -- INT VALUES
            IMDB_Rating FLOAT,                  -- IMDb rating
            Rating_Count NVARCHAR(20),          -- Rating count (e.g., "2.9M")
            Description VARCHAR(255),          -- Description of the movie
            Director VARCHAR(255),             -- Director of the movie
            Stars VARCHAR(255),                -- Comma-separated list of stars
            PosterURL NVARCHAR(MAX)            -- Image URL   
        )
    END
    ''')

    # Insert data into the table
    for movie in movies:
        cursor.execute('''
            INSERT INTO IMDB_Top_BoxOffice_Movies (Title, Weekly_Gross, Total_Gross, Weeks_Release, IMDB_Rating, Rating_Count, Description, Director, Stars, PosterURL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        movie['Title'], 
        movie['Weekend Gross'],
        movie['Total Gross'],
        movie['Week Release'],    
        movie['IMDb Rating'], 
        movie['Rating Count'], 
        movie['Description'], 
        movie['Director'], 
        movie['Stars'],
        movie['Poster']
    )
    connection.commit()
    cursor.close()
    connection.close()

# Main function
if __name__ == '__main__':
    # Scrape the data
    movies = scrape_imdb_top_250()
    
    if movies:
        print(f"Scraped {len(movies)} Top Box Movies successfully!")
        
        # Insert the scraped data into SQL Server
        insert_into_database(movies)
    else:
        print("No data scraped.")
