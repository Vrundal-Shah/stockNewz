# StockNewz

# Final Project Idea Description

## Q1: Description of Your Final Project Idea
Create a web application that allows users to search for and access real-time and historical stock information using the FinnHub API. This platform will enable users to track stock performance, view detailed stock data, and read news articles related to specific stocks they are interested in.

## Q2: Functionality Available to Logged-in Users Only
- **Personalized Dashboard**: Users can customize their dashboard to display information on stocks they are tracking.
- **Save Articles**: Users can save articles for later reading.

## Q3: List and Describe at Least 4 Forms
- **Registration Form**: Used to create a new user account by registering with a username, email, and password.
- **Login Form**: Allows users to log into their accounts to access personalized settings and features.
- **Stock Search Form**: Enables users to search for specific stock tickers to view relevant stock information and associated news articles.
- **Update Username Form**: Allows users to change their current username to a new one, ensuring the new username is not already in use.
- **Update Profile Pic Form**: Provides the ability for users to update their profile picture, supporting only JPG and PNG image formats.
- **Update Ticker Form**: Changes the users ticker preferences.

## Q4: Routes/Blueprints Description

### User Management Blueprint:
- **/register**: Provides a registration form and handles user registration. Redirects authenticated users to the home page.
- **/login**: Provides a login form and handles user authentication. Redirects authenticated users to their account page.
- **/logout**: Handles user logout and redirects to the home page.
- **/save_bookmark/<news_id>**: Allows authenticated users to save or unsave news articles as bookmarks.
- **/personalized_dashboard**: Displays personalized dashboard for authenticated users, showing saved news and favorite ticker information.
- **/account**: Provides forms to update username, profile picture, and save favorite tickers. Handles updates to user account settings.

### Stock Information Blueprint:
- **/**: Home page that displays a search form and handles redirection to display query results based on user input.
- **/save_news**: Saves news articles to the database, handles missing parameters, and redirects.
- **/search-results/<ticker>/<start_date>/<end_date>**: Displays search results for a specific ticker and date range, shows company financials, handles both authenticated and unauthenticated users.
- **/user/<username>**: Displays detailed user information including reviews and profile picture, handles non-existent users.


## Q5: Data Storage and Retrieval from MongoDB
- **User Model**: Stores user-specific information, including a unique username, email, a password (likely hashed for security), an optional image for the profile picture, a list of saved news article IDs, and a list of favorite stock tickers.
- **News Model**: Holds detailed information about news articles, such as a headline, a content URL, a timestamp of the news article (`datetime`), a unique ID, the source of the news, an image URL, a summary of the news content, and related tags or identifiers.

## Q6: Python Package or API Usage
- **FinnHub API**: This API will be used to fetch real-time and historical stock data as well as news related to the stocks. It provides comprehensive financial data, which is crucial for users making informed investment decisions. By using this API, users can obtain up-to-date and historical data about stocks, enhancing their ability to make informed investment decisions. The integration of stock data with related news articles provides a holistic view of stock performance, which is essential for personal investment tracking and analysis.
