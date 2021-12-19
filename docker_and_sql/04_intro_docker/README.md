## Topics
- Docker
- Docker Compose
- Webserver with Docker
- Webserver and Postgres database with Docker Compose

### Docker 
Docker is a Container Manager. Containers are a form of operating system virtualization. 
Inside a container are all the necessary executables, binary code, libraries and configuration files. 
Containers do not contain operating system images themselves, which makes them lighter and more portable. 
Think of the docker as a ship full of containers. It was created to avoid that classic situation: "on my machine it worked".

## Steps
- Install Docker:
    - `sudo apt install docker.io`

- Create a folder for this project and the Dockerfile
    - `mkdir 04_intro_docker`
    - `cd 04_intro_docker`
    - `touch Dockerfile`

- Create the simple webserver files
    - `mkdir web`
    - `cd mkdir web`
    - `touch index.html`

- Fill Dockerfile
1. What image we want
In the beginning of Docker study it's very useful to use the [hub.docker.com](hub.docker.com):
![Hub Docker](/img/home_hub_docker.png)

Get the lastest version of the image
`FROM httpd`

or set a version
`FROM httpd:2.4`

2. Use `COPY` to get the content of our webserver that is in /web folder and add to the default apache directory
`COPY ./web /usr/local/apache2/htdocs/`

3. Open port
`EXPOSE 80`

Our Dockerfile it's ready. Now we need to build it.

Build an image called `web_apache` and  for this use my `Dockerfile` that is located in `04_intro_docker` folder (use `.` for indicate the current folder)

Run in the terminal:
`docker build -t web_apache .`

A successfuly output:
![Docker build](/img/create_image_output.png)

To see the images that we have in our system:
`docker image ls`

![See images](/img/see_images.png)

`docker run -d -p 80:80 web_apache`
`-d`: run in background
`-p 80:80`: links the port 80 to the port 80 of the container

The output:
![Docker run](/img/run_image_output.png)

The server is running:
![Web server](/img/web_server_on.png)

Once the server is running, we can see with `docker ps`:
![Docker ps](/img/docker_ps.png)

To stop the container:
`docker stop <container_id>`

### Docker Compose
It is a tool for defining and executing containers together. With it, it is possible to create an application development environment, such as an application server, a database, an email server, etc. Each container is defined as a configuration file, which is run by Docker Compose.

- Install Docker Compose:
    - `sudo apt install docker-compose`

- Create the yml file
    - `cd web`
    - `touch docker-compose.yml`

- Create db folder
    - `mkdir db`

- Basic configuration contains: version, services with: image, container name, environment variables, ports and volumes (maintaining the image state)

    ``` yml
    version: "3"
    services:
            db: 
                image: postgres:9.6
                container_name: pg_container
                environment:
                    - POSTGRES_USER=postgres
                    - POSTGRES_PASSWORD=postgres
                    - POSTGRES_DB=postgres
                ports: 
                    - "5432:5432"
                volumes:
                    - ./db:/var/lib/postgresql/data
    ```
- Up the containers
    - `docker-compose up -d db`

- Postgres is running:
![Postgres](/img/postgres_on.png)

- Create a table in the database
    - Install Postgres CLI
        - `sudo apt install postgresql-client`
    - Switch to postgres user
        - `sudo -u postgres psql`
    - Connect to database
        - `psql -d "host=localhost port=5432 dbname=postgres user=postgres"`
    - Create a table
        - `CREATE TABLE IF NOT EXISTS customers (id serial NOT NULL, name VARCHAR(250), age INTEGER, PRIMARY KEY (id));`
        - Table created
        ![Create table](/img/table_created.png)

- Stop Docker Compose
    - `docker-compose down`