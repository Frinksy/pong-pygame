#! /bin/bash

# Move all files to folder to be deleted
echo -ne "Removing older version... \r"
mkdir old && mv * old/ > /dev/null
rm -rf old > /dev/null

# Download, extract and then delete the archive
echo -ne "Downloading new version.. \r"
curl -O https://codeload.github.com/Frinksy/pong-pygame/zip/master > /dev/null
echo -ne "Extracting... \r"
unzip master > /dev/null
mv pong-pygame-master/* . > /dev/null
echo -ne "Cleaning up... \r"
rmdir pong-pygame-master > /dev/null
rm -rf master /dev/master > /dev/null
echo -ne "Done!"