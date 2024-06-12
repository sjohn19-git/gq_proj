#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:08:09 2023

@author: sknoel
"""

import os
import sys
import signal
import pandas as pd

# Creates custom dataframe for prefered event hyopcenters, arrivals, and detections
# Dictates the basis of comparison dataframe structure for Dataframe_Compare

def event_dataframe(input_db):
   
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.path.append(os.environ['ANTELOPE'] + "/data/python")
    sys.path.append('/opt/antelope/5.11/data/python')
    import antelope.datascope as ds 
    
    with ds.closing(ds.dbopen(input_db, 'r')) as db:
        
         #Open antelope database tables needed to fully describe event parameters
         dborigin = db.lookup(table = "origin")
         dbevent = db.lookup(table = 'event')
         dbnetmag = db.lookup(table = "netmag")
         dbassoc=db.lookup(table = "assoc")
         dbarrival=db.lookup(table = "arrival")
         
         #Join database tables together
         dball = dborigin.join(dbevent, outer=True)
         dball = dball.join(dbnetmag, outer=True)
         dball=dball.join(dbassoc, outer=True)
         dball=dball.join(dbarrival, outer=True)
         #Subset to prefered origin solutions only
         dball = dball.subset('orid==prefor')
    
         #Count total records
         nrecs = dball.record_count
         print(input_db, nrecs)
    
         #Create zero array of length "nrecs" for each retrieved data value 
         lat = [0] * nrecs
         lon = [0] * nrecs
         depth = [0] * nrecs
         time = [0] * nrecs
         evid = [0] * nrecs
         nass = [0] * nrecs
         mag = [0] * nrecs
         etype = [0] * nrecs
         channel=[0]*nrecs
         stations=[0]*nrecs
         artime=[0]*nrecs
         phases=[0]*nrecs
     
         #Iterate through database records and pull out desired record
         for record in dball.iter_record():
             lat[record.record], lon[record.record] = record.getv("lat", "lon")
             depth[record.record], time[record.record] = record.getv("depth", "origin.time")
             evid[record.record], nass[record.record] = record.getv("evid", "nass")
             mag[record.record] = record.getv('ml')[0]
             etype[record.record] = record.getv('etype')[0]
             channel[record.record]=record.getv('chan')[0]
             stations[record.record]=record.getv('sta')[0]
             artime[record.record]=record.getv('arrival.time')[0]
             phases[record.record]=record.getv('phase')[0]
             
            #Combine records into CUSTOM DEFINED pandas dataframe
         db_dict = {'lat':lat, 'lon':lon, 'depth':depth, 'time':time, 'evid':evid, 'nass':nass, 'ml':mag, 'etype':etype,
                    'channel':channel, 'sta':stations, 'artime':artime, 'phases':phases}
         db_df = pd.DataFrame(db_dict)
         
    sys.path.remove(os.environ['ANTELOPE'] + "/data/python")
    sys.path.remove('/opt/antelope/5.11/data/python')
         
    return db_df


























    
