#!/bin/bash
# ec2 instance specific provisions

echo 'ec2_provision.sh start...' 

echo 'export IAMROLE=`curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/`' >> ~/.bashrc
echo 'export AWS_ACCESS_KEY_ID=`curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/$IAMROLE | grep '"'"'\"AccessKeyId\" : *'"'"' | cut -f5 -d '\" \"' | cut -b2- | rev | cut -b3- | rev`' >> ~/.bashrc
echo 'export AWS_SECRET_ACCESS_KEY=`curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/$IAMROLE | grep '"'"'\"SecretAccessKey\" : *'"'"' | cut -f5 -d '\" \"' | cut -b2- | rev | cut -b3- | rev`' >> ~/.bashrc
echo 'export AWS_SESSION_TOKEN=`curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/$IAMROLE | grep '"'"'\"Token\" : *'"'"' | cut -f5 -d '\" \"' | rev | cut -b2- | rev`' >> ~/.bashrc

#setup root virtualenv
cd ~/coincrunch
source setup

echo 'source $HOME/coincrunch/env/bin/activate' >> $HOME/.bashrc

echo 'ec2_provision.sh complete' 
