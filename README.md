# Karnataka State Police Datathon 2024
## Theme:  Police Performance and Resource Management
## 2nd Round: Prototype Development
#### Contains source code for the prototype solution developed.  

## Team: Radiant Ranger

### Owner:
- [@Ankan Bera](https://www.github.com/Ankan54)

## Description
This repository contains the source code for the prototype.  
The prototype has been designed to be run locally, but can easily be resturctured to be deployed into any cloud platform.

For the prototype, we have created the sample data using generative AI services. the generated data imitates any real life social media posts.

The code is written using python and for the database we have used locally hosted SQLite3 DB.  
The centralised dashboard for visualisation have been designed in Power BI platform.    

Additionally, Open AI services have been utilized for implementing AI based features.

To run the application please follow the below mentioned steps.  
## Installation

Download and Install:   
`python 3.9.6` https://www.python.org/downloads/release/python-396/  
`Visual Studio Code` https://code.visualstudio.com/download

Register an account in [OpenAI.com](https://www.openai.com) and create an API key.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Ankan54/ksp-hackathon-radiant-ranger
```

create virtual environment

```bash
  python -m venv venv
  ./venv/Scripts/activate.bat
```

Install dependencies

```bash
  pip install -r requirements.txt
```

go inside the src folder

```bash
  cd src
```

Start the data extraction process. database setup will happen automatically, the first time the app runs.

```bash
  python main.py
```

start the Demo Web App for checking individual data processing.
```bash
  python app.py
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SOURCE_DATA_FILE_PATH`  the full path to the ksp_hackathon_data.xlsx file inside the sample data folder
`OPENAI_API_KEY`  

