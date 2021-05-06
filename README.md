# single-row-facility-layout-solver
Single row facility layout problem solver written in python and node.js

# bringing up the testing SFTP server:
*the contents of ./docker-build/dev-sftp/sftp-contents will be mounted into the sftp server* <br><br>
sudo systemctl enable docker  <br>
sudo docker-compose up --build --force-recreate -d  <br>