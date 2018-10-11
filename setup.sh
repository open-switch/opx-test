#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

echo "#### Adding user Jenkins with root permission ######"
sudo useradd jenkins  -m -s /bin/bash
echo "jenkins:jenkins" | sudo chpasswd

sudo sed -i '/# See sudoers(5) for more information on "#include" directives:/ a jenkins ALL=(ALL) NOPASSWD: ALL' /etc/sudoers

sleep 0.5

sudo apt-get update

echo "#### Installing Git ######"
sudo apt-get -y install git

sudo apt-get install -y python-pip python-dev

sudo apt-get install -y default-jre \
    default-jdk \
    unzip \
    wget \
    git \
    python-software-properties \
    debconf-utils \
    zip \
    vim \
    ssh \
    unzip \
    tcl-dev \
    tk-dev \
    tclx8.4 \
    traceroute \
    curl

sleep 0.5
sudo apt-get -y install python-pexpect
sleep 0.5
sudo pip install jinja2 toposort six

getHost=$(hostname -f)
echo $getHost

export DEBIAN_FRONTEND=noninteractive
debconf-set-selections <<< "postfix postfix/mailname string $getHost"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
apt-get -y install postfix

sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
sudo apt-get install -y oracle-java8-installer
sudo update-alternatives --config java <<< '2'

sudo echo JAVA_HOME="/usr/lib/jvm/java-8-oracle" >> /etc/environment
sudo echo JENKINS_UC_DOWNLOAD="https://updates.jenkins-ci.org" >> /etc/environment
source /etc/environment

sudo wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
sudo echo deb http://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list

echo "#####Git clone test repo#####"
sudo git clone https://github.com/open-switch/opx-test.git  /tmp/opx-test
if [ $? -ne 0 ]; then
    echo "Git clone of opx-test repo failed, make sure you have git installed"
fi
sudo mv /tmp/opx-test/jenkins /home/jenkins/

echo "####INSTALLING ANSIBLE####"
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get -y install ansible
sudo mv /tmp/opx-test/* /etc/ansible/

echo "Installing Jenkins 2.89.3 version"
sudo apt-get update
sudo apt-get -y install daemon
sudo dpkg -i /home/jenkins/jenkins/jenkins_2.89.3_all.deb
sleep 30

#sudo cd /var/lib/jenkins
sudo cp /var/lib/jenkins/config.xml /home/jenkins/
sudo mkdir /var/lib/jenkins/init.groovy.d

sudo cp /home/jenkins/jenkins/basic-security.groovy /var/lib/jenkins/init.groovy.d/

sudo cp /home/jenkins/jenkins/install-plugins.sh /usr/local/bin
sudo cp /home/jenkins/jenkins/plugins.txt  /usr/local/bin
sudo cp /home/jenkins/jenkins/jenkins-support  /usr/local/bin
sudo service jenkins restart

sleep 10

sudo apt-get update
sudo bash /usr/local/bin/install-plugins.sh $(cat /usr/local/bin/plugins.txt | tr '\n' ' ')

sudo sed -i '/JAVA_ARGS="-Djava.awt.headless=true/c\JAVA_ARGS="-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false"' /etc/default/jenkins

sudo cp /home/jenkins/config.xml /var/lib/jenkins/
sudo service jenkins restart

echo "###DONE with JENKINS installation###"
sleep 0.5

echo "###Try the jenkins GUI by going to http://127.0.0.1:8080###"

echo "####installing jenkins-job-builder####"

sudo pip install jenkins-job-builder
[ "$?" != 0 ] && echo "Failed to install jenkins job builder" && exit 1

sleep 0.5

echo "####Adding the email extension templates to jenkins folder####"

sudo cp -rf /home/jenkins/jenkins/Unified-Test-Application/jenkins.model.JenkinsLocationConfiguration.xml /var/lib/jenkins/
sleep 0.5
cmd=$(traceroute -f 1 -m 1 8.8.8.8 | awk '{print $2}'| grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
cmd1=$(ip route show | grep $cmd|grep -oP '(?<=src).*'| awk '{print $1}')
sed -i "s/IP/$cmd1/g" /var/lib/jenkins/jenkins.model.JenkinsLocationConfiguration.xml
sudo service jenkins restart
sleep 1

sudo cp -rf /home/jenkins/jenkins/Unified-Test-Application/email-templates /var/lib/jenkins/
sudo cp -rf /home/jenkins/jenkins/Unified-Test-Application/hudson.plugins.emailext.ExtendedEmailPublisher.xml /var/lib/jenkins/
sudo service jenkins restart
sleep 1

echo "#####Installing FLASK####"
sudo pip install flask
[ "$?" != 0 ] && echo "Flask instalaltion failed" 

echo "####Launch Flask app. using this command:  python /home/jenkins/jenkins/Unified-test/ut_app.py &####"
chmod +x /home/jenkins/jenkins/Unified-Test-Application/ut-app.py
nohup /home/jenkins/jenkins/Unified-Test-Application/ut-app.py &

echo "#####Lauch flask using web GUI- http://127.0.0.1######"

exit 0

