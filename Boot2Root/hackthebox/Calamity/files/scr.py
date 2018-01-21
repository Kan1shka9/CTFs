#!/usr/bin/python
import os
import time
from datetime import datetime
while True:
        time.sleep(2)
        x=os.popen("netstat -pantu").read()
        os.system("chmod 333 /tmp");
        for line in x.split('\n'):



                name="fafafafa"
                pid="fafafafa"
                try:
                        name=line[line.index('/')+1:]
                        pid=line[:line.index('/')]
                        pid=pid[pid.rfind(' '):]

                except ValueError:
                        dummylol="dummy";


                try:
                        kill=name[:line.index(' ')-1]

                        if kill=="nc"  or kill=="sh" or kill=="/bin/sh" or kill=="/bin/nc" or "python" in name or "bash" in name or "dash" in name or "tmux" in name or  "ruby" in name:

                                out="POSSIBLE INTRUSION BY BLACKLISTED PROCCESS "+name+"...PROCESS KILLED AT "+str(datetime.now())+'\n'
                                file = open('/home/xalvas/intrusions', 'a')
                                file.write(out)
                                file.close()
                                os.system("kill -9"+pid)
                                dummylol="dummy";

                except ValueError:
                        dummylol="dummy";