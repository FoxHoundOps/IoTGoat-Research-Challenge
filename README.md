# IoTGoat-Research-Challenge

This repository contains the documentation and automation scripts for the IoTGoat Research Challenge. The challenge involves performing a penetration test on IoTGoat, an intentionally vulnerable IoT firmware. The goal is to identify vulnerabilities, assess the security posture, and demonstrate possible exploitation scenarios. 

*Note: Unfortunately I was unable to complete this challenge in its entirety. With a full-time job, I was only able to dedicate a few hours in my evenings in the past week and some time on this Mother's Day weekend to work on this research challenge. I hope this report can still serve to provide insight into my approach and methodology in tackling similar problems.*


## Report

The [Report.md](Report.md) file in this repository contains a detailed report of the penetration test conducted on IoTGoat. It includes an overview of the target system, the methodology followed, findings, vulnerabilities discovered, and recommendations for remediation. The report provides valuable insights into the security assessment process and highlights the key aspects of the pentest.

## Scripts

The [scripts](scripts) directory contains various automation scripts developed to assist in the IoTGoat Research Challenge. These scripts automate specific tasks related to the pentest, making the assessment process more efficient and streamlined. Each script focuses on a particular aspect, such as backdoor detection, binary extraction, or shadow file retrieval.

### Contents

- [backdoor_checker.py](scripts/backdoor_checker/backdoor_checker.py): A script to automate backdoor detection by scanning network hosts for potential backdoor services.

- [extract_shadow.py](scripts/extract_shadow/extract_shadow.py): A script to automate the extraction of a binary file using Binwalk and locate the shadow file within it.

- [iot_goat.rules](iot_goat.rules): A collection of Snort rules to mitigate specific vulnerabilities in the IoTGoat application. It should be noted that these rules have not been tested due to time constraints. If I had more time, my approach would be to install Snort on my GL-MT1300 Beryl Router since it is running OpenWrt, and test it live. 

Feel free to explore the scripts directory for more details about each script and their usage.

## Attachments

The [Attachments](Attachments) directory contains images and supporting materials related to the IoTGoat Research Challenge. These attachments are referenced in the report and provide additional visual context to the findings and analysis.

## Usage

To use the automation scripts provided in this repository, follow the instructions provided in each script's respective README or code comments. Ensure that the necessary dependencies are installed, and refer to the specific usage examples for proper execution.
