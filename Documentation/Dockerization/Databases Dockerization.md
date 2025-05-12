# DATABASE DOCKERIZATION

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

## Installation Guide guidelines

*Retain the following information in the final document, usually on the back of the cover page. The comment is for guidance and may be deleted or hidden.*

### *Acknowledgements

This document may refer to documents in Adobe® Acrobat® Portable Document Format (PDF). (Adobe® and Acrobat® are registered trademarks of Adobe Systems Incorporated.)

This document may refer to use of products in the Microsoft® Office suite, the Microsoft® Team Foundation Server® and Visual Studio®.

### Guidelines for revising this document

This document is prepared using Microsoft Word. The Arial 11 point font is used.

Features of Word can be used to automatically maintain section numbers, table and figure numbers, and fields for information that appears frequently throughout the document.

This document is set up with margins of 0.75 inches on all sides. This setting will allow the document to be printed on both US Letter and European A4 paper sizes without reformatting.

This document contains comments to the author with guidelines on using or revising the document. To view this information, turn on the Review features of Word to show the Final Showing Markup view.

### Ownership and revision

This Installation and Deployment Guide is owned and controlled by the project’s System Administrator. After a baseline of this document is published, the Technical Lead shall ensure that it is placed under change control.

Each change or revision made to this Installation Guide Document shall be summarized in “Revision history” section of this document.

## Contents

[1. Introduction](#_Toc197098672)

[1.1. Purpose](#_Toc197098673)

[1.2. Revision history](#_Toc197098674)

[1.3. Intended audience and reading suggestions](#_Toc197098675)

[1.4. Technical project stakeholders](#_Toc197098676)

[1.5. References](#_Toc197098677)

[1.6. Definitions, acronyms and abbreviations](#_Toc197098678)

[2. System Configurations](#_Toc197098679)

[2.1. Roles, Features, and Packages](#_Toc197098680)

[2.2. Command-Line](#_Toc197098681)

[2.3. Configured Values](#_Toc197098682)

[3. Container Configurations](#_Toc197098683)

[3.1. Service 1 (Database)](#_Toc197098684)

[3.1.1. Roles, Features, and Packages](#_Toc197098685)

[3.1.2. Container Configuration](#_Toc197098686)

[3.1.3. Configured Values](#_Toc197098687)

[4. Software Deployment](#_Toc197098688)

[4.1. Connection with EMASA API-REST](#_Toc197098689)

[4.2. Orchestration](#_Toc197098690)

[5. Testing the Deployment](#_Toc197098691)

[6. Troubleshooting](#_Toc197098692)

# 1. Introduction

## 1.1. Purpose

The purpose of this Installation and Deployment Guide is to describe in technical terms the steps necessary to install the software referred to ChirpStack open-source LoRaWAN Network Server and make it operational.

## 1.2. Revision history

The Revision history table shows the date, changes, and authors who have worked on this document.

| Version/Change request number | Version date | Description of changes | Author |
| --- | --- | --- | --- |
| 1.0 | 01/04/2025 | First Draft | Eder D. Martínez |

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

| Reference No. | Article | Author(s) |
| --- | --- | --- |
| REF-1 | [Enabling Intel VT and AMD-V virtualization hardware extensions in BIOS](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/5/html/virtualization/sect-virtualization-troubleshooting-enabling_intel_vt_and_amd_v_virtualization_hardware_extensions_in_bios#sect-Virtualization-Troubleshooting-Enabling_Intel_VT_and_AMD_V_virtualization_hardware_extensions_in_BIOS) | Red Hat |
| REF-2 | [Install Hyper-V on Windows](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) | Microsoft |
| REF-3 | [How to install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) | Microsoft |
| REF-4 | [Install Docker Engine](https://docs.docker.com/engine/install/) | Docker |
| REF-5 | [Overview of Docker Desktop](https://docs.docker.com/desktop/) | Docker |
| REF-6 | [PostgreSQL 16.9 Documentation](https://www.postgresql.org/docs/16/index.html) | PostgreSQL |



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

## 3.1. Service 1 (Database)

The installation of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 3.1.1. Roles, Features, and Packages

**Packages**

The following software packages must be installed on the construction of the Docker container:

1. postgresql: 16-alpine

### 3.1.2. Container Configuration

**Postgres Service Configuration:**

**Authentication**

Need to provide [postgres user, database name and password↗](#_Configured_Values_1)

### 3.1.3. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current deployment.

| Information | Value |
| --- | --- |
| Container name | postgres-1 |
| Postgres Default Server Administrator account name | chirpstack |
| Postgres Default Server Administrator account password | chirpstack |
| Postgres Default Database | chirpstack |
| Volumes | ● ./configuration/postgresql/initdb:/docker-entrypoint-initdb.d <br> ● postgresqldata:/var/lib/postgresql/data |
| Environment Variables | ● POSTGRES\_USER <br> ● POSTGRES\_PASSWORD <br>● POSTGRES\_DB |

# 4. Software Deployment

## 4.1. Connection with EMASA API-REST

To have communication with the EMASA middleware, it is necessary to add a network into docker system, to do it, run the following command

```sh
docker network -d bridge chirp-django-net
```
l
prop into each container settin
```yml
networks:
    - chirp-django-net
```
## 4.2. Orchestration

Modify/create a docker-compose.yaml file and copy the following code into it.

NOTE: Environment variables and ports can be changed as necessary
```yml
services:
    postgres:
        image: postgres:16-alpine
        restart: unless-stopped
        volumes:
        - ./configuration/postgresql/initdb:/docker-entrypoint-initdb.d
        - postgresqldata:/var/lib/postgresql/data
        environment:
        - POSTGRES\_USER=chirpstack
        - POSTGRES\_PASSWORD=chirpstack
        - POSTGRES\_DB=chirpstack
        networks:
        - chirp-django-net
    
volumes:
    postgresqldata:

networks:
    chirp-django-net:
        external: true
```

Finally, open the terminal in the path where docker-compose.yaml file is located and insert the following command, then press enter.

```sh
docker-compose up --build -d
```
## 4.3 Deployment Diagram for Database
![Diagram](images/datebase_docker_diagram.svg)


# 5. Testing the Deployment

Once the deployment is complete, it is possible to check if it was correctly set up by validating the owner of the Postgres database tables. In order to accomplish this, follow the guide below

1. Check if you can access the chirpstack database with the user chirpstack using the command

    ```sh
    docker exec -it <docker container name> \
    psql -U chirpstack -d chirpstack
    ```
12. Inside of the postgres interface run the command

    ```sh
    \l
    ```

3. A list of the available databases list is going to be displayed, make sure the owner is set to chirpstack.

    ```sh
    |Name        | Owner      | Encoding |
    |------------+------------+----------|
    |chirpstack  | chirpstack | UTF8     |
    |postgres    | chirpstack | UTF8     |
    |template0   | chirpstack | UTF8     |
    |template1   | chirpstack | UTF8     |
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
