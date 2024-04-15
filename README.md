# Techin510-Lab3

# Promptbase Repository

## Description

Promptbase is a simple and intuitive web application built with Streamlit, designed to store and retrieve various prompts. It utilizes a PostgreSQL database to manage prompt entries, including features to add, edit, delete, and search through prompts effectively.

## Running the Project

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Access to a PostgreSQL database

### Setup

1. Clone the repository to your local machine using `git clone` command or download the ZIP file and extract it.
2. Navigate to the project directory.

   ```bash
   cd path/to/promptbase
   ```
### Install the required Python packages:
   ```
pip install -r requirements.txt
   ```
### Create a '.env' file
 ```
DATABASE_URL=your_database_url
 ```
### Running the App
 ```
streamlit run app.py
 ```
## What I learnt from this class
#### Use of Python Dataclasses: 
The use of the dataclass from Python's standard library for creating a Prompt class simplifies the code by automatically generating special methods like __init__() and __repr__().

#### Responsive UI Elements: 
The code uses Streamlit's layout options, such as expander and columns, to organize content on the page, making the interface interactive and organized.






