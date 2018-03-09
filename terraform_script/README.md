# coincrunch-terraform
TF Scripts to provision ETL with EC2 Instance to pipeline data to RDS instance


#### Purpose
To help spin up ETL environment for coincrunch. You can do it manually too, but this is
meant to speed things up.


#### Basics
Make sure you have Terraform installed:
```
# on a Mac
brew terraform
```

You should have a file as such for your AWS credentials:
```
ls -la ~/.aws/credentials
```


#### Usage
```bash
cd coincrunch/terraform_script

# pulls dependencies
terraform get -update

# validate
terraform plan

# build the resources requested
terraform apply

# cleanup once if you don't need the resource anymore
terraform destroy
```
