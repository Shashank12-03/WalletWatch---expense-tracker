# WalletWatch--Expense-tracker

Expense Tracker is a web application built with Django that helps users track their expenses, manage income, and gain insights into their spending habits. The application allows users to register, log in, add expenses, categorize transactions, view spending trends, and plan budgets.

Features
Expense Tracking: Users can add and categorize expenses, view their transaction history, and analyze spending patterns.
Income Management: Users can manage their income sources, track earnings, and plan budgets for better financial management.
Dashboard: The dashboard provides an overview of total expenses, today's spending, and current balance, helping users stay informed about their financial status.
Automatic Expense Integration (Future Work): Seamlessly integrate online transactions for automatic expense tracking, saving users time and effort.
Income Planner (Future Work): Plan expenses for the entire month based on projected income, enabling users to budget effectively.
Installation
To run the Expense Tracker locally, follow these steps:

Clone the repository:

bash

Copy code
git clone https://github.com/Shashank12-03/WalletWatch--Expense-tracker.git
Navigate to the project directory:

bash

Copy code
cd expense-tracker
Install dependencies:

Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory.
Add necessary environment variables like SECRET_KEY, DATABASE_URL, and EMAIL_HOST.
Run migrations:

Copy code
python manage.py migrate

Start the development server:

Copy code

python manage.py runserver

Access the application at http://localhost:8000 in your web browser.

Technologies Used
Django
Postgresql
HTML/CSS
JavaScript
Bootstrap

Contributors
Shashank Joshi
