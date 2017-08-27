
##########################################
#####							  	 #####
#####     PROJECT - ITEM CATALOG     #####
#####                                #####
##########################################


1.0 ITEM CATALOG DESCRIPTION
- A web application to provide a list of catagories and items.
- The user can create, edit and delete for information created by them ONLY.
- And only view for items created by other users.
- It integrate to third-party provider for user registartion and authentication.  

2.0 INSTALLATION
- Please download the following software and install on your computer. Python 2.7, Vagrant and VirtualBox.
- Register with Google and Facebook for authentication. The link provided below.
- Follow the instruction to obtain the client id, etc.
Refer to below web site for more information:
2.1) https://www.vagrantup.com/docs/
2.2) https://docs.python.org/2/
2.3) https://www.virtualbox.org/wiki/Documentation
2.4) https://console.developers.google.com/project
2.5) https://developers.facebook.com/

3.0 GET STARTED
- Start up the Virtual Machine by "vagrant up".
- Follow by "vagrant ssh" to login to VM.
- Then, cd /vagrant/catalog to the directory consists of all the relevant files.
- Type "python ptdatabase.py" to create the database. And "python pt_samples.py" to load a list of dummy catalog items.
- Follow by "python powertools.py" to start the server.
- Browser to http://localhost:5000/

4.0  Additional info. JSON Endpoints
- Public users can view the catalog items as below.

4.1 Displays all the Powertools brand. 
	'/powertool/JSON'
4.2 Displays all Powertools items for specific brand (refer to their id display above). 
	'/powertool/<int:powertool_id>/menu/JSON'
4.3 Displays specific Powertool item of specific brand (refer to their id display above).
	'/powertool/<int:powertool_id>/menu/<int:menu_id>/JSON'

