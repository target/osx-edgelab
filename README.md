# EDGE Lab preview
Needing a way to utilize OS X test machines based on our standard deployment (without deploying hardware or having users make their own VMs), and lacking any enterprise options, we looked to do it ourselves. Special thanks to Joseph Chilcote, for [vfuse](https://github.com/chilcote/vfuse), which provides the basis for much of this.

## What it does
As this is a preview, this playbook will assume the following requirements at this point. We plan to have this in a more complete state soon.

### Requirements:
1. You have a machine setup with VMWare Fusion on it and have added it to the [fusion] group in your hosts file.
2. You've setup Guacamole already and added it to the [guacamole] group in your hosts file.

## Running the playbook
Within the directory, run `ansible-playbook vm_build.yml`. You'll need to define your variables in `vars/fusion.yml` using the example provided in `vars/fusion_example.yml`.

## What's not done yet
- A play to provision the Fusion machine. Should be easy, just haven't done it yet.
- A play to build Guacamole isn't done yet. I have the build documented, so hope to have that updated soon.
- Front end that can trigger creation and provide creds to the user.
- Module to remove machine from JSS and delete VM.

### Version
0.0.1
