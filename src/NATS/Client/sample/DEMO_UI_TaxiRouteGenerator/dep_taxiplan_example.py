#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example illustrates how to use NATS functions for plotting airport layout and
design a user-designed taxi plan. This compares the user-designed taxiplan with the one
generated by the shortest path, which is a default method employed in NATS.

Author: Jun Yang
Date: 03/28/2018
"""

import jpype as jp
import PlotHelpers as ph
import matplotlib.pyplot as plt
import os

#Preamble. Modify the client directory
#a directory where NATS_Client jar files are located.
client_dir='PLEASE_ENTER_PATH_TO_NATS_CLIENT_HERE'
classpath =client_dir+"dist/nats-client.jar"+":"+client_dir+"dist/nats-shared.jar"+":"+client_dir+"dist/json.jar"+":"+client_dir+"dist/rmiio-2.1.2.jar"+":"+client_dir+"dist/commons-logging-1.2.jar"

#b directory in which Center and Sector data are located
data_dir = './data'

#starts JVM
#----------------------------------------------------------------------------------------
jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath)

NATSClientFactory = jp.JClass('NATSClientFactory')
natsClient = NATSClientFactory.getNATSClient()

natsClient.login("admin")

#----------------------------------------------------------------------------------------------
# TaxiPlan Design Example starts here
#
# Step 1. From aircraftInterface load TRX file and select an aircraft.
equipmentInterface=natsClient.getEquipmentInterface()
ac_if = equipmentInterface.getAircraftInterface()  # aircraft interface
if (not (ac_if)):
    print("cannot get AircraftInterface from NATS server")
ac_if.load_aircraft("share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx", "share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx")
ac_names=ac_if.getAllAircraftId()
print("acs:{} are loaded".format(ac_names))

#select the first aircraft
ac_instance=ac_if.select_aircraft(ac_names[0])

#Obtain the airport for the above aircraft
environmentInterface = natsClient.getEnvironmentInterface()
airportInterface=environmentInterface.getAirportInterface()

dep_arpt_name=airportInterface.getDepartureAirport(ac_names[0])
dep_arpt_instance=airportInterface.select_airport(dep_arpt_name) #Airport Instance
print(" AC:{} departs from {}".format(ac_instance.getAcid(),dep_arpt_name))


#Step 2. Airport Interface Example
#Read the airport layout for the above aircraft
arpt_nodemap=None;arpt_nodedata=None;arpt_linkdata=None

#obtaiirport layout by the following calls.
#node_map: provides mapping between node_name and node_number.
#node data: node_number,lat_deg,lon_deg
#link_data: link is specified as the line between two nodes.
arpt_nodemap=airportInterface.getLayout_node_map(dep_arpt_name)
arpt_nodedata=airportInterface.getLayout_node_data(dep_arpt_name)
arpt_linkdata=airportInterface.getLayout_links(dep_arpt_name)
rwy_data=airportInterface.getAllRunways(dep_arpt_name)
#Step 3. From the obtained airport layout data, instantiate AirportLayout object.
#from PlotHelpers
arpt_surf=ph.AirportLayout(dep_arpt_name)
arpt_surf.initialize_from_NATS_airport_layout(arpt_nodemap,arpt_nodedata,arpt_linkdata,rwy_data)
arpt_surf.set_altitude_ft(dep_arpt_instance.getElevation())

#Step 4. Design from the airport layout
#
#5. Plot and Save Options
#5.a Specify whether center and/or sector boundaries are displayed on the background.
#---------------------------
include_center=True
include_sector=False

##5.b
#The figure allows for the user to design a taxi plan and save. For saving the designed plan, set
#the following True.
#
write_route_to_file=True

#5.c The airport layout can also be written to a kml file that can be uploaded to Google MyMaps for
# looking at the layout with respect to builds and roads provided by Google Maps.
write_arpt_to_kml=True


#Step 6. Plot
#a.load center data
if include_center:
    centerfile = os.path.join(data_dir,'Centers_CONUS')
    #in Default, include center boundaries
    center_handle = ph.RegionHandler()
    center_handle.read_region_file(centerfile,'CENTER')

#b. load sector data
if include_sector:
    sectorfile = os.path.join(data_dir,'SectorData')  # large file. takes time in loading and plotting
    sector_handle = ph.RegionHandler()
    sector_handle.read_region_file(sectorfile,'SECTOR')

#c. Airport Layout and Route Design
fig=plt.figure(0)
fig.set_size_inches(9*12/7,9)
ax=fig.add_axes([0.05,0.05,0.9,0.9])
ax.set_facecolor('black')
#a.center plot and/or sector plot
include_center=True
if include_center:
    center_handle.plot_regions(plt,color='w')
if include_sector: #takes long time to plot
    sector_handle.plot_regions(plt,color='m')
#b.plot airport layout
#arpt_surf.plot_airport_layout(plt)
arpt_surf.plot_airport_for_taxiroute_design(plt,airportInterface,ac_instance)

#c. when the route design is completed, the default route is also computed and compared

plt.show()



if write_route_to_file:
    if arpt_surf.have_a_designed_route():
        arpt_surf.write_taxiRoute_to_csv(arpt_surf.get_airport_name()+"_dep_designed_taxi_route.csv")
if write_arpt_to_kml:
    if arpt_surf:
        arpt_surf.write_airport_layout_to_kml()


natsClient.disConnect()
#JVM shutdown
jp.shutdownJVM()
