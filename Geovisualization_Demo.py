#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        Geovisualization Demo
# Purpose:     This script is created to demonstrate geovisualization with
#              Tkinter.
#
# Author:      johtran
# Contact:     johtran@deloitte.com
# Created:     01/18/2016
# Copyright:   Deloitte
#-------------------------------------------------------------------------------

import Tkinter as tk
import ttk
import struct
import math
import sys
import random

class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
    def __repr__(self):
        return "Point ({0}, {1})".format(self.x, self.y)
    def distanceto(self, otherpoint):
        """Find the distance btween this point and another point."""
        return math.sqrt((otherpoint.x-self.x)**2+(otherpoint.y-self.y)**2)

class LineSegment(object):
    def __init__(self, startpoint, endpoint):
        self.p1 = startpoint
        self.p2 = endpoint
        self.length = self.p1.distanceto(self.p2)
    def overlap(self, otherlinesegment):
        small = min(self.p1.y, self.p2.y)
        big = max(self.p1.y, self.p2.y)
        if small<otherlinesegment.p1.y<big or small<otherlinesegment.p2.y<big:
            return True
        else:
            return False

class Polyline(object):
    def __init__(self):
        pass
    def length(self):
        i, length = 1, 0;
        while i<len(self.x):
            length = length + math.sqrt((self.x[i]-self.x[i-1])**2 + (self.y[i]-self.y[i-1])**2)
            i = i+1
        return length;

def read_shp(shapefile):
    """Reads the .shx (index) portion of a shapefile to determine:
        - The number of features (feat_num)
        - The bounding box (xmin, ymin, xmax, ymax)
        - The record offset (record_offset)
        - The record content length (record_content_length)
       Then reads the main shapefile (.shp) portion of a shapefile to obtain:
        - Number of parts (part_num)
        - Number of points (point_num)
        - Index of parts (part_index)
        - X, Y coordinates in a list of [x1, y1, x2, y2, ...] (coords)"""
    shapefile = shapefile.replace(".shp", "").replace(".shx", "")
    shapefile_shx = shapefile+".shx"
    shapefile_shp = shapefile+".shp"

    f = open(shapefile_shx,'rb')
    f.seek(24)
    s = f.read(4)
    b = struct.unpack('>i',s)
    featNum = (b[0]*2-100)/8
    s = f.read(72)
    c = struct.unpack('<iidddddddd',s)
    minx, miny, maxx, maxy = c[2],c[3],c[4],c[5]
    offsets = []
    contentLengths = []
    for i in range(0,featNum):
        f.seek(100+i*8)
        s = f.read(8)
        offset,contentLength = struct.unpack('>ii',s)
        offsets.append(offset*2)
        contentLengths.append(contentLength*2)
    f.close()

    f = open(shapefile_shp,'rb')
    f.seek(100)
    polygonstates=[]
    for i in range(featNum):
        f.seek(offsets[i]+44)
        s = f.read(8)
        b = struct.unpack('<ii',s)
        polyline=Polyline()
        polyline.numParts,polyline.numPoints = b[0],b[1]
        strj = '<'
        for j in range(polyline.numParts):
            strj = strj+'i'
        s = f.read(4*polyline.numParts)
        polyline.partsIndex = struct.unpack(strj,s)
        polyline.x, polyline.y = [],[]
        polyline.partsPointsList = []
        for l in range(polyline.numParts):
            numPoints = 0
            if(l < polyline.numParts -1):
                numPoints = polyline.partsIndex[l + 1] - polyline.partsIndex[l]
            else:
                numPoints = polyline.numPoints - polyline.partsIndex[l]
            polyline.partsPointsList.append(numPoints)
        if len(polyline.partsPointsList) == 1:
            for k in range(polyline.numPoints):
                s = f.read(16)
                pointx, pointy = struct.unpack('dd',s)
                polyline.x.append(pointx)
                polyline.y.append(pointy)
            polygonstates.append(polyline)
        else:
            for m in polyline.partsPointsList:
                polylinePart = Polyline()
                polylinePart.x, polylinePart.y = [], []
                for n in range(m):
                    s = f.read(16)
                    pointx, pointy = struct.unpack('dd',s)
                    polylinePart.x.append(pointx)
                    polylinePart.y.append(pointy)
                polygonstates.append(polylinePart)
    f.close()
    return polygonstates

def create_canvas(polygonstates, choropleth_var="crime_rate"):
    """Create main window object for visualization. Colors vary by choropleth value."""

    root = tk.Tk()
    windowwidth = 700
    windowheight = 500
    can = tk.Canvas(root, width = windowwidth, height = windowheight)

    maxx, maxy, minx, miny = -sys.maxint-1, -sys.maxint-1, sys.maxint, sys.maxint
    for state in states:
        statemaxx = max(state.x)
        statemaxy = max(state.y)
        stateminx = min(state.x)
        stateminy = min(state.y)
        if statemaxx > maxx:
            maxx = statemaxx
        if statemaxy > maxy:
            maxy = statemaxy
        if stateminx < minx:
            minx = stateminx
        if stateminy < miny:
            miny = stateminy

    ratiox = (maxx - minx)/windowwidth
    ratioy = (maxy - miny)/windowheight

    if ratiox > ratioy:
        ratio = ratiox
    else:
        ratio = ratioy

    #Loops through each polyline and creates a list of [x1,x2,x3,...] and [y1,y2,y3,...]
    statesdrawn = [] #Creates list to store all drawn features
    colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "A", "B", "C", "D", "E", "F"]
    colorrange = [i+j for i in colors for j in colors]
    for i in range(0, len(polygonstates)):
        linexstates = polygonstates[i].x
        lineystates = polygonstates[i].y
        #Transforms each x and y value to window coordinates
        linextransstates = [(eachx - minx)/ratio for eachx in linexstates]
        lineytransstates = [(maxy - eachy)/ratio for eachy in lineystates]
        linetransstates = []
        #Creates a list in the form [x1,y1,x2,y2,x3,y3,...] for display in Tkinter and then creates lines
        for j in range(len(linextransstates)):
            linetransstates.append(linextransstates[j])
            linetransstates.append(lineytransstates[j])
        choroplethvalue = getattr(polygonstates[i], choropleth_var)
        choroplethfillvalue = colorrange[int(choroplethvalue*len(colorrange))]
        a = can.create_polygon(linetransstates, fill="#0000{0}".format(choroplethfillvalue), outline="#FFFFFF", width=0.1) # Creates polygon from list of points
        statesdrawn.append(a) #Appends drawn features in the drawn features list for use later on

    can.grid(row=0, column=0)
    root.mainloop()

if __name__== "__main__":
    states = read_shp("esri_us_states.shp")
    for state in states:
        # Pretend crime rate is a variable we want to use for choropleth colors
        state.crime_rate = random.random()
    create_canvas(states, "crime_rate")
