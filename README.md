# mood-journal
Reflectra: A Mood Journal
Reflectra is a command-line interface (CLI) application designed to help you track your daily moods, log journal entries, and analyze mood patterns over time. This README will guide you through the setup and initial usage of Reflectra.

# Step-by-Step Installation
Clone the Repository

First, clone the Reflectra repository to your local machine:

git clone `git@github.com:moemeylane/mood-journal.git`
`cd mood-journal`
Install Dependencies

Ensure you have pipenv installed. If not, install it using pip:

`pip install pipenv`
Use pipenv to install all the project dependencies:

`pipenv install`
Activate the Virtual Environment

Before running the application, activate the virtual environment:

`pipenv shell`
Initialize the Database

Run the following command to create the necessary database tables:

`python -c "from database import Base, engine; Base.metadata.create_all(engine)"`
# Usage
# Starting the Application
To start Reflectra, run the CLI application with the following command:

`python cli.py start`
You will see a prompt with options to register or log in.

Registering a New User
Select Register by typing ;`python cli.py register`

Follow the prompts to enter your name, email, and password. You will need to confirm your password.

Logging In
Select Login by typing ;`python cli.py login`
User Registration: Create a new account with your name, email, and password.
# User Login
Log in to your existing account using your email and password.
# Creating a Journal Entry
After logging in, you can create a new journal entry by selecting the option from the menu. You will be prompted to describe your mood and any thoughts you want to record.

# Viewing Journal Entries
You can view all your past journal entries, along with the recorded moods.

# Analyzing Mood Patterns
Select the option to analyze your mood patterns. The application will display detected mood fluctuations based on your entries and prompt you for feedback on the analysis.

# Suggestions and Motivational Quotes
After creating a journal entry, Reflectra will suggest topics based on your past mood patterns and display a random motivational quote to encourage you.

# Updating and Deleting Entries
You can update or delete your existing journal entries through the menu options.