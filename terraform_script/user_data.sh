#!/bin/bash

echo 'Updating proxy...'
echo '# start configurations' >> /home/admin/.bashrc
echo 'export no_proxy="localhost,127.0.0.1,169.254.169.254,s3.amazonaws.com"' >> /home/admin/.bashrc
echo '# end configurations' >> /home/admin/.bashrc
#set the following to $HOME if you do not want EBS instance to have anything
echo 'export MYWORKDIR=$HOME' >> /home/admin/.bashrc
echo 'cd $MYWORKDIR' >> /home/admin/.bashrc
source /home/admin/.bashrc

#EC2
echo "Install base applications..."
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade
apt-get install python3-pip python3-dev python-virtualenv -y
apt-get install postgresql-client libpq-dev -y
apt-get install htop -y
apt-get install zip -y
apt-get install git -y
apt-get install curl -y

echo "apt-get applications complete" 
su - admin -c 'git clone -b master --single-branch https://github.com/sharma0611/coincrunch.git'
su - admin -c 'bash ~/coincrunch/terraform_script/ec2_provision.sh'

#EBS
#to start the EBS for first time
#mkfs -t ext4 /dev/xvdg
#mkdir /opt/mount1
#mount /dev/xvdg /opt/mount1
#chown -R admin:admin /opt/mount1
#echo /dev/xvdg  /opt/mount1 ext4 defaults,nofail 0 2 >> /etc/fstab
#su - admin -c 'bash ~/rtpm-datascience-terraform/ebs_provision.sh'

#to remount EBS after it exists
#sudo mkdir /opt/mount1
#sudo mount /dev/xvdg /opt/mount1

echo "user_data.sh complete" 

#commands created to run program
echo 'Now running coincrunch suite:'
source /home/admin/.bashrc
cd ~/coincrunch
python coincrunch.py'
