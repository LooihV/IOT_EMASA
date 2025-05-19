# Deployment Considerations

## Installation and Deployment Guide

Software Version: 1.0 | 18 may 2025

## Installation and Deployment Guide template information

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

### Installation Guide guidelines

*Retain the following information in the final document, usually on the back of the cover page. The comment is for guidance and may be deleted or hidden.*

### Acknowledgements

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

[1. Introduction](#1-introduction)

[1.1. Purpose](#11-purpose)

[1.2. Revision history](#12-revision-history)

[1.3. Intended audience and reading suggestions](#13-intended-audience-and-reading-suggestions)

[1.4. Technical project stakeholders](#14-technical-project-stakeholders)

[2. Considerations](#2-considerations)

[2.1. Environment Variables](#21-environment-variables)

[2.2. Healthcheks](#22-healthcheks)

[2.3. Exposed ports](#23-exposed-ports)

[3. Troubleshooting](#3-troubleshooting)

# 1. Introduction

## 1.1. Purpose

The purpose of this Installation and Deployment Guide is to describe in technical terms the steps necessary to install the software referred to ChirpStack open-source LoRaWAN Network Server and make it operational.

## 1.2. Revision history

The Revision history table shows the date, changes, and authors who have worked on this document.

| Version/Change request number | Version date | Description of changes | Author |
| --- | --- | --- | --- |
| 1.0 | 18/05/2025 | First Draft | Eder D. Martínez |

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

# 2. Considerations
As it can be noiced, tnere are two docker-compose files, one for development purposes and one for production purposes. It is important to recognize their differences at their requirements. This docuemnt in focuesed on the production file. to check out development files requiremets, please refer to the [development file](, please refer to the [development docs↗](../Dockerization/).
## 2.1. Environment variables
 It is indespensable to create a `.env.prod` file at the root directory of the repository, containing the following variables:
```txt
SWAGGER_JSON_URL
REDIS_PASSWORD
REDIS_HOST
MQTT_BROKER_HOST
MQTT_BROKER_PORT
REDIS_HOST
INTEGRATION__MQTT__EVENT_TOPIC_TEMPLATE
INTEGRATION__MQTT__STATE_TOPIC_TEMPLATE
INTEGRATION__MQTT__COMMAND_TOPIC_TEMPLATE
CHIRPSTACK__POSTGRESQL__DSN
POSTGRESQL_HOST
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_PORT
DJANGO_SECRET_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
CHIRPSTACK_JWT_TOKEN
ALLOWED_HOST
SUPERUSER_1_USERNAME
SUPERUSER_1_EMAIL
SUPERUSER_1_PASSWORD
SUPERUSER_2_USERNAME
SUPERUSER_2_EMAIL
SUPERUSER_2_PASSWORD
```
## 2.2. Healthcheks
Production docker-compose file contains a healthcheck for the most relevant services. This is done to ensure that the services are running properly before the application is exposed to the public. The healthchecks are defined in the `healthcheck` section of the docker-compose file. 

> NOTE: Healthchecks are important for scaleability and resilience, it is recommnded to keep them activ specially for Docker Swarm of Kubernetes implementations.
## 2.3. Exposed ports
Production docker-compose file contains a port mapping for the most relevant services. This is done to ensure that the services are running properly before the application is exposed to the public. The port mappings are defined in the `ports` section of the docker-compose file.
> NOTE: it recommended to use common ports for the services due to security reasons.

# 3. Troubleshooting

Docker logs can be visualized either through the Docker Engine container information using the docker logs <container name> command, by Checking container information on Docker Desktop
```sh
docker logs –-follow <docker container name>
```
or by accessing the log files directly on the host system. On Linux Ubuntu, logs are located at
```sh
/var/lib/docker/containers/<container\_id>/<container\_id>-json.log
```
