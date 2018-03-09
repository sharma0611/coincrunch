# This file defines the outputs from launching the EC2 instance module.

output "ec2_private_ip" {
  value = "${aws_instance.ec2_instance.private_ip}"
}

output "ec2_instance_public_dns" {
  value = "${aws_instance.ec2_instance.public_dns}"
}

output "ec2_instance_id" {
  value = "${aws_instance.ec2_instance.id}"
}
#
#data "aws_ebs_volume" "ebs_volume" {
#  most_recent = true
#
#  filter {
#    name   = "attachment.instance-id"
#    values = ["${aws_instance.ec2_instance.id}"]
#  }
#}
#
#output "ebs_volume_id" {
#  value = "${data.aws_ebs_volume.ebs_volume.id}"
#}
