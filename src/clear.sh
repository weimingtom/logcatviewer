svn st | grep ^? | cut -c 2- | grep -v dm.log |xargs rm -rf
