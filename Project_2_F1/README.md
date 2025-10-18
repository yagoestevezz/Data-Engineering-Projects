# Lab practice 2 : F1 data analisys
## Group 6:
* Yago Estévez Figueiras
* Andrea Real Blanco
* Francisco Manuel Vázquez Fernández

This project had been developed for the "Data engieneering" course from the "Master en Intelixencia Artificial" USC, UDC, UVigo, 2025-2026.
The main goal is to make a dimensional modelling and the full ETL process  and visualization of the data from a F1 database available at 
 the following URL:  
https://www.kaggle.com/code/kevinkwan/formula-1-pit-stops-analysis/input  
Our anaslisys surround 3 key aspects: performance in qualifying, pit-stop eficiency and the results from each race.

## Get Started
Follow this steps in order to run the project on your local enviroment.

### Software requirements:

* DBMS: MySQL Server and MySQL workbench.
* ETL and pipeline: Python 3.x ( A jupyter notebook ".ipynb" is provided with the main script and functions).
* The following libraries  must be installed prior to running the pipeline: (numpy, matplolib, pandas and mysqlalchemy).
* Visualization : Tableau Desktop or Tableau Public.

### Setup:

1.  **Download the project .zip:**
  
2.  **Start the database:**
    * Open MySQL Workbench and connect to your db local server.
    * Execute the "create_database_f1.sql " file to create all the schemas and dimensions needed.
     
3.  ** Python jupyter notebook:**
    * Open the "pipeline.ipynb" file. 
      
### Run the code:
Once you have finisshed the setup you will be able to run the pipeline and populate the databse.
