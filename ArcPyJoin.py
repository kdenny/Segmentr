__author__ = 'kdenny'

def joinTracts(shploc,segloc,states,segments):
    ## Title: Census Bureau American Community Survey (ACS) API Automated Query Script
    ## Written By: Kevin Denny, Deloitte
    ## Support: kdenny@deloitte.com
    ##
    ## Description: Given a .csv file containing a list of names and table titles of ACS data fields, this script automatically queries the Census Bureau's API
    ## and populates data files for the provided data fields across every Census tract in the U.S. This script requires an API key from the Census Bureau and
    ## the Census Python package (available at https://pypi.python.org/pypi/census)

    ######################################################################################################################################################

    import arcpy
    import csv
    import os
    from datetime import datetime
    print ("Modules imported")


    for state in states:

        ifile = shploc + "tl_2015_{0}_tract.shp".format(state)
        ofile = shploc + state + "_TractsWData.shp"

        # cfile = csvloc + state + "DataFields_Result.csv"
        sfile = segloc + state + "_Segments.csv"

        fieldName = "GeoStr"
        fieldName2 = "Segment"
        fieldLength = 15

        if arcpy.Exists(ofile):
            arcpy.Delete_management(ofile)
            print "Old file deleted for {0}".format(state)

        if not arcpy.Exists(ofile):
            arcpy.Copy_management(ifile, ofile, "")
            print "File copied for {0}".format(state)

            arcpy.AddField_management(ofile, fieldName, "TEXT", "", "", fieldLength)
            print 'GEOID string field added for {0}'.format(state)

            for fn in segments:
                arcpy.AddField_management(ofile, fn, "DOUBLE", "", "", fieldLength)
            arcpy.AddField_management(ofile, fieldName2, "TEXT", "", "", fieldLength)

        # expression = "GetGeoString(!GEOID!)"
        # codeblock = """
        #     def GetGeoString(geoid):
        #         gstring = str(geoid)
        #         return gstring"""

        arcpy.CalculateField_management(ofile, fieldName, "str(!GEOID!)", "PYTHON")
        print 'GEOID string field calculated for {0}'.format(state)
        # arcpy.CalculateField_management(ofile, fieldName, "GetGeoString(!GEOID!)", "PYTHON_9.3", codeblock)


        fields = []
        for m in segments:
            fields.append(m)
        fields.append("Segment")
        listr = {}

        with open(sfile, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                li = {}
                for field in fields:
                    li[field] = row[field]
                listr[str(row['GEOID'])] = li

        rowst = arcpy.UpdateCursor(ofile) #this is my feature layer

        for cu in rowst:
            gid = cu.getValue("GeoStr")
            gi = gid.replace("u","")
            if gi in listr:
                seglist = listr[gi]
                for s in segments:
                  cu.setValue(s, seglist[s])
                  cu.setValue(fieldName2, seglist[fieldName2])
            elif gi not in listr:
                for y in segments:
                    cu.setValue(y, 0)
                    cu.setValue(fieldName2, "N/A")
            rowst.updateRow(cu)






