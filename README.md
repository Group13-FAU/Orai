
# Senior Design Project: Project Management Data with Django

This web application is a recommendation engine built around project management data. It combines the querying power of the [Neo4j graph database](https://neo4j.com/) with the flexibility of the [Django web framework](https://www.djangoproject.com/) using the [django-neomodel plugin](https://github.com/neo4j-contrib/django-neomodel).

## Running the Application Locally
(Note: Currently, these instructions assume that you are running this using the Windows operating system)

### Set Up the Local Environment
First, ensure that you have Python 3.9 downloaded to your device. If you don't follow the instructions on the official download page [here](https://www.python.org/downloads/). You can double check that Python was installed correctly by typing `python --version` in the command line, which should return the version of Python you installed if you added it to your path. 

The default installation of Python includes pip, the standard package manager for Python. You can ensure that this is installed and up to date by typing `py -m pip install -U pip` in the command line. 

Once you've made sure that Python and pip are installed, you can clone the repository and start setting up the environment. Using a virtual environment is best practice, as it allows you to isolate the dependencies. 

To set up a virtual environment:

 1. Install the virtualenv library using `pip install virtualenv`
 2. Navigate to project folder and run `virtualenv .`
 3. Start the virtual environment using `.\Scripts\activate`

If this was successful, you should see something like `(proj-name) C:\path\to\proj-name`. To deactivate the virtual environment, run the command `.\Scripts\deactivate`.

Now, you can add the necessary dependencies to the project. This can be done by using the requirements file:
`pip install -r requirements.txt`

The key dependencies are also listed below and can be installed individually by running `pip install <name>==<version>`:
```
Django==3.1.8 
django-neomodel==0.0.6
neo4j-driver==4.1.1
neomodel==4.0.2
djangorestframework==3.12.2
```
### Connect to the Database
Now that the application is up and running, you need to connect to the database. Running this database locally requires Neo4j Desktop, which you can download [here](https://neo4j.com/download/). 

To load the database:

 1. Download the dump file from https://drive.google.com/file/d/1NB29_JRyXT2QSpN5LEM0Cww9QIgPWLyd/view?usp=sharing
 2. Create a new project (or use the existing default project)
 3. Add a local DMBS, making sure to remember the password
 4. Click the three dots next to your newly created DBMS and open up the terminal
 5. Change to the `bin` directory using `cd bin`
 6. Load the database from the dump file by running `neo4j-admin load --from C:\path\to\projdata.dump` 
 

Now, you can start the DBMS. To connect the database to the application, open up DJangoBackend\settings.py. Find the part that says `config.DATABASE_URL` and change it so that it looks like `config.DATABASE_URL = 'bolt://neo4j:<password>@localhost:7687'`. 

Once this is done, go back to the command line and use `python manage.py runserver` to run the development server. If everything was done correctly, you should be able to go to http://127.0.0.1:8000/ to see the application. 

## Application Features

Right now, the application has a basic proof-of-concept feature that allows you to search by story title (full or partial). This search will return a page that contains the first item in the list of potential matching results. 

![Main Search Page](https://github.com/FAU-ED2Spr2021-Gr21/Project-Management-Django/blob/main/imgs/main_search.png "Main Search Page")
_________

![Search Results](https://github.com/FAU-ED2Spr2021-Gr21/Project-Management-Django/blob/main/imgs/searchresults.png "Search Results")
_________

![Example Graph](https://github.com/FAU-ED2Spr2021-Gr21/Project-Management-Django/blob/main/imgs/domain_model.png "Example Graph")
_________

Of course, this proof-of-concept is not necessarily a reflection of the final product. Future feature updates will include adding more search functionality, displaying related stories, and improving the user interface. 


## Built With

* HTML, CSS, Javascript
* [Django](https://www.djangoproject.com/)
* [Neo4j](https://neo4j.com/)
* [django-neomodel](https://github.com/neo4j-contrib/django-neomodel)

## Authors

* Angelo De Marta
* Ciara O'Neill
* Micah Brown
* Zack Inthapanya

## Acknowledgments

* The [Paradise Papers Django project](https://github.com/neo4j-examples/paradise-papers-django), which served as a model for our own application
* The Silver Logic for sponsoring this project and giving us support all the way through


