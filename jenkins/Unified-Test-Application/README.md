### Code Organization
#### Very first step- Use [setup.sh](../../setup.sh) for setting up the environment 
Use: **wget** setup.sh_raw_file_link to get the script and run it to set up the enviroment required by the opx test infra.

##### Run the Flask based app: 
```
python ut-ap.py
```
The script ut-app.py launches GUI on port 80, reads the playbooks in the /etc/ansible/playbook folder to display on GUI and creates jenkins jobs for the selected tests.

* **To view the app on browser use:** http://127.0.0.1 or http://mgmt-ip

* The App runs on **port 80**, you can modify the port by changing the line *app.run(host="0.0.0.0", port=80)* in ut-app.py

The App is self-explanatory and easy to use threfore no seperate document on how to use the App.

![test-infra-opx](https://user-images.githubusercontent.com/14809064/46426350-267ed900-c6f3-11e8-8ca4-d96325effa91.PNG)


(c) 2018 Dell Inc. or its subsidiaries. All Rights Reserved.
