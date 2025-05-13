# LoRaWAN Server Dockerization

## Installation and Deployment Guide

Software Version: 1.0 | Date: 21 mar 2025

## Installation and Deployment Guide information

The purpose of this document is to provide the System Administrator or any other technical stakeholder with a complete and easy to follow guide designed specifically for the Technical Domain. It is intended to provide installation instructions to any stakeholder that has an interest or a role in the project.

### Document Responsibilities

The Installation and Deployment Guide is first created in the Deployment process step. Responsibilities for document creation and content are shown in the [RACI](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix) chart below:


| **Group Manager** | **Project Manager** | **Technical Lead** | **Business Analyst** | **Developer** | **Testing Analyst** |
| --- | --- | --- | --- | --- | --- |
| I | A | R | I | C | I |

### Combining or splitting documents

Documentation required by the process may be physically combined into fewer documents or split up into more documents in any way which makes sense to the project provided that all topics required by all the standard templates are present.

If information is split across several documents, all related documents shall be included in the reviews and sign off. For example, when installation and deployment instructions are in separate documents, the documents shall undergo the same preparation, review, and approval activities as well as review to ensure consistency of technical information among the component documents.

### Reviews

The Installation and Deployment Guide is to be reviewed by the Technical Lead, and the Test Lead. At a minimum the review should ensure that the Installation and Deployment Guide is technically correct and can be used to install and deploy the software or system in the target environment, resulting in a working and usable system.

### Approvals/Signoffs

The Installation and Deployment Guide is usually a deliverable component of the software solution. It is reviewed and bugs may be logged against it. But it is not approved or signed off unless required by the client scope/contract.

## Installation guide guidelines

*Retain the following information in the final document, usually on the back of the cover page. The comment is for guidance and may be deleted or hidden.*



### Guidelines for revising this document

This document is prepared using Microsoft Word. The Arial 11 point font is used.

Features of Word can be used to automatically maintain section numbers, table and figure numbers, and fields for information that appears frequently throughout the document.

This document is set up with margins of 0.75 inches on all sides. This setting will allow the document to be printed on both US Letter and European A4 paper sizes without reformatting.

This document contains comments to the author with guidelines on using or revising the document. To view this information, turn on the Review features of Word to show the Final Showing Markup view.

### Ownership and revision

This Installation and Deployment Guide is owned and controlled by the project’s System Administrator. After a baseline of this document is published, the Technical Lead shall ensure that it is placed under change control.

Each change or revision made to this Installation Guide Document shall be summarized in “Revision history” section of this document.

## Contents

