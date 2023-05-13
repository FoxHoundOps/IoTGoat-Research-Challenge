*Note: Unfortunately I was unable to complete this challenge in its entirety. With a full-time job, I was only able to dedicate a few hours in my evenings in the past week and some time on the weekend to work on this research challenge. I hope this report can still serve to provide insight into my approach and methodology in tackling similar problems. 

# IoTGoat Research Challenge Report

## Introduction

The IoTGoat Project is a deliberately insecure firmware based on OpenWRT and maintained by OWASP. It serves as a platform to educate and train software developers and security professionals by testing commonly found vulnerabilities in IoT devices. The challenges are based on OWASP IoT Top 10. 

## Objective

The objective of this challenge is to showcase my own approach and research methodologies. I will then try to develop automated tests and exploits that I ran manually, as well as provide Snort IDS rules to detect the vulnerabilities and exploits that I create. 

## Setup

For this challenge I used VMWare Workstation to run my Kali Linux attacker box and I used a physical Raspberry Pi 3 Model B+ running the IoTGoat firmware. I used a GL-MT1300 Beryl to connect these two devices together to run this challenge on its own private network isolated from my home network. In summary, the three devices used for setting up this challenge are:
1) Raspberry Pi Model B+ (Running IoTGoat firmware)
2) Kali Linux Virtual Machine running with VMWare Workstation on a Windows 10 host
3) GL-MT1300 Beryl Router for connecting the above devices in an isolated network (Running OpenWrt)
![](setup.jpg)

Machine Details:
|IP|Hostname|Operating System|
|---|---|---|
|192.168.171.131|IoTGoat|Linux
|192.168.171.133|kali|Kali Linux (attacker box)

# High-Level Summary

I was tasked with performing an internal penetration test towards IoTGoat.
The focus of this test is to perform attacks, similar to those of a hacker and attempt to infiltrate an IoT device.
My overall objective was to evaluate the identify vulnerabilities, exploit flaws, automate the exploits, create Snort IDS rules for mitigation, and report the findings back to CyberadAPT.

When performing the internal penetration test, there were several alarming vulnerabilities that were identified on IoTGoat.
When performing the attacks, I was able to gain shell access to both user level account 'iotgoatuser' and administrator level account 'root'.
During the testing, I discovered a backdoor with administrative level access.
The system was successfully exploited.

# Methodologies

I utilized a widely adopted approach to performing penetration testing that is effective in testing how well the IoTGoat is secured.
Below is a breakdown of how I was able to identify and exploit the variety of systems and includes all individual vulnerabilities found.

## Information Gathering

I began my test with information gathering and tried to locate as much information I could on the system under test. As with any system, information can be gathered without touching the system itself. It can be advantageous to research documentation and user guides to gather information about the system. This type of reserach can provide valuable insight into what services exist on the system, how to interact with the services, how the services interact with one another, and possibly default user accounts and/or credentials. 

