National Airspace Trajectory-Prediction System(NATS)

Utility Program

NATS Management Web
===================
NATS Management Web Server, by default, is started when users start NATS Server(the run script).
The default URL of NATS Management Web Server is http://127.0.0.1:3000
Users can use a web browser to connect to the NATS management web to use management/utility/maintenance operations.


Utility: Create Wind Files
==========================
createWindFiles.py
	Provide a command-line functionality to download wind files from NOAA and convert them to NATS-compatible HDF5 format.

    Syntax:
    $./createWindFiles.py ./ ---> Download the current wind data and 
                                 forecasted wind data for the next 21 hours 
                                 from the current UTC time to the current directory (./).
                                 Further this will process the GRIB2 files and create .h5 files 
                                 from them to be used in NATS. This last functionality
                                 uses the windtool module from NATS and has to be compiled. 
                                 
    $./createWindFiles.py ./ 2018-04-09,9 ---> Download wind data from 9th April 2018 9 hours UTC
                                               all the way upto current UTC time to the current directory.
    
    
    $./createWindFiles.py ./ 2018-04-09,9 2018-04-12,17---> Download wind data from 9th April 2018 9 hours UTC 
                                                            to 12th April 2018 17 hours UTC to the current directory.