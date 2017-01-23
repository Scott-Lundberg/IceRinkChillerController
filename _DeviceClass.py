/* A _Device is any component in the system, including sensors and relays.  
	Basic properties and methods are declared here: logging, database setup/teardown, 
		basic properties like Name, dbID, Type
*/

class Device:
	'Base class that all sensors, relays, and the controller itself are based off of'

	def __new__(TypeId,Name,Description):
		