In my OSINT research, the official OWASP GitHub Wiki page for IoTGoat (https://github.com/OWASP/IoTGoat/wiki) contained the most valuable information for my test. Since this is designed to have various challenges, the Wiki has information about how to start, but it it important to remember a real-world system could possibly also have valuable information out on the Internet. 

![](challenges_page.png)

## Static Analysis

Because we know that IoTGoat is a firmware that can be flashed, we can download the latest precompiled firmware release from https://github.com/OWASP/IoTGoat/releases. I will be downloading "[IoTGoat-raspberry-pi2.img](https://github.com/OWASP/IoTGoat/releases/download/v1.0/IoTGoat-raspberry-pi2.img)".

![](releases.png)

With prior experience in static analysis and also participating in CTF events, I believe the tool 'binwalk' would be worthwhile to try:

![](binwalk_output.png)
We can see that binwalk was able to successfully extract the filesystem from the .img file! It extracted everything into a directory "\_IoTGoat-raspberryp-pi2.img.extracted/":
![](extracted_filesystem.png)
We can now look through the filesystem and search for anything of value. Some of the most valuable places to look in a Linux file system are `/etc/passwd` and `/etc/shadow`. Let's try to read the contents of these files:

![](passwd_shadow.png)
We now have some valuable information from this static analysis! We know that there are two users with accomanying password that are created when the firmware is flashed (iotgoatuser and root), and we have the MD5 hashes of these accounts. If time was not an issue and I had access to powerful GPUs for password cracking, running something like hashcat or johntheripper would be more feasible, but for the purposes of this particular challenge I will refrain from password cracking for now and instead take my win of knowing that there is a user `root` and a user `iotgoatuser`:

##### Users
|Username|Where Found?|Notes|
|---|---|---|
|iotgoatuser|/etc/shadow|binwalk extraction
|root|/etc/shadow|binwalk extraction

##### Password Hashes
|Hash|Hash Type|Where Found?|Notes|
|---|---|---|---|
|root:\$1\$Jl7H1VOG$Wgw2F/C.nLNTC.4pwDa4H1|MD5|/etc/shadow|binwalk extraction
|iotgoatuser:\$1\$79bz0K8z$Ii6Q/if83F1QodGmkb4Ah.|MD5|/etc/shadow|binwalk extraction

## Service Enumeration

The service enumeration portion of a penetration test focuses on gathering information about what services are alive on a system or systems.
This is valuable for an attacker as it provides detailed information on potential attack vectors into a system.
Understanding what applications are running on the system gives an attacker needed information before performing the actual penetration test.
In some cases, some ports may not be listed.

Typically when doing challenges and practicing my penetration testing (HackTheBox, TryHackMe), since there is no need to evade detection and there is no risk of setting off any alarms, I like to run my nmap scans as such:

`nmap -sC -sV -p- <IP ADDRESS> -oA nmap/<hostname>`

- -sC: Enables the default set of NSE (Nmap Scripting Engine) scripts against the target host to gather information and perform basic security checks
- -sV: Enables service version detection
- -p-: Scann all 65,535 TCP ports

**Nmap Scan Results:**
![](nmap_results.png)
Server IP Address | Ports Open
------------------|----------------------------------------
192.168.117.131       | **TCP**: 22, 53, 80, 443, 5000, 5515

The nmap scan reveals the above ports as open, many of which are standard services that may exist. However, the interesting one is port 5515, where nmap is unable to detect what service is running on that port. In our full nmap output there is an interesting section with respect to this port:

![](5515.png)
This looks very interesting and I will definitely explore this further in the next phase - manual testing!

## Manual Testing

### Port 5515: Unknown Service
As mentioned above, nmap detected an 'unknown' service running on port 5515 and we saw indication of a possible backdoor:
![](5515.png)

Because this service is unknown and we know nothing about what could be here, it's possible to connect to it with `netcat` and see if there is some banner or interaction we can get:

![](backdoor.png)
Upon connecting with `netcat` we are greeting with a "Successfully Connected to IoTGoat's Backdoor" message. We still don't know yet what it is that we connected to, but something to try is running shell commands, which we find works. I ran `id` which will display the user and group identity of the connected user who issued the command (in this case, we find we are root!).

**Vulnerability Explanation:**
IoTGoat has a built-in backdoor and since this is a firmware that is flashed, any device using this will also have this backdoor. This vulnerability exposes a critical security issue in the IOTgoat application, as it allows an attacker to gain unrestricted access to the system. With root-level privileges, an attacker can execute arbitrary commands, modify system configurations, access sensitive data, and potentially compromise the entire system.

**Vulnerability Fix:**
Remove the backdoor from the IOTgoat application. This involves identifying the entry point, closing the open port (5515), and removing any associated code or configuration that allows unauthorized access.

**Severity:**
Very High

### Port 22: SSH
In our static analysis we were able to identify two users (root, iotgoatuser). These users may be able to SSH into the device, and if we had enough time to crack their password we might be able to use those password to get SSH access. What we can try though is to see if any of these users use insecure or leaked password that are publically known. In my search, I decided to try to ask ChatGPT if it could point me in the right direction:

![](cgpt.png)
The Mirari Botnet password are actually included in SecLists, and I have SecLists installed on my Kali machine. I'll try to use Hydra to brute force these password for both root and iotgoatuser. mirai-botnet.txt is not in a usable format for hydra, however. I want to take mirai-botnext.txt and take only the second column of it and write it to a new file 'mirai-botnet-passwords.txt'. I can use the 'cut' tool to do this:

![](mirai_cut.png)

Now that I have the password in a usable format I can run hydra. Running these password against the root user yielded no matches, but the user iotgoatuser did:

![](hydra.png)
## Passwords Found
|Username|Password|Service|Notes|
|---|---|---|---|
|iotgoatuser|7ujMko0vizxv|ssh|Hydra with mirai botnet creds|

Now we can proceed to try to login ourselves with these credentials and find that they do work:
![](iotgoatuser_ssh.png)
**Vulnerability Explanation:**
A significant vulnerability was discovered that allows unauthorized access to the SSH service using the known username "iotgoatuser" and passwords commonly associated with the Mirai botnet. 

The presence of the "iotgoatuser" account with weak or default passwords that match those used by the Mirai botnet indicates poor security practices. This vulnerability highlights several security concerns:

1.  Weak or Default Passwords: The fact that the Mirai botnet passwords were effective in accessing the SSH service suggests that weak or default passwords were used for the "iotgoatuser" account. Default or easily guessable passwords significantly compromise the security of the system and expose it to unauthorized access.
2.  Failure to Monitor and Limit Failed Login Attempts: The successful use of Hydra to perform a brute force attack indicates a lack of effective security controls to detect and mitigate such attacks. Proper monitoring of failed login attempts and implementing account lockout mechanisms can help protect against brute force attacks and limit the effectiveness of such intrusion attempts.

**Vulnerability Fixes:**
1. Password Policy Enhancement: Enforce strong password policies across the system, including minimum password length, complexity requirements, and regular password rotation. Discourage the use of default or easily guessable passwords and educate users on selecting strong, unique passwords.
2. Account Lockout Mechanisms: Implement account lockout mechanisms that temporarily lock user accounts after a certain number of failed login attempts. This can help prevent brute force attacks by significantly delaying an attacker's ability to guess passwords.
3. Intrusion Detection and Monitoring: Implement intrusion detection systems (IDS) or intrusion prevention systems (IPS) to monitor and alert on suspicious login activities, including failed login attempts, brute force attacks, or account compromise attempts.
4. Security Awareness and Training: Provide security awareness and training to system administrators and users to promote good security practices, including the importance of strong passwords, avoiding default credentials, and understanding the risks of weak authentication mechanisms.

**Severity:**
High

### Sensitive Information
With user-level access (iotgoatuser), I began enumerating the live filesystem and searching for any sort of interesting files. I began looking for configuration files, database files, custom scripts, and cronjobs. I usually begin by running manual commands and poking around before running some type of enumeration script, such as LinEnum.sh (https://github.com/rebootuser/LinEnum). 

In my manual search, I identified some interesting database (.db) files:

![](find_db.png)

-   `find`: This is the command used to search for files and directories.
-   `/`: Specifies the starting point for the search, in this case, the root directory.
-   `-iname *.db`: This is an option for the `find` command. The `-iname` flag performs a case-insensitive search, and `*.db` is the pattern used to match files with a `.db` extension. This means it will match files like `file.db`, `database.db`, etc.
-   `-type f`: Another option for the `find` command. The `-type f` flag filters the search results to include only regular files (excluding directories and other types of files).
-   `2>/dev/null`: Redirects the standard error (stderr) output to `/dev/null`, effectively discarding any error messages that may occur during the search. This prevents error messages from being displayed on the terminal.

This "sensordata.db" file might contain some interesting information. I will use scp to copy this file back to my Kali attacker box:

![](scp_fail.png)

I got the above error and had to do some research online on how to resolve it. Fortunately I found a resolution with an explanation:

![](scp_resolve.png)

After adding the `-O` flag, I was able to successfuly copy the file to my machine:
![](scp_working.png)

Now with this file on my local attacker machine, I can run sqlite3 on this file and dump its contents:
![](db_dump.png)
We have discovered some sensitive information including names, emails, and birthdates:

|Name|Email|Where Found?|Birthdate|
|---|---|---|---|
|johnsmith|johnsmith@gmail.com|/usr/lib/lua/luci/controller/iotgoat/sensordata.db|1/31/1977
|jillsmith|jillsmith@gmail.com|...|4/14/1979
|walter|waltergary@yopmail.com|...|32821969
|WilliamRonald|billronald@yopmail.com|...|11/14/1989
|Test|TstUser@aol.com|...|12/12/1990
|Sgt|sgtmajor@us.gov|...|10/17/1956

**Vulnerability Explanation:**
During the penetration test, a vulnerability was discovered that allowed a database file containing sensitive information, including names, email addresses, and birthdates, to be copied to a remote machine and subsequently dumped. This vulnerability poses a significant security risk as it exposes personally identifiable information (PII) and creates opportunities for misuse, including phishing attacks.

**Vulnerability Fixes:**
1) Access Controls and Data Encryption: Review and strengthen access controls to ensure that sensitive data, such as the database file, is accessible only to authorized individuals. Implement robust encryption measures to protect the confidentiality and integrity of sensitive data at rest and in transit.
2) Data Monitoring and Logging: Implement comprehensive monitoring systems and logging mechanisms to track and record access to sensitive data. Monitor for suspicious or unauthorized activities, including file access and transfer, and generate alerts or notifications for timely response and investigation.

