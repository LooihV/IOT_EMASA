# API-REST EMASA Dockerization

## Installation and Deployment Guide

Software Version: 1.0 | Date: 08 may 2025

## Installation and Deployment Guide information

The purpose of this document is to provide the System Administrator or any other technical stakeholder with a complete and easy to follow guide designed specifically for the Technical Domain. It is intended to provide installation instructions to any stakeholder that has an interest or a role in the project.

### Document Responsibilities

The Installation and Deployment Guide is first created in the Deployment process step. Responsibilities for document creation and content are shown in the [RACI](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix) chart below:


| **Group Manager** | **Project Manager** | **Technical Lead** | **Business Analyst** | **Developer** | **Testing Analyst** |
| --- | --- | --- | --- | --- | --- |
| I | A | R | I | C | I |

### Combining or Splitting Documents

Documentation required by the process may be physically combined into fewer documents or split up into more documents in any way which makes sense to the project provided that all topics required by all the standard templates are present.

If information is split across several documents, all related documents shall be included in the reviews and sign off. For example, when installation and deployment instructions are in separate documents, the documents shall undergo the same preparation, review, and approval activities as well as review to ensure consistency of technical information among the component documents.

### Reviews

The Installation and Deployment Guide is to be reviewed by the Technical Lead, and the Test Lead. At a minimum the review should ensure that the Installation and Deployment Guide is technically correct and can be used to install and deploy the software or system in the target environment, resulting in a working and usable system.

### Approvals/Signoffs

The Installation and Deployment Guide is usually a deliverable component of the software solution. It is reviewed and bugs may be logged against it. But it is not approved or signed off unless required by the client scope/contract.

## Installation Guide Guidelines

*Retain the following information in the final document, usually on the back of the cover page. The comment is for guidance and may be deleted or hidden.*

### Guidelines for Revising This Document

This document is prepared using Microsoft Word. The Arial 11 point font is used.

Features of Word can be used to automatically maintain section numbers, table and figure numbers, and fields for information that appears frequently throughout the document.

This document is set up with margins of 0.75 inches on all sides. This setting will allow the document to be printed on both US Letter and European A4 paper sizes without reformatting.

This document contains comments to the author with guidelines on using or revising the document. To view this information, turn on the Review features of Word to show the Final Showing Markup view.

### Ownership and Revision

This Installation and Deployment Guide is owned and controlled by the project’s System Administrator. After a baseline of this document is published, the Technical Lead shall ensure that it is placed under change control.

Each change or revision made to this Installation Guide Document shall be summarized in “Revision history” section of this document.

## Contents

