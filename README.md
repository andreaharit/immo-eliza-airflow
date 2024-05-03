# Belgian house market, Airflow pipeline 

## Project context 📝

This is the fifth part of a project that aims to create a machine learning model to predict the selling price of houses in Belgium.

Previous stages were:

- Scrapping the data from the real state website [Immoweb](https://www.immoweb.be/) to train the model. See [repository](https://github.com/niels-demeyer/immo-eliza-scraping-scrapegoat).
- Analysing the data for business insights. See [repository](https://github.com/Yanina-Andriienko/immo-eliza-scrapeGOATS-analysis).
- Building and evaluating a ML model via regression. See [repository](https://github.com/andreaharit/05-immoeliza-ml-Andrea).
- Deploying  an API and Streamlit to get a prediction using the chosen model from the previous step (Random Forest Regression). See [repository](https://github.com/andreaharit/immo-eliza-deployment).


And now we are scheduling the webscrapping (recoded comapared to the previous steps for simplification) and machine learning pipelines into Airflow in a Docker-compose to run daily.
The scraper saves the links that were scrapped and the raw data about the houses in a dated csv file for later backup. Then it cleans the dataset and merges it into an file with the accumulated data that will be used for the model training.
The model metrics as R2, MAE, 
After that we use Streamlit to display the price prediction based on the latest trained model, and plots updated dataset in a separate Docker container.

## Table of Contents

- [Usage: Airflow](#Airflow)
- [Usage: Streamlit](#Streamlit)
- [File structure](#structure)
- [Timeline](#timeline)

## Usage 🛠

<a id="Airflow"></a>
### Airflow ⌚
</a> 

To use the ML pipeline first, make sure your Docker Engine has sufficient memory allocated.

Before running Docker make sure you prepared your enviroment:

    echo -e "AIRFLOW_UID=$(id -u)" > .env

And directories:

    mkdir -p ./logs ./plugins ./config
    
To start the Docker compose container run:

    docker compose up 

Access the Airflow web interface in your browser at http://localhost:8080 with:

- Login: airflow
- Password airflow

And activate the dag immo_pipeline at the Airflow web interface.

When you are finished working and want to clean up your environment, run:

    docker compose down --volumes --rmi all


<a id="Streamlit"></a>
### Streamlit 🖱
</a> 

This is how the app looks like:

<div style="max-height: 300px;">
    <img src="https://github.com/andreaharit/immo-eliza-deployment/blob/main/img/streamlit_example.jpg" alt="Streamlit app" style="width: auto; height: 300px;">
</div>

To run streamlit navigate to the directory:

    cd ml
    
Build the docker image with:

    docker build -t streamlit .
    
And run the container with:

    docker run -p 8501:8501 streamlit


Access the Streamlit web interface in your browser at http://localhost:8501.

<a id="structure"></a>
## File structure 🗃️

This is the general file structure of the repository:

    ├─── dags
    │   └───dag_immo_pipeline.py
    ├───ml
    │   ├───0-Resources 
    │   ├───1-Scrape
    │   ├───2-Merge
    │   ├───3-Train
    │   └───4-Predict_deploy
    ├───Dockerfile
    ├───docker-compose.yaml
    └───requirements.txt

The CSVs, model files and json with the model metrics are saved inside the 0-Resources directory.
Scrape contains the code for the scrapper.
Merge is the code for merging the latest CSV into the previous merged one.
Train contains the code to train the ML model and, finally, Predict_deploy the code for the Streamlit app.

## Timeline 📅

This project took 3 days to be completed.