#AWS
variable "aws_region"                 {default = "us-west-1"}
variable "public_key_path"            {default = "~/.ssh/shivam.pub"}

# Resource Tags
variable "owner_contact"              { default = "sharma.shivam0611@gmail.com" }
variable "project"                    { default = "coincrunch"}
variable "maid_offhours"              { default = "tz=et"}

# Instance details
variable "key_name"                   { default = "shivam_key" }
variable "iam_instance_profile"       { default = "sharma0611" }
variable "subnet_id"                  { default = "subnet-f90fb590" }
variable "security_groups"            { default = "sg-22c2c247" }
variable "instance_type"              { default = "t2.micro" }
variable "availability_zone"          { default = "us-west-1a" }
variable "root_block_device_vol_size" { default = 20 }

#ebs details
variable "ebs_delete_on_termination"  { default = false }
variable "ebs_block_device_vol_size"  { default = 30 }
variable "ebs_device_name"            { default = "/dev/sdg"}

# bootstrap the ec2 instance
variable "ec2_user_data"              { default = "user_data.sh"}