[1. Introduction](#_Toc194682498)

[1.1. Purpose](#_Toc194682499)

[1.2. Revision history](#_Toc194682500)

[1.3. Intended audience and reading suggestions](#_Toc194682501)

[1.4. Technical project stakeholders](#_Toc194682502)

[1.5. References](#_Toc194682503)

[1.6. Definitions, acronyms and abbreviations](#_Toc194682504)

[2. System Configurations](#_Toc194682505)

[2.1. Roles, Features, and Packages](#_Toc194682506)

[2.2. Command-Line](#_Toc194682507)

[2.3. Configured Values](#_Toc194682508)

[3. Container Configurations](#_Toc194682509)

[3.1. Service 1 (Web UI)](#_Toc194682510)

[3.1.1. Roles, Features, and Packages](#_Toc194682511)

[3.1.2. Container Configuration](#_Toc194682512)

[3.1.3. Configured Values](#_Toc194682513)

[3.2. Service 2 (Gateway Bridge)](#_Toc194682514)

[3.2.1. Roles, Features, and Packages](#_Toc194682515)

[3.2.2. Container Configuration](#_Toc194682516)

[3.2.3. Configured Values](#_Toc194682517)

[3.3. Service 3 (BasicStation)](#_Toc194682518)

[3.3.1. Roles, Features, and Packages](#_Toc194682519)

[3.3.2. Container Configuration](#_Toc194682520)

[3.3.3. Configured Values](#_Toc194682521)

[3.4. Service 4 (REST API)](#_Toc194682522)

[3.4.1. Roles, Features, and Packages](#_Toc194682523)

[3.4.2. Configured Values](#_Toc194682524)

[3.5. Service 5 (Database)](#_Toc194682525)

[3.5.1. Roles, Features, and Packages](#_Toc194682526)

[3.5.2. Container Configuration](#_Toc194682527)

[3.5.3. Configured Values](#_Toc194682528)

[3.6. Service 6 (Data Structure Store)](#_Toc194682529)

[3.6.1. Roles, Features, and Packages](#_Toc194682530)

[3.6.2. Configured Values](#_Toc194682531)

[3.7. Service 7 (MQTT Broker)](#_Toc194682532)

[3.7.1. Roles, Features, and Packages](#_Toc194682533)

[3.7.2. Configured Values](#_Toc194682534)

[4. Software Deployment](#_Toc194682535)

[5. Testing the Deployment](#_Toc194682536)

[5.1.1. Change admin user password](#_Toc194682537)

[6. Troubleshooting](#_Toc194682538)

# 1. Introduction

## 1.1. Purpose

The purpose of this Installation and Deployment Guide is to describe in technical terms the steps necessary to install the software referred to ChirpStack open-source LoRaWAN Network Server and make it operational.

## 1.2. Revision history

The Revision history table shows the date, changes, and authors who have worked on this document.

| Version/Change request number | Version date | Description of changes | Author |
| --- | --- | --- | --- |
| 1.0 | 21/03/2025 | First Draft | Eder D. Martínez |

## 1.3. Intended audience and reading suggestions

This Installation and Deployment Guide is intended to be used by technical stakeholders of the project who will be responsible for planning, performing, or maintaining the installation or deployment, such as the Systems Developers, Site Reliability Engineers (SRE) or Deployment Engineers.

It is intended that stakeholders and software support personnel can read this document and coordinate their efforts in the installation/deployment of the application.

## 1.4. Technical project stakeholders

This section provides a list of all known stakeholders with an interest in the project.

| Name | E-mail address | Role |
| --- | --- | --- |
| Jemison Montealgre | jonathangc.awt@gmail.com | Product owner |
| Jonathan Gonzalez | jeminson00@gmail.com | Lead Developer |
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
| REF-9 | [The ChirpStack project](https://www.chirpstack.io/docs/) | ChirpStack |
| REF-10 | [LoRaWAN](https://es.wikipedia.org/wiki/LoRaWAN) | Wikipedia |
| REF-11 | [LoRa](https://www.vencoel.com/que-es-lora-como-funciona-y-caracteristicas-principales/) | VENCO |
| REF-12 | [MQTT Ports: Common Ports and How to Configure and Secure Them](https://www.emqx.com/en/blog/mqtt-ports) | EMQ Technologies |

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
| Default Software Directory | /home/dragino/IOT\_EMASA/lorawan\_server |

# 3. Container Configurations

## 3.1. Service 1 (Web UI)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.1.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. chirpstack/chirpstack: 4

### 3.1.2. Container Configuration

**ChirpStack Server Configuration:**

**First Steps**

Once Container is running, [change the ChirpStack administrator user password↗](#_Change_admin_user) to a more secure one.

**Authentication**

Chirpstack requires [administrative credentials↗](#_Configured_Values) to access main panel

### 3.1.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Container name | chirpstack-1 |
| ChirpStack Default Server Administrator account name | admin |
| ChirpStack Default Server Administrator account password | admin |
| Volumes | ● ./configuration/chirpstack:/etc/chirpstack |
| Dependencies | ● Postgres <br> ● Redis <br> ● Mosquitto | |
| Environment Variables | ● MQTT\_BROKER\_HOST <br>● REDIS\_HOST <br>● POSTGRESQL\_HOST |
| Exposed Ports | 8080 |

## 3.2. Service 2 (Gateway Bridge)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.2.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. Chirpstack/chirpstack-gateway-bridge: 4

### 3.2.2. Container Configuration

**ChirpStack Gate Configuration:**

**First Steps**

Before running the compose file, make sure that the [region is correctly assigned (us915\_7)↗](#_Software_Deployment)

### 3.2.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Container name | chirpstack-gateway-bridge-1 |
| Volumes | ● ./configuration/chirpstack-gateway-bridge:/etc/chirpstack-gateway-bridge |
| Environment Variables | ● INTEGRATION\_\_MQTT\_\_EVENT\_TOPIC\_TEMPLATE <br>● INTEGRATION\_\_MQTT\_\_STATE\_TOPIC\_TEMPLATE <br> ● INTEGRATION\_\_MQTT\_\_COMMAND\_TOPIC\_TEMPLATE |
| Exposed Ports | 1700/udp |

## 3.3. Service 3 (BasicStation)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.3.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. chirpstack/chirpstack-gateway-bridge-basicstation: 4

### 3.3.2. Container Configuration

**ChirpStack Gate Configuration:**

**First Steps**

Before running the compose file, make sure that the [region is correctly assigned (us915\_7)↗](#_Software_Deployment)

### 3.3.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Container name | chirpstack-gateway-bridge-basicstation-1 |
| Volumes | ● ./configuration/chirpstack-gateway-bridge:/etc/chirpstack-gateway-bridge |
| Dependencies | Mosquitto |
| Exposed Ports | 3001 |

## 3.4. Service 4 (REST API)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.4.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. chirpstack/chirpstack-rest-api:4

### 3.4.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Container name | chirpstack-rest-api-1 |
| Dependencies | Chirpstack |
| Exposed Ports | 8090 |

## 3.5. Service 5 (Data Structure Store)

The installation of this product is supported on the following operatve systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.5.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. redis: 7-alpine

### 3.5.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current deployment.

| Information | Value |
| --- | --- |
| Container name | redis-1 |
| Volumes | ● redisdata:/data |

## 3.6. Service 6 (MQTT Broker)

Installation of this product is supported on the following operation systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.6.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. Eclipse-mosquitto: 2

### 3.6.2. Configured Values

| Information | Value |
| --- | --- |
| Container name | Mosquitto-1 |
| Exposed Ports | 1883 |
| Volumes | ● ./configuration/mosquitto/config/:/mosquitto/config/ <br>● ../../.certs:/etc/mosquito/certs |

# 4. Software Deployment

The following deployment is a fork from the offcial chirpstack-docker GitHub repository that can be obtained running the following command

```sh
git clone https://github.com/chirpstack/chirpstack-docker.git
```
## 4.1. Certification Authority Generation

In order to MQTT integration to work, it is necessary to have registered a valid certificate authority registered (this certificate authority can be self-signed). The steps describing the process are below.

1. Create a folder outside of the IOT\_EMASA folder called .certs and go inside the directory.

mkdir .certs && cd .certs

2. Generate a RSA of 4096 bits private key for the Certification Authority and saves it in a ca.key file.

openssl genrsa -out ca.key 4096

3. Generate a Self-signed certificate for the CA

openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem

4. Fill up the fields requested on screen

5. Now in the directory it should appear a ca.pem and ca.key files.

## 4.2. Server certificate Generation (Optional)

This is and optional but more direct way to create self-signed certificates for MQTT communication between ChirpStack and Mosquitto.

1. In .certs folder create a mqtt-server.crt file using the following command.

openssl genrsa -out mqtt-server.key 4096

2. Create a certificate signing request using the following command.

openssl req -new -key mqtt-server.key -out mqtt-server.csr

3. Sign the CSR with your CA to generate the server certificate with the following command.

openssl x509 -req -in mqtt-server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out mqtt-server.crt -days 3650 -sha256

## 4.3. Conection with EMASA API-REST

1. To have communication with the EMASA middleware, it is necessary to add a network into docker system, to do it, run the following command

    ```sh
    docker network -d bridge chirp-django-net
    ```

    prop into each container settings

    ```yml
    networks:

        - chirp-django-net
    ```

## 4.4. Orchestration

Modify/create the docker-compose.yaml file and copy the following code into it.

    NOTE: Environment variables and ports can be changed as necessary

```yml
services:
  chirpstack:
    image: chirpstack/chirpstack:4
    user: 1000:1000
    command: -c /etc/chirpstack
    restart: unless-stopped
    volumes:
    - ./configuration/chirpstack:/etc/chirpstack
    - ../../.certs:/etc/chirpstack/certs
    depends_on:
    - mosquitto
    - redis
    environment:
    - MQTT_BROKER_HOST=mosquitto
    - REDIS_HOST=redis
    - POSTGRESQL_HOST=persistence-postgres-1
    ports:
    - "8080:8080"
    networks:
    - chirp-django-net

  chirpstack-gateway-bridge:
    image: chirpstack/chirpstack-gateway-bridge:4
    restart: unless-stopped
    ports:
    - "1700:1700/udp"
    volumes:
    - ./configuration/chirpstack-gateway-bridge:/etc/chirpstack-gateway- bridge
    environment:
    - INTEGRATION__MQTT__EVENT_TOPIC_TEMPLATE=us915_7/gateway/{{ .GatewayID }}/event/{{ .EventType }}
    - INTEGRATION__MQTT__STATE_TOPIC_TEMPLATE=us915_7/gateway/{{ .GatewayID }}/state/{{ .StateType }}
    - INTEGRATION__MQTT__COMMAND_TOPIC_TEMPLATE=us915_7/gateway/{{ .GatewayID }}/command/#
    depends_on:
    - mosquito
    networks:
    - chirp-django-net

  chirpstack-gateway-bridge-basicstation:
    image: chirpstack/chirpstack-gateway-bridge:4
    restart: unless-stopped
    command: -c /etc/chirpstack-gateway-bridge/chirpstack-gateway-bridge-basicstation-us915_7.toml
    ports:
    - "3001:3001"
    volumes:
    - ./configuration/chirpstack-gateway-bridge:/etc/chirpstack-gateway-bridge
    - ../../.certs:/etc/chirpstack-gateway-bridge/certs
    depends_on:
    - mosquito
    networks:
    - chirp-django-net

  chirpstack-rest-api:
    image: chirpstack/chirpstack-rest-api:4
    restart: unless-stopped
    command: --server chirpstack:8080 --bind 0.0.0.0:8090 --insecure
    ports:
    - "8090:8090"
    depends_on:
    - chirpstack
    networks:
    - chirp-django-net
  
redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --save 300 1 --save 60 100 --appendonly no
    volumes:
    - redisdata:/data
    networks:
    - chirp-django-net

  mosquitto:
    image: eclipse-mosquitto:2
    restart: unless-stopped
    ports:
    - "1883:1883"
    volumes:
    - ./configuration/mosquitto/config/:/mosquitto/config/
    - ../../.certs:/etc/mosquito/certs
    networks:
    - chirp-django-net

volumes:
  redisdata:

networks:
    chirp-django-net:
        external: true
```
Verify that the file located at /configration/chirpstack/chirpstack.toml has the following sections.

```conf
[network]
    enabled\_regions=[
        "as923",
        "as923_2",
        "as923_3",
        "as923_4",
        "au915_0",
        "cn470_10",
        "cn779",
        "eu433",
        "eu868",
        "in865",
        "ism2400",
        "kr920",
        "ru864",
        "us915_0",
        "us915_1",
        "us915_7", #<------working region
    ]
```
In case it becomes necesary to connect via ssl add the following lines

```conf
[integrattion]
    [integration.mqtt]
        [integration.mqtt.client]
            ca_cert="/etc/chirpstack/certs/ca.pem"
            ca_key="/etc/chirpstack/certs/ca.key"
```
Finally, open the terminal in the path where docker-compose.yaml file is located and insert the following command, then press enter.

```sh
docker-compose up -d
```
## 4.5. Deployment Diagram for LoRaWAN Server
![Diagram](resources/SVG/lorawan_server_docker_diagram.svg)


# 5. Testing the Deployment

Due to this is deployed in a server, most of the time it won’t be possible to access a UI, so it is required that most of the operations are done using bash, curl and ChirpStack REST API.

1. A Token is required in order to use ChirpStack REST API. To generate the Token please run the following command in bash

    ```sh
    docker exec -it <docker container name> \
    chirpstack –-config /etc/chirpstack/ create-api-key –-name <name>
    ```

2. A token will be displayed on bash, **`SAVE THE TOKEN IN A SAVE PLACE`.**
3. Navigate your web browser to localhost: then insert the port number registered in the docker-compose.yaml for Chirpstack REST API container, the url should look something like this

    ```sh
    localhost:8090
    ```

4. A Swagger web UI will display on screen showing all the possible requests and its models
5. Open Postman or use Curl Command-Line Requests Tool and create a new session.
6. In the headers include the token in this way

    ```http
    Authorization = Bearer <TOKEN>
    ```
7. As mentioned previously in this document it is recommended to change the admin user password, in order to achieve this, follow the guide below.

## 5.1. Change admin user password

1. In Postman or Curl make a GET request with the following criteria:

    ```sh
    url: localhost:8090/api/users?limit=5

    headers: Authorization = Bearer <TOKEN>
    ```

2. The returned json should look something like this:

    ```json
    {
        "totalCount": 1,
        "result": [
            {
                "id": "05244f12-6daf-4e1f-8315-c66783a0ab56",
                "createdAt": "2025-04-01T21:07:49.076775Z",
                "updatedAt": "2025-04-01T21:07:49.076775Z",
                "email": "admin",
                "isAdmin": true,
                "isActive": true
            }
        ]
    }
    ```

3. Note down the user id, then make a POST request with the following criteria

    ```http
    url: localhost:8090/api/users?limit=5

    headers: Authorization = Bearer <TOKEN>,

    body: {"password": <New password>}🡨 SAVE THE NEW PASSWORD IN A SAVE PLACE.
    ```
# 6. Troubleshooting

Docker logs can be visualized either through the Docker Engine container information using the docker logs <container name> command, by Checking container information on Docker Desktop

```sh
docker logs –-follow <docker container name>
```
or by accessing the log files directly on the host system. On Linux Ubuntu, logs are located at

```sh
/var/lib/docker/containers/<container\_id>/<container\_id>-json.log
```

