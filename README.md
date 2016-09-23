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
(TO BE REVISED)
Prerequisites:
 - installed virtualbox: https://www.virtualbox.org/
 - installed vagrant: https://www.vagrantup.com
 - connection to a squid proxy server
The last item is required to make CVMFS work. Usually this means that you
need to be connected to a network where the local site's squid proxy servers
are reachable from.
To check for the servers, login onto a node that has CVMFS installed and execute
```bash
grep -r CVMFS_HTTP_PROXY /etc/cvmfs/
# the output should be similar to this:
# CVMFS_HTTP_PROXY='http://<server 1>:<port>;http://<server 2>:<port>; etc
# check on your machine if you can access it via telnet
telnet <server> <port>
```
if yes, lets continue (if you do not have telnet installed, wait until you start up your vagrant box to test this).

```bash
# get the cmssw box:
wget https://cernbox.cern.ch/index.php/s/5SNj4MhjL8hJlmm/download -O cmssw.box
vagrant box add cmssw.box --name l1t/cmssw
rm -f cmssw.box
vagrant up
vagrant ssh
cd /vagrant
source bin/env.sh
```
