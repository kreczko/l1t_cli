# l1t_cli
CLI for the L1Trigger (offline) based on [hepshell](https://github.com/kreczko/hepshell).

For available commands, execute `l1t help` (after setup).

# Setup on Scientific Linux 6/7
```bash
git clone https://github.com/kreczko/l1t_cli.git
cd l1t_cli
source bin/env.sh
```

# interactive mode
The l1t_cli comes with an interactive mode that allows for auto-completion of commands.
To use it simply execute `l1t <enter>`.


# Setup on OS X/Ubuntu/Windows
## Prerequisites:
 - installed virtualbox: https://www.virtualbox.org/
 - installed vagrant: https://www.vagrantup.com

## run

```bash
# get the CERNVM box
vagrant up
vagrant ssh
# if you need AFS, do this first time only:
sudo mkdir /afs
sudo /sbin/chkconfig afs on
sudo /sbin/service afs start
# now time to do some work
cd /vagrant
source bin/env.sh
```
For some of the recipes you will be required to interact with github.
For the recipes to work correctly you will need to define

```bash
# Please set up your full name via:
git config --global user.name '<your name> <your last name>'
# Please set up your email via:
git config --global user.email '<your e-mail>'
# Please set up your GitHub user name via:
git config --global user.github <your github username>

```
