#!/usr/bin/env python
# author: Peter M. Petrakis <peter.petrakis@gmail.com>
# license: None, use however you see fit
# description: Demonstrates pexpect's ability to automate SAN failover
# SAN is already configured for public key ssh access

import sys, time
sys.path.insert(1,'/usr/share/autotest/client/common_lib')
import pexpect

host='10.232.43.25'

#XXX The reason that there's no abstraction for the prompt
# is I have to manage the text before the '#' and after for
# regexp. If I figure out a neat code efficient breadcrumb
# solution, or someone contributes it...

with open('/tmp/workfile', 'w') as f:
  print "logging in..."
  child = pexpect.spawn('ssh ' + host, logfile=f)
  child.expect('acrab#')
  print "logged in"

  # must enter config mode to twiddle vsan
  child.sendline('config t')
  child.expect('acrab\(config\)#.+', timeout=5)
  print "entered config mode"
  
  child.sendline('vsan database')
  child.expect('acrab\(config-vsan-db\)#.+', timeout=5)

  print "enable both vsans, wait 30 secs"
  child.sendline('no vsan 10 suspend')
  child.sendline('no vsan 20 suspend')
  time.sleep(30)

  print "disable vsan 10, wait 60 secs"
  child.sendline('vsan 10 suspend')
  child.expect('acrab\(config-vsan-db\)#.+', timeout=5)

  time.sleep(60)

  print "enable vsan 10"
  child.sendline('no vsan 10 suspend')
  child.expect('acrab\(config-vsan-db\)#.+', timeout=5)

  print "exit config mode"
  child.sendline('end')
  child.expect('acrab#.+', timeout=5)

  print "exit fc switch"
  child.sendline('exit')
  print "terminated %s" % child.terminate()

# vim:ts=2:sw=2:et:filetype=python:
