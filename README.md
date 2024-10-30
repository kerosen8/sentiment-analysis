## Description

This project is a Flask-based web application that analyzes the sentiment of user-provided text.

## Built with
* Python (NLTK, transformers, PyTorch)
* Flask
* Pure JavaScript
* Docker
* Nginx

## Installation

Skip steps 2-4 for Docker usage.

1. Clone the project into your working directory

   ```sh
   git clone https://github.com/kerosen8/sentiment-analysis.git
   ```
2. Create Python's virtual environment, f.e.:
   ```sh
   python -m venv name_of_venv_for_this_project
   ```
3. Activate a virtual environment:
   * for Windows
   ```sh
   name_of_venv_for_this_project\Scripts\activate
   ```
   * for Ubuntu
   ```sh
   source name_of_venv_for_this_project/bin/activate
   ```
4. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

## Usage

#### Without Docker
To start a project, go to the project/src/ directory and type following command:
```sh
gunicorn app.wsgi:app --bind 127.0.0.1:port
```
now it is accessible at the address localhost:port.

#### With Docker
Go to root directory and type following command to start docker containers:
```sh
docker-compose up --build
```
now it is available on port 8080 (make sure that this port is not occupied).

For stopping (from a root directory):
 ```sh
docker-compose down
```

#### ATTENTION!
In both cases, time is needed to install the Hugging Face library (500 MB), during which the server will be unavailable. In the case of a local installation, this is done once, and the library is cached.

## Preview
![изображение](https://github.com/user-attachments/assets/6230c41b-2554-4588-9a47-c86ff72fd5ec)![изображение](https://github.com/user-attachments/assets/877717d5-c641-461f-a780-718e21dc6c97)


## Features
* Every review that is not rated as neutral is saved in a CSV file for the possibility of further training the model.

