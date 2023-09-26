# Reservation Application

The Reservation Application aims to make panel reservations based on specific IDs and provide ease of use.

## Used Technologies

This project utilizes the following technologies:

- **Flask**: A Python web framework used for developing web applications.
- **MariaDB**: A relational database system used for database management.
- **Nginx**: An open-source web server and reverse proxy used for serving web content.

Each of these technologies is employed for different aspects of the project.


## Features
- Access to the application is available through a web page.
- Reservation records can be made by entering the desired name, panel ID, and reservation duration using the "ADD" button.
- Information about the made reservation is displayed on the screen.
- When making a reservation, you can specify how many hours you want to reserve or until the end of the day, or you can leave the duration information blank to automatically reserve until the end of the day.
- In the case of a successful reservation, reservation information is sent to the Teams chat via a Webhook.
- If you enter the duration information in the wrong format or provide a past date, you will receive an error message.
- Similarly, if you try to make a reservation for a panel that appears to be unavailable or does not exist, you will receive an error message.
- When the reservation duration expires, the record is automatically deleted. You can also delete a reservation early by using the button at the end of the record.
- You can use the "SEARCH" section to see if there is a reservation record for the panel you are looking for.

## Requirements
To use the application, Docker and Docker Compose must be installed on your computer.

If Docker is installed:
sudo apt install docker-compose

Project Installation

Clone the project repository:
git clone '<project_url>'

Replace the Webhook URL address in the main.py file with the Webhook URL of the Teams channel you want.

Modify the port settings in the Docker Compose file according to the desired IP address and port number (e.g., <ip_address>:80:80). You can also replace "localhost" with an IP address in the default.conf file.

Run the following command to start the project:
docker-compose up 

Automatic Panel Addition
Panels with IDs ranging from 100 to 200 in an available state are automatically added to the database. You can update this function according to your requirements.

How to Use the Application
To use the application, go to the localhost address in your browser or use the internal IP address of your computer. For example, http://localhost or http://<ip_address>.

To run the application in the background, you can use the following command:
docker-compose up -d

If the version specified in the Docker Compose file is not supported, you should make updates based on the version supported by your computer. Similarly, if port conflicts occur when you run the docker-compose up command, you should make appropriate port changes. You can access the web page by adding the updated port number to the end of the accessed address