[1. Introduction](#1-introduction)

[1.1. Purpose](#11-purpose)

[1.2. Revision history](#12-revision-history)

[1.3. Intended audience and reading suggestion5](#13-intended-audience-and-reading-suggestions)

[1.4. Technical project stakeholders](#14-technical-project-stakeholders)

[1.5. References](#15-references)

[1.6. Definitions, acronyms and abbreviations](#16-definitions-acronyms-and-abbreviations)

[2. System Configurations](#2-system-configurations)

[2.1. Roles, Features, and Packages](#21-roles-features-and-packages)

[2.2. Command-Line](#22-command-line)

[2.3. Configured Values](#23-configured-values)

[3. Container Configurations](#3-container-configurations)

[3.1. Service 1 (Web UI)](#31-service-1-web-ui)

[3.1.1. Images and Packages](#311-images-and-packages)

[3.1.2. Container Configuration](#312-container-configuration)

[3.1.3. Configured Values 9](#313-configured-values)

[3.2. Service 2 (Data Structure Store)](#32-service-2-data-structure-store)

[3.2.1. Roles, Features, and Packages](#321-roles-features-and-packages)

[3.2.2. Configured Values 10](#322-configured-values)

[3.3. Service 3 (Documentation Framework)](#33-service-3-documentation-framework)

[3.3.1. Roles, Features, and Packages](#331-roles-features-and-packages)

[3.3.2. Configured Values](#332-configured-values)

[4. Software Deployment](#4-software-deployment)

[4.1. Connection with ChirpStack LoRaWAN Server](#41-connection-with-chirpstack-lorawan-server)

[4.2. Orchestration](#42-orchestration)

[5. Testing the Deployment](#5-testing-the-deployment)

[6. Troubleshooting](#6-troubleshooting)

# 1. Introduction

## 1.1. Purpose

The purpose of this Installation and Deployment Guide is to describe in technical terms the steps necessary to install the software referred to ChirpStack open-source LoRaWAN Network Server and make it operational.

## 1.2. Revision history

The Revision history table shows the date, changes, and authors who have worked on this document.

| Version/Change request number | Version date | Description of changes | Author |
| --- | --- | --- | --- |
| 1.0 | 08/05/2025 | First Draft | Eder D. Martínez |

## 1.3. Intended audience and reading suggestions

This Installation and Deployment Guide is intended to be used by technical stakeholders of the project who will be responsible for planning, performing, or maintaining the installation or deployment, such as the Systems Developers, Site Reliability Engineers (SRE) or Deployment Engineers.

It is intended that stakeholders and software support personnel can read this document and coordinate their efforts in the installation/deployment of the application.

## 1.4. Technical project stakeholders

This section provides a list of all known stakeholders with an interest in the project.

| Name | E-mail address | Role |
| --- | --- | --- |
| Jemison Montealgre | jeminson00@gmail.com | Product owner |
| Jonathan Gonzalez | jonathangc.awt@gmail.com | Lead Developer |
| Eder Martínez | 2220211052@estudiantesunibague.edu.co | Deployment Engineer |
| Carlos Bernal | 2420201003@estudiantesunibague.edu.co | Software Developer |

## 1.5. References

| Reference No. | Document | Author(s) |
| --- | --- | --- |
| REF-1 | [Install Hyper-V on Windows](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) | Microsoft |
| REF-2 | [How to install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) | Microsoft |
| REF-3 | [Enabling Intel VT and AMD-V virtualization hardware extensions in BIOS](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/5/html/virtualization/sect-virtualization-troubleshooting-enabling_intel_vt_and_amd_v_virtualization_hardware_extensions_in_bios#sect-Virtualization-Troubleshooting-Enabling_Intel_VT_and_AMD_V_virtualization_hardware_extensions_in_BIOS) | Red Hat |
| REF-4 | [Install Docker Engine](https://docs.docker.com/engine/install/) | Docker |
| REF-5 | [Overview of Docker Desktop](https://docs.docker.com/desktop/) | Docker |
| REF-6 | [Install and update Postman](https://learning.postman.com/docs/getting-started/installation/installation-and-updates/) | Postman |
| REF-7 | [How to Install and Use Curl on Ubuntu](https://linuxize.com/post/how-to-install-and-use-curl-on-ubuntu-20-04/) | Linuxize |
| REF-8 | [VIM](https://www.guia-ubuntu.com/index.php/Vim) | Guía Ubuntu |
| REF-9 | [Python documentation](https://www.python.org/doc/) | Python Software Foundation |
| REF-10 | [Django documentation](https://docs.djangoproject.com/en/5.2/) | Django Software Foundation |

## 1.6. Definitions, acronyms and abbreviations

| Term | Definition |
| --- | --- |
| Administrator | This is anyone from the client that has been given administrative rights in the ProjectName. |
| Ubuntu | Ubuntu 22.04 |
| db | Data base |
| CA | Certification Authority |
| CSR | Certificate Signing Request |

# 2. System Configurations

Installation of this product is supported on the following operation systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

## 2.1. Roles, Features, and Packages

**Features**

The main software is fetched from the project’s repository on GitHub and stored on chirpstack-docker directory

**Packages**

The following software packages must be installed before the deployment of the software:

1. Git Version Control System
2. Curl Command-Line Requests Tool
3. Vim Command-Line Text Editor
4. Docker Engine

## 2.2. Command-Line

**Authentication**

Most of the commands are recommended to be executed with administrative privileges

## 2.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current system.

| Information | Value |
| --- | --- |
| Default User | dragino |
| Default Root User Password | dragino |
| Default Software Directory | /home/dragino/IOT_EMASA/apr-rest-emasa |

# 3. Container Configurations

## 3.1. Service 1 (Web UI)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.1.1. Images and Packages

**Images**

The following software images are going to be created during the construction of the docker container

* api\_rest\_emasa-web

**Packages**

The following software packages must be included on the construction of the Docker image:

* asgiref: 3.8.1
* attrs: 25.1.0
* autobahn: 24.4.2
* Automat: 24.8.1
* cffi: 1.17.1
* channels: 4.2.0
* channels\_redis: 4.2.1
* constantly: 23.10.4
* cryptography: 44.0.1
* daphne: 4.1.2
* dj-database-url: 2.3.0
* Django: 5.1.6
* django-cors-headers: 4.7.0
* djangorestframework: 3.15.2
* djangorestframework\_simplejwt: 5.4.0
* hyperlink: 21.0.0
* idna: 3.10
* incremental: 24.7.2
* jsonschema: 4.23.0
* jsonschema-specifications: 2024.10.1
* msgpack: 1.1.0
* ocpp: 2.0.0
* psycopg: 3.2.4
* psycopg2-binary: 2.9.10
* pyasn1: 0.6.1
* pyasn1\_modules: 0.4.1
* pycparser: 2.22
* PyJWT: 2.10.1
* pyOpenSSL: 25.0.0
* redis: 5.2.1
* referencing: 0.36.2
* rpds-py: 0.23.1
* service-identity: 24.2.0
* setuptools: 75.8.0
* sqlparse: 0.5.3
* Twisted: 24.11.0
* txaio: 23.1.1
* typing\_extensions: 4.12.2
* websockets: 15.0
* zope.interface: 7.2
* whitenoise: 6.6.0

### 3.1.2. Container Configuration

**ChirpStack Server Configuration:**

**First Steps**

Once Container is running, [change the EMASA API REST administrator user password↗](#_Change_admin_user) to a more secure one.

**Authentication**

Chirpstack requires [administrative credentials↗](#_Configured_Values) to access main panel

### 3.1.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key values used for the current service.

| Information | Value |
| --- | --- |
| Container name | web-1 |
| ChirpStack Default Server Administrator account name | EMASADOCK |
| ChirpStack Default Server Administrator account password | Emasa123 |
| Volumes | ● .:/app <br>● Static\_volume:/app/staticfiles |
| Dependencies | ● Redis |
| Environment Variables | ● DJANGO\_SECRET\_KEY <br>● EMAIL\_HOST\_USER <br>● EMAIL\_HOST\_PASSWORD <br>● CHIRPSTACK\_JWT\_TOKEN <br>● SUPERUSER\_1\_USERNAME <br>● SUPERUSER\_1\_EMAIL <br>● SUPERUSER\_1\_PASSWORD <br>● SUPERUSER\_2\_USERNAME <br>● SUPERUSER\_2\_EMAIL <br>● SUPERUSER\_2\_PASSWORD <br>● POSTGRES\_USER <br>● POSTGRES\_PASSWORD <br>● POSTGRES\_DB <br>● REDIS\_PASSWORD |
| Exposed Ports | 8000 |

## 3.2. Service 2 (Data Structure Store)

The installation of this product is supported on the following operatve systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.2.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

* redis: 7-alpine

### 3.2.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current deployment.

| Information | Value |
| --- | --- |
| Container name | redis-1 |
| Volumes | ● redis\_data:/data |
| Environment Variables | ● REDIS\_PASSWORD |
| Exposed Ports | ● 6379 |

## 3.3. Service 3 (Documentation Framework)

The installation of this product is supported on the following operatve systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.3.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

* swagger: latest

### 3.3.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current deployment.

| Information | Value |
| --- | --- |
| Container name | Swagger-ui-1 |
| Volumes | ● ../openapi.json:/usr/share/nginx/html/openapi.json |
| Environment Variables | ● SWAGGER\_JSON\_URL |
| Exposed Ports | ● 8010 |

# 4. Software Deployment

## 4.1. Connection with ChirpStack LoRaWAN Server

To have communication with the EMASA middleware, it is necessary to add a network into docker system, to do it, run the following command

```sh
docker network -d bridge chirp-django-net
```
Then, add the netwroks prop into each container settings

```yml
networks:
      - chirp-django-net
```
## 4.2. Orchestration

Modify/create a docker-compose.yaml file and copy the following code into it.

    NOTE: Environment variables and ports can be changed as necessary

```yml
services:
  redis:
    image: redis:alpine
    restart: always
    volumes:
    - redis_data:/data
    environment:
    - REDIS_PASSWORD=redispass
    command: >
    sh -c "redis-server 
    --requirepass \"${REDIS_PASSWORD}\" 
    --save 300 1 
    --save 60 100 
    --appendonly no"
    networks:
    - chirp-django-net

  web:
    build: .
    command: bash -c "python manage.py migrate && python manage.py shell < init_superuser.py && daphne -b 0.0.0.0 -p 8000 drf.asgi:application"
    volumes:
    - static_volume:/app/staticfiles
    ports:
    - "8000:8000"
    environment:
    - DJANGO_SECRET_KEY=your_secret_key_here
    - EMAIL_HOST_USER=email@example.com
    - EMAIL_HOST_PASSWORD=password
    - CHIRPSTACK_JWT_TOKEN=your_chipstack_jwt_token_here
    - SUPERUSER_1_USERNAME=admin1
    - SUPERUSER_1_EMAIL=admin1@example.com
    - SUPERUSER_1_PASSWORD=admin1password
    - SUPERUSER_2_USERNAME=admin2
    - SUPERUSER_2_EMAIL=admin2@example.com
    - SUPERUSER_2_PASSWORD=admin2password
    - POSTGRESQL_HOST=persistance-postgres-1
    - POSTGRES_USER=chirpstack
    - POSTGRES_PASSWORD=chirpstack
    - POSTGRES_DB=chirpstack
    - REDIS_PASSWORD=redispass
    - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
    - redis
    networks:
    - chirp-django-net
  
  swagger-ui:
    image: swaggerapi/swagger-ui:latest
    ports:
    - "8010:8080"
    volumes:
    - ../openapi.json:/usr/share/nginx/html/openapi.json
    environment:
    - SWAGGER_JSON_URL=/openapi.json
    restart: always
    networks:
    - chirp-django-net

volumes:
  redis_data:
  static_volume:

networks:
  chirp-django-net:
    external: true
```
Verify that a ChirpStack API key is already generated and **`STORED IN A SAVE PLACE`**, the API key is not captured on logs, and it is displayed only once. A API key can be generated from the ChirpStack UI or by running the following command

```sh
docker exec -it <docker container name> \
chirpstack –-config /etc/chirpstack/ create-api-key –-name <name>
```
Place the ChirpStack API Key in the `docker-compose.yml` file under this environmet
```yml
CHIRPSTACK\_JWT\_TOKEN=hereGoesTheAPIKey
```
Finally, open the terminal in the path where docker-compose.yaml file is located and insert the following command.

```sh
docker-compose up -d
```
## 4.3. Deployment Diagram for EMASA API-REST
![Diagram](resources/SVG/emasa_api_rest_docker_diagram.svg)

# 5. Testing the Deployment

Due to this is deployed in a server, most of the time it won’t be possible to access a UI, so it is required that most of the operations are done using bash, curl and ChirpStack REST API.

1. A Token is required in order to use EMASA REST API. To generate the Token please run the following command in bash

    ```sh
    docker exec -it <docker container name> \
    curl –X POST “Content-type: application/json” \
    -d ‘{"username":"<Admin\_user\_name>","password":"<pass\_word>"}’ \
    http://localhost:8000/api/v1/token/
    ```
2. A token will be displayed on bash, **`THIS TOKEN IN TEMPORAL`**.
3. Open Postman or use Curl Command-Line Requests Tool and create a new session.
4. In the headers include the token in this format

    ```http
    Authorization: Token <TOKEN>
    ```
5. When using UI, a token is generated at every login. Navigate your web browser to localhost: then insert the port number registered in the docker-compose.yaml for EMASA REST API WEB container, the url should look something like this
    ```txt
    localhost:8000/admin
    ```
6. A chart requesting user and password will be displayed, once logged in a token will be generated and the API REST endpoints become available.
7. A complete API Documentation can be obtained by accessing the following path

    ```txt
    IOT_EMASA/openapi.json
    ```
8. To access the API Swagger UI, access the following route on a web browser

    ```txt
    localhost:8010
    ```

# 6. Troubleshooting

Docker logs can be visualized either through the Docker Engine container information using the docker logs <container name> command, by Checking container information on Docker Desktop

```sh
docker logs –-follow <docker container name>
```
or by accessing the log files directly on the host system. On Linux Ubuntu, logs are located at
 ```sh
/var/lib/docker/containers/<container_id>/<container_id>-json.log
```
