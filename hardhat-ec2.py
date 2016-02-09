#!/usr/bin/env python
import os
import sys
import click
import boto3

SECURITY         = ['launch-wizard-4']
IMAGE            = 'ami-c9b572aa' 
INSTANCE_TYPE    = 't2.micro'   
PLACEMENT        = {'AvailabilityZone': 'ap-southeast-1a'}
KEY_NAME         = 'adam'
BOOT_SCRIPT = """\
#!/bin/bash
sudo yum -y update
sudo yum -y install git
sudo git clone https://github.com/bryanhann/foo.git /tmp/hardhat
sudo git clone https://github.com/bryanhann/foo.git /hardhat
source /hardhat/dot_profile
touch /tmp/bch-foo.$RANDOM
ls /tmp
"""


ec2 = boto3.resource('ec2')


@click.group()
def cli():
    pass

@cli.command()
def create():
    print
    print 'Starting an EC2 instance of type {0} with image {1}'.format(INSTANCE_TYPE, IMAGE)
    print 
    print "This will cost you money. Press enter to continue."
    print
    raw_input()
    exit(4)
    ec2.create_instances(
        UserData=BOOT_SCRIPT,
        ImageId=IMAGE,
        InstanceType=INSTANCE_TYPE,
        Placement=PLACEMENT,
        MinCount=1,
        MaxCount=1,
        KeyName=KEY_NAME,
        SecurityGroups=SECURITY,
    )

@cli.command()
def ssh():
    print
    print "STARTING SSH TO EC2 INSTANCE"
    print "It may be necessary to run the following commands:"
    print "\tsudo yum update"
    print "\tsudo yum install git"
    print
    SSH_HOME=os.environ['HOME'] + '/.ssh'
    for ii in ec2.instances.all():
        if ii.public_dns_name:
            cmdline = """ssh -i "%s/%s.pem" ec2-user@%s""" % ( SSH_HOME, ii.key_name, ii.public_dns_name )
            os.system(cmdline)

cli.add_command(ssh)
cli.add_command(create)




if __name__=='__main__':
    cli()

