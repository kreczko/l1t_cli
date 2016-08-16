# l1t-cli
CLI for the L1Trigger (offline)

For available commands, execute `l1t help`.

# Setup on SL6/7
```bash
git clone https://github.com/kreczko/l1t_cli.git
cd l1t_cli
source bin/setup.sh
source bin/env.sh
```


# Setup on OS X/Ubuntu/Windows
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
# first time only
source bin/setup.sh
source bin/env.sh
```
