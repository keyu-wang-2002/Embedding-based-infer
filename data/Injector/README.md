Injector 

**Command**: 

java -cp \<kaon2 library>;<mysql-jdbc library>;. ConflictAdder <db name> <#conflicts> <owl file/url>...<owl file/url>

\<kaon2 library> : A *.jar file packing the whole KAON2 DL reasoner. It is generally the following file: kaon2.jar

\<mysql-jdbc library> : A *.jar file connecting MySQL to JAVA, as described in the Dumper tool.

\<db name> : The MySQL database in which the ABox of the given ontology is stored.

\<#conflict> : The number of conflicts to be inserted to the ABox. A conflict is a set of assertions violating a (inverse) functional restriction or a disjointness constraint specified in the TBox.

\<owl file/url > : A OWL file or URL storing (a part of) the ABox of the given KB.


**Running Environment**

Sun Java SE (version 1.5.0 or above)
MySQL (version 5.0 or above) and Connector/J (version 5.0 or above)
KAON2 (version 2007-1-25)
Running Preparation
Download the KAON2 OWL reasoner from the above link and put the mysql-jdbc library (unpacked from the MySQL Connector/J package) into the directory where KAON2 locates. Unpack the download package into the directory where KAON2 locates. Edit mysql.ini to set the host, user name and password for the MySQL database in which the ABox of the given KB is stored using the Dumper tool.


**Running Example**

Continue the previous running example on the Dumper tool. Suppose all files are prepared as described above, and the ABox of the test KB has been stored in MySQL database lubmlite, as the previous running example has done. This example shows how to insert 1000 conflicts to a KB whose ABox has been stored in MySQL database lubmlite.

Ensure that all owl files in the previous running example are still available at the subdirectory lubmlite1.
Type the following command (set -Xmx smaller if the available memory is less than 1GB; change ";" to ":" in the command if the operating system is not Windows):
java -Xms256m -Xmx1024m -cp kaon2.jar;mysql-connector-java-5.0.3-bin.jar;. ConflictAdder lubmlite 1000 lubmlite1/*.owl