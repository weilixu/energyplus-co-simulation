# energyplus-co-simulation
 Utilize the new EnergyPlus 9.6 python API, the project runs multi-threading EnergyPlus models and exchange data among the models at each timesteps.
 
# THIS CODE IS DEVELOPED AT VERY EARLY STAGE, PLLEASE USE IN CAUTIONS.

# Why do I need this package?
For community-scale study, we often want to understand how multiple buildings respond with one or multiple centralized system. Currently, tools around EnergyPlus can perform controls and energy management for one building, or batch simulations of energy saving measures at community scale. However, no tools seem to address the hourly energy or power analysis for community-based system controls.

# What does this package do?
This package allows user to fire up a number of energyplus simulations. Simulations can be separated into demand group and supply system. At every time step, the simulations at demand group will send values to the supply system, and supply system can apply supply strategy (sending back values is still under-development...) 

The data exchange can be between EnergyPlus models (demand group) and EnergyPlus models or other python scripts (supply system).

# How to use it?
## Prerequisite:
The package only works with EnergyPlus 9.6 - which has the built-in python package.

# Installation and kick off sample simulation
Download the pacakge.
1. Copy and paste the package to your EnergyPlus 9.6 folder, override the existing pyenergyplus folder.
2. You can leave the other files anywhere you want.
3. The example has three buildings, bldg 1 and bldg 2 are the demand side and bldg 3 is the supply side.
4. You can change the weather file by adding more weather files into the folder, or build up your own main.py
5. Kick off the main.py to run the sample simulation.

# Advanced technique
The HeatingSetpoint class in PythonPluginCustomSchedule1.py and PythonPluginCustomSchedule2.py shows a good example how to program an EnergyPlus plugin python script.
When there is a value to update from demand side, call ```python self.save_writer(state, "model_name", value)``` to send value to the supply side.

The HeatingSetpoint class in PythonPluginCustomSchedule3.py shows a good example how to program an Energyplus plugin python script for supply side.
When there is a need to check all the demand side data, call self.save_read(state).
