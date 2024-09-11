# Django Docker Project

This is a Django project containerized using Docker.

## Features

- Django for the web application
- PostgreSQL for the database
- Docker for containerization

## Requirements

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/django-docker-project.git
    ```

2. Navigate to the project directory:

    ```bash
    cd django-docker-project
    ```

3. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Run database migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. Access the Django application at `http://localhost:8000/`.

## Additional Commands

- **Stop the containers:**

    ```bash
    docker-compose down
    ```

- **Run the Django shell:**

    ```bash
    docker-compose exec web python manage.py shell
    ```

- **Run tests:**

    ```bash
    docker-compose exec web python manage.py test
    ```

## License

[MIT License](LICENSE)
