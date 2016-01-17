__author__ = 'kdenny'

def getACS_base(outLoc=r"\\ussltcher8002fs.dan.sltc.com\FASGeoSpatial\Segmentation\Dependencies\Params", inStates):
    """
     Title: Census Bureau American Community Survey (ACS) API Automated Query Script
     Written By: Kevin Denny, Deloitte
     Support: kdenny@deloitte.com

     Description: Given a .csv file containing a list of names and table titles of ACS data fields, this script automatically queries the Census Bureau's API
     and populates data files for the provided data fields across every Census tract in the U.S. This script requires an API key from the Census Bureau and
    ## the Census Python package (available at https://pypi.python.org/pypi/census)
    """

    from census import Census
    from us import states
    import csv
    import os
    from datetime import datetime

    # A key can be obtained at http://api.census.gov/data/key_signup.html
    # c = Census("YOUR KEY HERE")
    c = Census("fc35b71dfc10725453726fd1e8bcb1c6063db66f")

    fipsLoc = r'\\ussltcher8002fs.dan.sltc.com\FASGeoSpatial\Segmentation\Dependencies\Params\fips_codes.csv'
    dataLoc = r'\\ussltcher8002fs.dan.sltc.com\FASGeoSpatial\Segmentation\Dependencies\Params\dataFields.csv'

    indic = 'SegmentIndicators' ## This is the name of the .csv file you will create for each county; update for each different type (e.g. Economic, Housing)
    opath = os.path.join(outLoc, "DataFiles")

##    print ("Do you wish to overwrite existing ACS files? ")
##    ow = raw_input("(Y/N) ").upper()
##    assert ow in ["Y", "N"], "Overwrite user input must be 'Y' or 'N'"

    datum = []
    datumNames = []
    statesCounties = []

    ## print("Start")
    ## print(datetime.now().time())

    # Populate list of states and counties
    with open(fipsLoc, "r") as csvfile:
        for b in inStates:
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            for row in reader:
                tempAr = []
                curState = str(row['State FIPS Code'])
                curCounty = str(row['County FIPS Code'])
                ## if curState == b:
                tempAr.append(curState)
                tempAr.append(curCounty)
                if tempAr not in statesCounties:
                    statesCounties.append(tempAr)
    ## print(statesCounties)

    # Populate list of datum fields / datum names
    with open(dataLoc, "r") as csvfile2:
        reader2 = csv.DictReader(csvfile2)
        for rowa in reader2:
            datum.append(str(rowa['TableID']))
            datumNames.append(str(rowa['DatumName']))

    # Creates any necessary folders / subfolders
    finStates = []
    finCounties = []
    for ss in inStates:
        if not os.path.exists(opath):
            os.makedirs(opath)
        fname = os.path.join(opath, str(ss)+"_"+'DataFields.csv')
        # print(datetime.now().time())
        # print(fname)
        # print ("")
        texta = ''
        textb = ''
##        if (os.path.isfile(fname) and ow == 'Y') or (os.path.isfile(fname) == False):
##            os.remove(fname)
        if not os.path.isfile(fname):
            # if not os.path.isfile(fname):
            textb = textb + 'State,County,Tract'
            k = 0
            while k < len(datum):
                textb = textb + ',' + datumNames[k]
                k += 1

            textb = textb + '\n'
            n = open(fname, 'w')
            n.write(textb)
            n.close()

            # Begin creating data file for county
            for sd in statesCounties:
                texta = ''
                allVars = []
                if  str(sd[0]) == int(ss):
                    state = str(sd[0]).zfill(2)
                    county = str(sd[1]).zfill(3)

                    # Process tracts
                    l = 0
                    while l < len(datum):
                        aString = c.acs.state_county_tract(datum[l], state, county, Census.ALL)
                        allVars.append(aString)
                        l += 1

                    ## print ("Done processing tracts for" + state + ", " + county)
                    ## print allVars
                    ## print (datetime.now().time())

                    tracts = []

                    a = 0
                    listOfVars = []

                    # Cleans up data results

                    for vark in allVars:
                        tempList = []
                        for s in vark:
                            if a == 0:
                                tr = s['tract'].replace("u","")
                                tracts.append(str(tr).zfill(6))

                            md = s[datum[a]]
                            tempList.append(md)
                            if md == 'None':
                                tempList.append('0')
                        listOfVars.append(tempList)
                        a += 1

                    f = 0

                    # Writes API query results as a string
                    while f < len(tracts):
                        texta = texta + state + "," + county + "," + str(tracts[f]).zfill(6)
                        g = 0
                        while g < len(datum):
                            texta = texta + "," + str(listOfVars[g][f])
                            g = g + 1
                        f = f + 1
                        texta = texta + "\n"

                    # Exports results string to the identified output file
                    m = open(fname, 'a')
                    ## print fname
                    ## print texta
                    m.write(texta)
                    m.close()

            print ("ACS Data gathered for ") + str(ss)
        else:
            return



