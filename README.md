# single-row-facility-layout-solver

Single row facility layout problem solver written in python and node.js

# bringing up the testing SFTP server:

_the contents of ./docker-build/dev-sftp/sftp-contents will be mounted into the sftp server_ <br><br>
sudo systemctl enable docker <br>
sudo docker-compose up --build --force-recreate -d <br>

JEGYZET:

Az aplikáció lehetővé teszi a létesítmény elhelyezési probléma megoldását olyan emberek számára, akiknek nincs programozási illetve matematikai hátterük. Egy olyan feladatot old meg, amit nagyobb számokra nem lehet megközelíteni sem determinisztikusan. A program segítségével cégek képesek gépek gyárok, gépek, alkatrészek optimális vagy közel optimális elhelyezést találni.
