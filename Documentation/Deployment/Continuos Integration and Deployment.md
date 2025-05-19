# Continuos Integration and Deployment (CI/CD)

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

[1.5. References](#15-references)

[2. Actions](#2-actions)

[2.1. Action 1 (Deploy component)](#21-action-1-deploy-component)

[2.2. Action 2 (CI/CD)](#22-action-2-cicd)

[3. Workflow](#3-workflow)

[3.1. Deploy Component](#31-deploy-component)

[3.2. Deployment Pipeline](#32-deployment-pipeline)

[4. Troubleshooting](#4-troubleshooting)


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
## 1.5. References

| Reference No. | Document | Author(s) |
| --- | --- | --- |
| REF-1 | [About SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh) | GitHub |
| REF-2 | [About Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/about-secrets) | GitHub |
| REF-3 | [Understanding GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions) | GitHub |
| REF-4 | [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) | GitHub |


# 2. Actions
## 2.3. Defining Secrets
it necessary to define the following Github Secrets in the repository to be able to use the GitHub Actions:
* SSH\_PRIVATE\_KEY
* SSH\_HOST
* SSH\_USER
* PROJECT\_PATH

## 2.1. Action 1 (Deploy component)
The deployment of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 2.1.1. Purpose
This is a reusable action that integrates and deploys components described in the [CI/CD workflow ↗](#22-action-2-cicd)

### 2.1.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Action name | Deploy Component |
| Steps | ● Checkout repository<br>● Set up SSH <br>● Copy files to server<br>● Deploy component |
| Secrets | ● SSH\_PRIVATE\_KEY<br> ● SSH\_HOST <br> ● SSH\_USER <br>● PROJECT\_PATH |

## 2.2. Action 2 (CI/CD)
The deployment of this product is supported on the following operative systems and versions:

* Linux Ubuntu 20.04
* Linux Ubuntu 22.04(recommended)
* Linux Ubuntu 24.04

### 2.2.1. Purpose
This is a action that describes the services to be deployed in the machine.

### 2.2.2. Configured Values

The table below describes the values for your installation environment for future reference. (Note: recording of information throughout should be in keeping with your local policies for system documentation and password security). The following map describes the key, values used for the current service.

| Information | Value |
| --- | --- |
| Action name | Unified Deployment Pipeline |
| Jobs | ● deploy-databases<br>● deploy-lorawan-server<br>● deploy-mqtt-client<br>● deploy-api-emasa<br>● cleanup-volumes |

# 3. Workflow
Before implementing the CI/CD pipeline, it is necessary to define the correspondin [Github Secrets ↗](#23-defining-secrets) and [environment variables ↗](./Deployment%20Considerations.md) in the local repository

## 3.1. Deploy Component 
This actions are desined to run  on main branch push. Reusable workflows are used to deploy the components.
```yml
name: Deploy Component

on:
  workflow_call:
    inputs:
      component-path:
        required: true
        type: string
    secrets:
      SSH_PRIVATE_KEY:
        required: true
      SSH_USER:
        required: true
      SSH_HOST:
        required: true
      PROJECT_PATH:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Copy files to server
        run: |
          rsync -avz --delete \
          --exclude '.env.prod' \
          --exclude '**/.env.prod' \
          -e "ssh -o StrictHostKeyChecking=no" \
          ./ ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }}:${{ secrets.PROJECT_PATH }}

      - name: Deploy component
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'EOF'
            cd ${{ secrets.PROJECT_PATH }}/${{ inputs.component-path }}
            git pull origin main
            docker compose -f docker-compose.prod.yml pull
            docker compose -f docker-compose.prod.yml down
            docker compose -f docker-compose.prod.yml up -d
          EOF
```
## 3.2. Deployment Pipeline
This workflow defines the omponents to be deployed and their dependencies.
```yml
name: Unified Deployment Pipeline

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy-databases:
    uses: ./.github/workflows/deploy_component.yml
    with:
      component-path: 'persistance'
    secrets: inherit

  deploy-lorawan-server:
    needs: deploy-databases
    uses: ./.github/workflows/deploy_component.yml
    with:
      component-path: 'lorawan-server'
    secrets: inherit

  deploy-mqtt-client:
    needs: deploy-lorawan-server
    uses: ./.github/workflows/deploy_component.yml
    with:
      component-path: 'mqtt-client'
    secrets: inherit

  deploy-api-emasa:
    needs: deploy-lorawan-server
    uses: ./.github/workflows/deploy_component.yml
    with:
      component-path: 'api-rest-emasa'
    secrets: inherit

  cleanup-volumes:
    name: Cleanup Unused Docker Volumes
    needs: [deploy-mqtt-client, deploy-api-emasa]
    runs-on: ubuntu-22.04
    steps:
      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          
      - name: Prune unused Docker volumes
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'EOF'
            docker volume prune -f
          EOF

```
## 3.3. Activity Diagram
![Diagram](resources/SVG/github_actions_activity_diagram.svg)

## 3.4. Pipeline Diagram
![Diagram](resources/SVG/github_actions_workflow_diagram.svg)
# 4. Troubleshooting

Docker logs can be visualized either through the Docker Engine container information using the docker logs <container name> command, by Checking container information on Docker Desktop
```sh
docker logs –-follow <docker container name>
```
or by accessing the log files directly on the host system. On Linux Ubuntu, logs are located at
```sh
/var/lib/docker/containers/<container\_id>/<container\_id>-json.log
```