# IoTGoat-Research-Challenge

This repository contains the documentation and automation scripts for the IoTGoat Research Challenge. The challenge involves performing a penetration test on IoTGoat, an intentionally vulnerable IoT firmware. The goal is to identify vulnerabilities, assess the security posture, and demonstrate possible exploitation scenarios.

## Report

The [Report.md](Report.md) file in this repository contains a detailed report of the penetration test conducted on IoTGoat. It includes an overview of the target system, the methodology followed, findings, vulnerabilities discovered, and recommendations for remediation. The report provides valuable insights into the security assessment process and highlights the key aspects of the pentest.

## Scripts

The [scripts](scripts) directory contains various automation scripts developed to assist in the IoTGoat Research Challenge. These scripts automate specific tasks related to the pentest, making the assessment process more efficient and streamlined. Each script focuses on a particular aspect, such as backdoor detection, binary extraction, or shadow file retrieval.

### Contents

- [backdoor_checker.py](scripts/backdoor_checker/backdoor_checker.py): A script to automate backdoor detection by scanning network hosts for potential backdoor services.

- [extract_shadow.py](scripts/extract_shadow/extract_shadow.py): A script to automate the extraction of a binary file using Binwalk and locate the shadow file within it.

Feel free to explore the scripts directory for more details about each script and their usage.

## Attachments

The [Attachments](Attachments) directory contains images and supporting materials related to the IoTGoat Research Challenge. These attachments are referenced in the report and provide additional visual context to the findings and analysis.

## Usage

To use the automation scripts provided in this repository, follow the instructions provided in each script's respective README or code comments. Ensure that the necessary dependencies are installed, and refer to the specific usage examples for proper execution.

