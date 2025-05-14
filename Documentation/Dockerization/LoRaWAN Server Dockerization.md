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

[1.2. Revision History](#12-revision-history)

[1.3. Intended Audience and Reading Suggestions](#13-intended-audience-and-reading-suggestions)

[1.4. Technical Project Stakeholders](#14-technical-project-stakeholders)

[1.5. References](#15-references)

[1.6. Definitions, Acronyms and Abbreviations](#16-definitions-acronyms-and-abbreviations)

[2. System Configurations](#2-system-configurations)

[2.1. Roles, Features, and Packages](#22-command-line)

[2.2. Command-Line](#22-command-line)

[2.3. Configured Values](#23-configured-values)

[3. Container Configurations](#3-container-configurations)

[3.1. Service 1 (Web UI)](#31-service-1-web-ui)

[3.1.1. Roles, Features, and Packages](#311-roles-features-and-packages)

[3.1.2. Container Configuration](#312-container-configuration)

[3.1.3. Configured Values](#313-configured-values)

[3.2. Service 2 (Gateway Bridge)](#32-service-2-gateway-bridge)

[3.2.1. Roles, Features, and Packages](#321-roles-features-and-packages)

[3.2.2. Container Configuration](#322-container-configuration)

[3.2.3. Configured Values](#323-configured-values)

[3.3. Service 3 (BasicStation)](#33-service-3-basicstation)

[3.3.1. Roles, Features, and Packages](#331-roles-features-and-packages)

[3.3.2. Container Configuration](#332-container-configuration)

[3.3.3. Configured Values](#333-configured-values)

[3.4. Service 4 (REST API)](#34-service-4-rest-api)

[3.4.1. Roles, Features, and Packages](#341-roles-features-and-packages)

[3.4.2. Configured Values](#342-configured-values)

[3.5. Service 5 (Data Structure Store)](#35-service-5-data-structure-store)

[3.5.1. Roles, Features, and Packages](#351-roles-features-and-packages)

[3.5.2. Container Configuration](#352-configured-values)

[3.6. Service 6 (MQTT Broker)](#36-service-6-mqtt-broker)

[3.6.1. Roles, Features, and Packages](#361-roles-features-and-packages)

[3.6.2. Configured Values](#362-configured-values)

[4. Software Deployment](#4-software-deployment)

[4.1. TLS Connection](#41-tls-conection)

[4.1.1. Requirements](#411-requirements)

[4.1.2. Certification Authority Generation](#412-certification-authority-generation)

[4.1.3. Server Certificate Generation](#413-mosquitto-configuration)

[4.2. Conection with EMASA API-REST](#42-conection-with-emasa-api-rest)

[4.3. Orchestration](#43-orchestration)

[4.4. Deployment Diagram for LoRaWAN Server](#44-deployment-diagram-for-lorawan-server)

[5. Testing the Deployment](#5-testing-the-deployment)

[5.1. Change admin user password](#51-change-admin-user-password)

[6. Troubleshooting](#6-troubleshooting)

# 1. Introduction

## 1.1. Purpose

The purpose of this Installation and Deployment Guide is to describe in technical terms the steps necessary to install the software referred to ChirpStack open-source LoRaWAN Network Server and make it operational.

## 1.2. Revision History

The Revision history table shows the date, changes, and authors who have worked on this document.

| Version/Change request number | Version date | Description of changes | Author |
| --- | --- | --- | --- |
| 1.0 | 21/03/2025 | First Draft | Eder D. Martínez |

## 1.3. Intended Audience and Reading Suggestions

This Installation and Deployment Guide is intended to be used by technical stakeholders of the project who will be responsible for planning, performing, or maintaining the installation or deployment, such as the Systems Developers, Site Reliability Engineers (SRE) or Deployment Engineers.

It is intended that stakeholders and software support personnel can read this document and coordinate their efforts in the installation/deployment of the application.

## 1.4. Technical Project Stakeholders

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
| REF-9 | [The ChirpStack project](https://www.chirpstack.io/docs/) | ChirpStack |
| REF-10 | [LoRaWAN](https://es.wikipedia.org/wiki/LoRaWAN) | Wikipedia |
| REF-11 | [LoRa](https://www.vencoel.com/que-es-lora-como-funciona-y-caracteristicas-principales/) | VENCO |
| REF-12 | [MQTT Ports: Common Ports and How to Configure and Secure Them](https://www.emqx.com/en/blog/mqtt-ports) | EMQ Technologies |

## 1.6. Definitions, Acronyms and Abbreviations

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

Once Container is running, [change the ChirpStack administrator user password↗](#51-change-admin-user-password) to a more secure one.

**Authentication**

Chirpstack requires [administrative credentials↗](#313-configured-values) to access main panel

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

Before running the compose file, make sure that the [region is correctly assigned (us915_7)↗](#43-orchestration)

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

Before running the compose file, make sure that the [region is correctly assigned (us915_7)↗](#43-orchestration)

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
## 4.1. TLS Conection
### 4.1.1. Requirements
Before proceeding, please make sure that you have installed the [cfssl](https://github.com/cloudflare/cfssl)
utility. You should also already have a working ChirpStack environment.

If using Debian or Ubuntu, this package can be installed using:

```sh
sudo apt-get install golang-cfssl
```

### 4.1.2. Certification Authority Generation 
In order to MQTT integration to work, it is necessary to have registered a valid certificate authority registered (this certificate authority can be self-signed). The steps describing the process are below.

1. Create a folder outside of the `IOT_EMASA` directory called `.certs` and go inside the directory.

    ```sh
    mkdir .certs && cd .certs
    ```
2. Create a file called `ca-csr.json` inside the directory with the following content:

    ```json
    {
        "CN": "ChirpStack CA",
        "key": {
            "algo": "rsa",
            "size": 4096
        }
    }
    ```

3. Create a file called `ca-config.json` inside the directory with the following content:
    ```json
    {
        "signing": {
            "default": {
                "expiry": "8760h"
            },
            "profiles": {
                "server": {
                    "expiry": "8760h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "server auth"
                    ]
                }
            }
        }
    }
    ```

3. Then execute the following command to generate the CA certificate and key:

    ```sh
    cfssl gencert -initca ca-csr.json | cfssljson -bare ca
    ```

### 4.1.2. Server Certificate Generation

The MQTT server-sertificate is used to establish a secure TLS connection between
the MQTT client (gateway or integration) and the MQTT broker.

1.  Create a file called `mqtt-server.json` and change`example.com` into the hostname that will be used by clients that will connect to the MQTT broker:

    ```json
    {
        "CN": "example.com",
        "hosts": [
            "example.com"
        ],
        "key": {
            "algo": "rsa",
            "size": 4096
        }
    }
    ```

2. Execute the following command to generate the MQTT server-certificate:

    ```sh
    cfssl gencert -ca ca.pem -ca-key ca-key.pem -config ca-config.json -profile server mqtt-server.json | cfssljson -bare mqtt-server
    ```
### 4.1.3. Mosquitto Configuration
1. Create a folder outside of the IOT_EMASA directory called `.acl` and go inside the directory.
    
    ```sh
    mkdir .acl && cd .acl
    ```
2. Create an `acl` file and add the following content to it:
    
    ```text
    pattern readwrite +/gateway/%u/#
    pattern readwrite application/%u/#
    ```
3. In the docker compose file, add the following lines to the `mosquitto` service section:

    ```yml
    mosquitto:
        volumes:
        - ../.acl:/etc/mosquitto/acl
    ```
4. go inside `IOT_EMASA/lorawan-server/configuration/mosquitto/config/mosquitto.conf` file and add the following lines:

    ```conf
    per_listener_settings true

    listener 1883 127.0.0.1
    allow_anonymous true

    listener 8883 0.0.0.0
    cafile /etc/mosquitto/certs/ca.pem
    certfile /etc/mosquitto/certs/mqtt-server.pem
    keyfile /etc/mosquitto/certs/mqtt-server-key.pem
    allow_anonymous false
    require_certificate true
    use_identity_as_username true
    acl_file /etc/mosquitto/acl
    ```
>**NOTES**
>1. Make sure to restart ChirpStack. Also verify the logs for possible errors.
>2. The `ca.pem`, `cert.pem` and `key.pem` must be obtained from the ChirpStack
  web-interface (gateway certificate or application MQTT integration certificate).
>3. Verify that your firewall rules allow incoming connections to the MQTT broker.
>4. In case you see TLS related errors, please verify that the hostname
  (of the `-h` flag) matches the MQTT server-certificate. Validation of the 
  server-certificate can be disabled using the `--insecure` flag.

## 4.2. Conection with EMASA API-REST

1. To have communication with the EMASA middleware, it is necessary to add a network into docker system, to do it, run the following command

    ```sh
    docker network -d bridge chirp-django-net
    ```

    prop into each container settings

    ```yml
    networks:

        - chirp-django-net
    ```

## 4.3. Orchestration

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
## 4.4. Deployment Diagram for LoRaWAN Server
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
    Authorization: Bearer <TOKEN>
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

