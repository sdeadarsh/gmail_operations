# Gmail Operations API

The Gmail Operations API is a Python-based project aimed at automating various operations related to Gmail accounts, including fetching emails, processing them, and storing them in a database. It utilizes the Gmail API provided by Google to interact with Gmail accounts programmatically.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Documentation](#documentation)
7. [Contributing](#contributing)
8. [Credits](#credits)

## Introduction

The Gmail Operations API project aims to simplify common tasks associated with managing Gmail accounts, such as fetching emails, extracting relevant information, and storing them in a database for further analysis or processing. Whether you're building a custom email analytics tool, automating email processing workflows, or integrating Gmail data into your applications, this API provides a flexible and efficient solution.

## Features

- Fetch emails from Gmail accounts using the Gmail API.
- Extract metadata and content from emails, including sender, subject, date, and message body.
- Store email data in a database for future reference or analysis.
- Support for handling various email formats and attachments.
- Automate email processing tasks based on custom rules or criteria.
- Easy integration with Django projects for seamless database management.

## Getting Started

To get started with the Gmail Operations API, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up authentication with the Gmail API.
4. Configure the database settings in the `settings.py` file according to your environment. ## for this prject i have used the default django db.sqlite3 Database
5. Run the Django migrations to create the necessary database tables.
6. Start the Django server using `python manage.py runserver`.

## Usage

Once the project is set up, you can use the provided scripts and Django views to perform various Gmail operations:

- Use the `fetch_message()` function to fetch emails from Gmail and store them in the database.
- Customize the email processing logic in the `fetch_message()` function to suit your specific requirements.
- Access the stored email data through Django's admin interface or custom views.

## Configuration

The Gmail Operations API requires the following configurations:

- Gmail API credentials: Obtain OAuth 2.0 credentials from the Google Cloud Console and save them in the `credentials.json` file.
- Database settings: Configure the database connection settings in the `settings.py` file, including the database engine, name, user, and password.

## Documentation

For detailed documentation on using the Gmail Operations API, refer to the `docs` directory or visit the project's [Google_Doc]([https://github.com/sdeadarsh/gmail_operations_api/wiki](https://developers.google.com/gmail/api/guides)).

## Contributing

Contributions to the Gmail Operations API project are welcome! To contribute, follow these steps:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure that the code passes all tests.
3. Submit a pull request with a clear description of your changes and why they are needed.

## Credits

The Gmail Operations API project relies on the following third-party libraries and resources:

- Django: Web framework for building the API backend.
- Google API Client Library: Python library for interacting with the Gmail API.
- Pandas: Data manipulation library for processing email data.
- Requests: HTTP library for making requests to external APIs.

## Here are Screenshots 

### 1. List of Data

![Image Alt text](/gmail_operations_api/gmail_script/media/demo.png "Listing of Data")

![Image Alt text](/gmail_operations_api/gmail_script/media/demo1.png "Listing of Data")


## Here is the video demonstration 

[![Watch the video](https://img.youtube.com/vi/cA7C_1_NpGw/maxresdefault.jpg)](https://www.youtube.com/watch?v=cA7C_1_NpGw)


