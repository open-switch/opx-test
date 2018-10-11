## Code Organization on your machine:

```bash

├── home
│   │   
│   └── jenkins                                 #New jenkins user to give root access to jenkins to run jenkins jobs
        │            										
        └── jenkins
            ├── ansible_jjb_template.yaml       #Template used to create jenkins job
            ├── basic-security.groovy           #Provide default username and password for the Jenkins GUI
            ├── install-plugins.sh              #Install Jenkins Plugins
            ├── jenkins_2.89.3_all.deb
            ├── jenkins.groovy
            ├── Jenkins-Jobs-ansible		#Stores the Jenkins Jobs created using GUI
            │   ├── jenkins_jobs.def
            │   ├── jenkins_jobs.ini
            │   └── macros.yaml
            ├── jenkins-support
            ├── plugins.txt
            └── Unified-Test-Application        #Stores Flask based GUI code
                ├── APIkey.sh
                ├── getmanagement.sh            
                ├── README.md                   #OPX test GUI description
                ├── templates                   #HTML code          
                └── ut-app.py                   #Main script to run Flask based GUI


```



(c) 2018 Dell Inc. or its subsidiaries. All Rights Reserved.
