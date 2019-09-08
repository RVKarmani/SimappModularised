#Web Application for generating pricing charts

This project was developed during my internship at a consulting and analytics company. 
It was designed having the following design requirements - 
- A file management and assignment capability
- Storage using PostgreSQL database
- Roles for the users of the platform - End Users, Analysts and Administrator having well defined roles
- Server-side processing for all the calculated columns generated from the input data
- The capability to apply categorical filters on the data and render analytical charts from data in-browser 
- The final application being deployable on AWS Lightsail

This project has been developed from the Flask

- Uses the new Flask methods for running the project
- The database is initialized via a flask command ```create-database``` defined in commands.py
- Database and models have been placed in models.py
- Flask-Admin views have been placed in views.py

### Initializing the database
The project has a defined module for setting up the database. Open up a CLI and run
    > flask create-database

### Running Flask
For running the application locally in your system, open up a CLI in the root of the project and run:
    > flask run
###
For showing the aggregate values for the different columns such as Price Index, Volume Index etc., the summary values need to be injected into the view. So this involves defining what Jinja template to use and suitably modify it to use the injected summary values

#### Setting up the view

```views.py``` beginning at line 60.
Setting up the different views the application shows based on the user role i.e End User, Data Analyst and Administrator with each of their views and the permissions setup in the views.py file.

#### Defining the database schema
The database schema can be setup using the create_database CLI command. As for the schema of the tables themselve, they have been defined in the models.py file itself. For the server-side processing part, some of the columns such as Price Impact, Volume Impact, Mix Impact, Acquisition and Attrition needed to be calculated. For this, the hybid property of flask is being used with the calculations for each of the columns being defined.
