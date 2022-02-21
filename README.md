# IOS_Audit_Run
 
 Python Code that allows Network Engineers to run through their ACI Infrastructure for Layer 1 availability and compare to a set of interfaces that reflects their tenant computing a health score
 


## Overview



**Device/Interface Health**: 

The idea of the health check is to provide visibility into possible layer 1 problems within the network fabric. The script runs to check for interfaces that are down and compares them with expected set of interfaces and computes a health percentage score. 

**Python**

The script is written in python using acitoolkit to interact with APIC,and computation based on defined set of interfaces.

**Output**: The results of the CLI commands are stored in simple .txt file: (L1_Output.txt, L1_Health.txt) ![Sample Output](Output_Snapshot.JPG)

You can also find the results of a full run in the text file (Result.txt)

## Contacts
*Oluyemi Oshunkoya (yemi_o@outlook.com)

## Solution Components
*Python
*

## Prerequisites 

ACITOOLKIT

Python3.6 and above

## Step 1 - Downloading - Option A Using a Docker Image

1. Download the latest version of the PYATS from docker hub

$ docker pull ciscotestautomation/pyats:latest

2. Run the docker image 

$ docker run -it ciscotestautomation/pyats:latest /bin/bash

## Step 1 - Downloading - Option B Using GIT

1. Clone the repository

git clone https://github.com/datacenter/acitoolkit.git

2. Install ACITOOLKIT library

cd acitoolkit
python setup.py install

## Step 2 - Script Setup

1. Clone this repository into your desired directory using the command:

git clone https://github.com/yzmar4real/ACI_LAYER1_CHECK.git

2. CD into the directory 

cd ACI_LAYER1_CHECK

3. (Optional) Use the directory as a virtual environment for the project

python3 -m venv . 

4. (Optional) Start the virtual environment and install the requirements for the project

source bin/activate

6. Execute the main script from console

python3 Main.py 
