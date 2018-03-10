provider "aws" {
  region                   = "${var.aws_region}"
}

# dynamically get AMIs
#module "ami" {
#  source        = "git"
#  account       = "prod"
#  version       = "latest"
#  region        = "us-west-1"
#  distribution  = "ubuntu1604"
#}

resource "aws_key_pair" "auth" {
 key_name = "${var.key_name}"
 public_key = "${file(var.public_key_path)}"
}

resource "aws_instance" "ec2_instance" {
  ami                     = "ami-94bdeef4"
  availability_zone       = "${var.availability_zone}"
  instance_type           = "${var.instance_type}"
  key_name = "${aws_key_pair.auth.id}"
#  iam_instance_profile    = "${var.iam_instance_profile}"
#  subnet_id               = "${var.subnet_id}"
  vpc_security_group_ids  = ["${split(",", var.security_groups)}"]
  user_data               = "${file("user_data.sh")}"
  
  root_block_device = {
    volume_size           = "${var.root_block_device_vol_size}"
  }

  tags = {
    "OwnerContact"        = "${var.owner_contact}"
    "Project"             = "${var.project}"
  }

  ebs_optimized           = false 

#only needed to create EBS in first place
#  ebs_block_device {
#    device_name           = "${var.ebs_device_name}"
#    volume_type           = "gp2"
#    volume_size           = "${var.ebs_block_device_vol_size}"
#    encrypted             = true
#    delete_on_termination = "${var.ebs_delete_on_termination}" 
#  }
}

#only needed to reattach persistent EBS with vol-id

