# Quick Pay

---
Demo Finance Web app.

## Stack & Technologies
* Python
* Django Rest Framework
* SimpleJWT authentication
* HTML
* CSS
* JavaScript

--- 

## Installation

* Clone the repo
* open repo in command line
* create a virtual environment
	```bash
		# For linux and MacOS devices run the below command
		$ python3 -m venv venv

		# For windows
		$ python -m venv venv
	```
* Activate Virtual Environment
	```bash
		# For Linux and MacOS
		$ source vemv/bin/activate

		# For windows
		$ .\venv\Scripts\activate.bat
	```
* Install Requirements
	```bash
		$ pip install -r requirements.txt
	```
* create Credentials file
	create a file named `credentials.json` with the below format
	```json
	{
		"security_key": "random-security-key"
	}
	```
* Run Migrations
	```bash
		$ python manage.py makemigrations

		$ python manage.py migrate
	```

* Runserver
	```bash
		$ python manage.py runserver
	```

* Run HTTP-SERVER for frontend
	open the repo in a new cmd window
	```bash
		$ cd frontend

		# For Linux and MacOS
		$ python3 -m http.server 9000

		# For Windows
		$ python -m http.server 9000

	```

* Done - Now visit localhost:9000 in your browser
