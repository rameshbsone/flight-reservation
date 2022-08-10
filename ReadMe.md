Context
========
    This document provides the installation steps for the Flight Reservation System Microservice which is implemented as a set of REST API endpoints hosted using a docker container. The Micro services uses an in-memory data object model to store all the relevant data structures. This means that the data structures is retained as long as the docker container is running. 

    Tech stack: Fast API, Python - Language used for API implementation, Uvicorn - Web server hosting the API endpoints, VSCode - Code editor, Docker - Micro service hosting environment

Prerequisites
=============
    Docker Desktop in Windows/ Equivalent in Linux

Steps to install
=================
    Unzip the zipfile "FlightReservation.zip"
    Open the command prompt in Windows/ terminal in other OS environments
    Verify that the "docker-compose.yml" is present in the unzipped folder
    Run the command "docker-compose up". This step installs & starts the docker container
    To verify if the docker container is created & running, use the command "docker ps"
    Open a browser and navigate to "http://localhost:2000/docs"
    API endpoints will be listed here which can be executed by clicking the links
