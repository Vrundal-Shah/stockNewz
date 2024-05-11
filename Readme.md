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
- **/register**: Registration page.
- **/login**: Login page.
- **/logout**: Logout functionality.
- **/profile**: Profile settings page.

### Stock Information Blueprint:
- **/search**: Search for stocks and display results.
- **/stock/<ticker>**: Display detailed information and news about a specific stock.

## Q5: Data Storage and Retrieval from MongoDB
- **User Model**: Stores user-specific information, including a unique username, email, a password (likely hashed for security), an optional image for the profile picture, a list of saved news article IDs, and a list of favorite stock tickers.
- **News Model**: Holds detailed information about news articles, such as a headline, a content URL, a timestamp of the news article (`datetime`), a unique ID, the source of the news, an image URL, a summary of the news content, and related tags or identifiers.

## Q6: Python Package or API Usage
- **FinnHub API**: This API will be used to fetch real-time and historical stock data as well as news related to the stocks. It provides comprehensive financial data, which is crucial for users making informed investment decisions. By using this API, users can obtain up-to-date and historical data about stocks, enhancing their ability to make informed investment decisions. The integration of stock data with related news articles provides a holistic view of stock performance, which is essential for personal investment tracking and analysis.
