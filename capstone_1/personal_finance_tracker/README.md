# Financial Tracking App

Welcome to the Financial Tracking App! This web application helps users manage their budgets, track expenses, and plan for their financial goals effectively.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Managing personal finances is a crucial aspect of modern life. The Financial Tracking App simplifies this process by providing users with tools to create budgets, track income and expenses, and set savings goals.

## Features

- **User Authentication:** Secure user authentication system to protect user data.
- **Budget Management:** Create, edit, and delete budgets to organize income and expenses.
- **Expense Tracking:** Categorize and track expenses to gain insights into spending habits.
- **Savings Goals:** Set and monitor savings goals for better financial planning.
- **Profile Management:** Users can edit their profiles, change passwords, and delete accounts.
- **Dashboard:** Overview of budgets, savings, and key financial information.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (>=3.6)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Shayne0312/School/tree/main/capstone_1/personal_finance_tracker.git
    cd personal_finance_tracker
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Populate the database:

    ```bash
    python3 seed.py
    ```

5. Start the server:

    ```bash
    flask run -p 5000
    (note: if you change the port, replace 5000 with the new port)
    ```

6. Access the app:

    - [http://localhost:5000](http://localhost:5000)
    - [http://127.0.0.1:8800](http://127.0.0.1:8800)

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Description of your changes'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [licence](licence) file for details.

## Contact

For any inquiries or feedback, please contact:

- Shayne0312
- Email: ghostmanzdayz@gmail.com.com
- GitHub: [shayne0312](https://github.com/shayne0312)