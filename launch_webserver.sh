if [ "${1}" == "load" ]
then
  #load
  sudo -s launchctl load -w /System/Library/LaunchDaemons/org.apache.httpd.plist
else
  #unload
  sudo -s launchctl unload -w /System/Library/LaunchDaemons/org.apache.httpd.plist
fi
