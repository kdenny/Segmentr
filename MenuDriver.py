__author__ = 'kdenny'

import os
import shutil

coeffNew = {}
segmentsList = []
variablesList = []
paths = {}
variableClassBreaks = {}

def addVarToData(vard):
    if vard not in variablesList:
        variablesList.append(vard)
    co = getCoefficients()
    ns = {}
    nss = {}
    for key in co:
        ns = co[key]
        ns[vard] = 0
        nss[key] = ns
    setCoefficients(nss,co)


def addVarClassesToData(vard, varclasses):
    variableClassBreaks[vard] = varclasses

def getVarClasses():
    return variableClassBreaks

def getCoefficients():
    if len(coeffNew) == 0:
        initCoefficients()
    return coeffNew

def addSegm(sy):
    segmentsList.append(sy)

def setPaths(pa):
    for p in pa:
        paths[p] = pa[p]

def getVariables():
    if len(variablesList) == 0:
        g = getCoefficients()
        for keyr in g:
            if keyr not in variablesList:
                variablesList.append(keyr)
        # initCoefficients()
    return variablesList

def getSegments():
    if len(segmentsList) == 0:
        initCoefficients()
    return segmentsList

def initCoefficients():
    import csv
    coeffFile = paths["Params"] + "coefficients.csv"
    with open(coeffFile, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            liy = {}
            for m in row:
                if m != "Segment":
                    liy[m] = row[m]
                    variablesList.append(m)
            coeffNew[row['Segment']] = liy
            if row['Segment'] not in segmentsList:
                segmentsList.append(row['Segment'])

def setCoefficients(new,old):
    if len(coeffNew) == 0:
        initCoefficients()
        old = getCoefficients()
    for a in old:
        if a in new:
            coeffNew[a] = new[a]
            print(a + " is in new")
        else:
            coeffNew[a] = old[a]
    for b in new:
        coeffNew[b] = new[b]

    print coeffNew

def getAvailStates(datad):
    sa = []

    shpath = datad + "Shapefiles/"

    src_files = os.listdir(shpath)
    for file_name in src_files:
        # full_file_name = os.path.join(src, file_name)
        if file_name[8:10] not in sa:
            sa.append(file_name[8:10])
        # if (os.path.isfile(full_file_name)):
        #     shutil.copy(full_file_name,ppath)

    return sa

def fipsToText(fips,paths):
    import csv
    te = ""
    fi = int(fips)
    floc = paths["Params"] + "fips_codes.csv"
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if int(row['State FIPS Code']) == fi:
                te = row['State Abbreviation']
    return te

def calcHotspots(paths,states,segl):
    import arcpy

    shpath = paths["Shapefiles"]

    for state in states:
        input_fc = shpath + "{0}_TractsWData.shp".format(state)
        tpath = shpath + "Centroids/"
        if not os.path.exists(tpath):
            os.makedirs(tpath)
        output_fc = tpath + "{0}_Hotspot.shp".format(state)
        print ("Calculating hotspot for ")
        for segy in segl:
            arcpy.HotSpots_stats(input_fc, segy, output_fc)


        # cursor = arcpy.da.SearchCursor(input_fc, ["SHAPE@XY", "GEOID"])
        # centroid_coords = []
        # ccoords = {}
        #
        # for feature in cursor:
        #     centroid_coords.append(feature[0])
        #     # print "GID"
        #     # print feature[1]
        #     ccoords[feature[1]] = feature[0]
        #
        # pointGeometryList = []
        # fieldLength = 15
        #
        # # for pt in centroid_coords:
        # #     point.X = pt[0]
        # #     point.Y = pt[1]
        # #
        # #     pointGeometry = arcpy.PointGeometry(point)
        # #     pointGeometryList.append(pointGeometry)
        # coos = []
        # gids = []
        # for gid in ccoords:
        #     point = arcpy.Point()
        #     coord = [ccoords[gid]]
        #     co = coord[0]
        #     print "Coord"
        #     print coord
        #     point.X = co[0]
        #     print point.X
        #     point.Y = co[1]
        #     print point.Y
        #     gids.append(gid)
        #     coos.append[co]
        #
        #     pointGeometry = arcpy.PointGeometry(point)
        #     pointGeometryList.append(pointGeometry)
        #
        # if not arcpy.Exists(output_fc):
        #         rname = "{0}_TractCentroids.shp".format(state)
        #         arcpy.CreateFeatureclass_management(tpath, rname, "POINT", "", "", "", input_fc)
        #         # arcpy.Copy_management(pointGeometryList, output_fc, "")
        #
        #         cursor = arcpy.da.InsertCursor(output_fc, ['GID', 'SHAPE@XY'])
        #         count = 0
        #         for cow in coos:
        #             cursor.insertRow((gids[count], cow))
        #
        #         # print ('Field created for point shapefile for {0}'.format(fipsToText(state)))
        #         # print "File copied for {0}".format(state)
        #
        #
        #
        # # for a in segl:
        # #     arcpy.AddField_management(output_fc, a, "DOUBLE", "", "", fieldLength)
        # #     # print 'Segment fields added to point shapefile for {0}'.format(fipsToText(state))
        # #     hotspotfile = shpath + "{0}_{1}_Hotspots.shp".format(state,a)
        # #     if not arcpy.Exists(hotspotfile):
        # #         # print 'Hotspots created for segment {0) in {1}'.format(seg, fipsToText(state))
        # #         arcpy.OptimizedHotSpotAnalysis_stats(output_fc, hotspotfile, a)

def textToFips(te,paths):
    import csv
    fips = ""
    floc = paths["Params"] + "fips_codes.csv"
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row['State Abbreviation'] == te:
                fips = str(row['State FIPS Code']).zfill(2)
    # print "Fi: " + str(fi)
    return fips

# def getSegments(floc):
#     floc2 = floc + "coefficients.csv"
#     import csv
#     segs = []
#     with open(floc2, 'rU') as infile:
#         reader = csv.DictReader(infile)
#         for row in reader:
#             if row['Segment'] not in segs:
#                 segs.append(row['Segment'])
#     # print "Fi: " + str(fi)
#     return segs

def createFolders(path):
    # print path[-1:]
    paths = {}

    if not os.path.exists(path):
        os.makedirs(path)
    paths["Main"] = path

    dpath = path + "DataFiles/"
    if not os.path.exists(dpath):
        os.makedirs(dpath)
    paths["Data"] = dpath

    spath = path + "Segments/"
    if not os.path.exists(spath):
        os.makedirs(spath)
    paths["Segments"] = spath

    shpath = path + "Shapefiles/"
    if not os.path.exists(shpath):
        os.makedirs(shpath)
    paths["Shapefiles"] = shpath

    ppath = path + "Params/"
    if not os.path.exists(ppath):
        os.makedirs(ppath)
    paths["Params"] = ppath

    src = 'C:/Users/kdenny/Documents/SegmentrBase/Params/'

    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            nfilename = ppath + file_name
            if (os.path.isfile(nfilename)) == False:
                shutil.copy(full_file_name, ppath)

    return paths

def printr(f):
    print(f)

def readSegments(floc):
    import csv
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        segs = []
        for row in reader:
          segs.append(row['Segment'])
    return segs

def getACSDataFields(paths):
    import csv
    floc = paths["Params"] + "dataFields.csv"
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        dataFields = {}
        for row in reader:
            dataFields[row["DatumName"]] = row["TableID"]
    return dataFields

def createSegments(paths,states,cn):
    import sys
    import csv
    import numpy as np
    import os
    from ArcPyJoin import joinTracts as joinr

    def rmse(predictions, targets):
        t = 0
        vals = []
        for p in predictions:
            val = np.sqrt(((p - targets[t]) ** 2))
            vals.append(val)
            t = t + 1

        m = sum(vals)/float(len(vals))

        return m

    def calcColumns(fname,fname2):
        if os.path.isfile(fname2):
            os.remove(fname2)
        with open(fname,'r') as csvinput:
            with open(fname2, 'w') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)

                all = []
                head = ''

                counta = 0
                for row in reader:
                    if counta == 0:
                        head = row
                        head.append('MedInc')
                        head.append('EdPop')
                        head.append('PSomeCol')
                        head.append('PColPlus')
                        head.append('PPostGrad')
                        head.append('GEOID')
                        all.append(head)

                    if counta != 0:
                        # Ed pop = Pop - Pop under 18 - (current UG students)
                        medi = row[head.index("Median_Income")]
                        hs = int(row[head.index("Population_Completed_High_School")])
                        sc = int(row[head.index("Population_Completed_Some_College")])
                        asd = int(row[head.index("Population_With_Associates_Degree")])
                        bach = int(row[head.index("Population_With_Bachelors_Degree")])
                        msd = int(row[head.index("Population_With_Masters_Degree")])
                        doc = int(row[head.index("Population_With_Doctorate_Degree")])
                        ug = int(row[head.index("Enrolled_In_Undergraduate")])
                        pu18 = int(row[head.index("Population_Under_18")])
                        tpop = int(row[head.index("Total_Population")])

                        st = str(row[head.index("State")]).zfill(2)
                        co = str(row[head.index("County")]).zfill(3)
                        tr = str(row[head.index("Tract")]).zfill(6)


                        edpop = float(tpop - pu18 - ug)
                        gid = str(st) + str(co) + str(tr)
                        if edpop != 0:
                            psomecol = float((sc + asd + bach + msd + doc) / edpop)
                            pcolplus = float((bach + msd + doc) / edpop)
                            ppostgrad = float((msd + doc) / edpop)
                        if edpop == 0:
                            psomecol = float(0)
                            pcolplus = float(0)
                            ppostgrad = float(0)
                        row.append(medi)
                        row.append(edpop)
                        row.append(psomecol)
                        row.append(pcolplus)
                        row.append(ppostgrad)
                        row.append(gid)
                        # print row
                        all.append(row)
                    counta = counta + 1

                writer.writerows(all)
        print "Columns calculated in " + fname
        return head


    def calcScores2(ids,urb,inc,ed,ag,segmentWeights,coeffFile,ocT):
        # coeffFile = r"C:\Users\kdenny\Documents\PostalSegmentation\Params/coefficients.csv"
        n = 0
        segments = {}
        while n < len(urb):
            segs = {}
            if len(cn.keys()) == 0:
                with open(coeffFile, "rb") as fo:
                    reader = csv.reader(fo)
                    next(reader, None)
                    for line in reader:
                        seg = str(line[0])
                        predictions = [float(urb[n]), float(inc[n]), float(ed[n]), float(ag[n])]
                        targets = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]
                        for key in ocT:
                            classym = ocT[key]
                            predictions.append(float(classym[n]))
                            targets.append(float(classym[n]))
                        # a = (float(urb[n]) * float(line[1])) + (float(inc[n]) * float(line[2])) + (float(ed[n]) * float(line[3])) + (float(ag[n]) * float(line[4]))
                        b = rmse(predictions,targets)
                        segs[seg] = b / float(segmentWeights[seg])
            elif len(cn.keys()) != 0:
                skey = []
                for lkey in cn:
                    liner = cn[lkey]
                    seg = lkey
                    # print "You win!"
                    for hkey in liner:
                        if hkey not in skey:
                            skey.append(hkey)
                    # print "Skey"
                    # print skey
                    # print liner
                    pns = [float(urb[n]), float(inc[n]), float(ed[n]), float(ag[n])]
                    trgs = [float(liner["Urban"]), float(liner["Income"]), float(liner["Education"]), float(liner["Age"])]
                    predictions = []
                    targets = []
                    col = 0
                    for prw in pns:
                        if trgs[col] != 0:
                            predictions.append(prw)
                            targets.append(trgs[col])
                        col = col + 1


                    # targets.append(float(liner["Urban"]))
                    # targets.append(float(liner["Income"]))
                    # targets.append(float(liner["Education"]))
                    # targets.append(float(liner["Age"]))
                    for key in ocT:
                        classym = ocT[key]
                        # print "Length"
                        # print(len(classym))
                        # print(classym)
                        # print liner
                        if (liner[key] != 0):
                            predictions.append(float(classym[n]))
                            targets.append(float(liner[key]))
                    # targets.append(float(liner[skey.index("Urban")]))
                    # # targets.append(float(liner[skey.index("Urban")]))
                    # targets.append(float(liner[skey.index("Income")]))
                    # targets.append(float(liner[skey.index("Education")]))
                    # targets.append(float(liner[skey.index("Age")]))
                    # print("Deezy")
                    # print(targets)
                    # print(predictions)
                    # targets = [float(line2["Urban"]), float(line2["Income"]), float(line2["Education"]), float(line2[["Age"]])]
                    b = rmse(predictions,targets)
                    segs[seg] = b
                                # / float(segmentWeights[seg])
                    # predictions = [float(urb[n]), float(inc[n]), float(ed[n]), float(ag[n])]
                    # targets = [float(coeffNew["Urban")), float(line[2]), float(line[3]), float(line[4])]

            # print ids[n]
            # print segs
            ns = str(ids[n])
            segments[ns] = segs
            n = n + 1


        print "Scores calculated using " + coeffFile
        return segments

    def calcAvgIncome(data):
        incs = data['MedInc']
        n = 0
        totIncome = 0
        for i in incs:
            if (i != 'None'):
                inc = int(i)
                if inc != 0:
                    totIncome = totIncome + inc
                    n = n + 1

        avgIncome = totIncome / n
        # print "Average income calculated to be " + str(avgIncome)
        return avgIncome

    def classAges(data):
        ages = data['Median_Age']
        classy = []
        for a in ages:
            if a != 'None':
                ag = float(a)
                if ag < 40:
                    classy.append(-10)
                if (ag >= 40) and (ag < 45):
                    classy.append(-5)
                if (ag >= 45) and (ag < 50):
                    classy.append(0)
                if (ag >= 50) and (ag < 55):
                    classy.append(5)
                if (ag >= 55):
                    classy.append(10)
            elif (a == 'None'):
                classy.append(0)
        # print classy
        return classy

    def classIncs(data,med):
        incs = data["MedInc"]
        classy = []
        for a in incs:
            if (a != 'None'):
                ag = int(a)
                if ag < (med*.6):
                    classy.append(-10)
                if (ag >= (med*.6)) and (ag < (med*.9)):
                    classy.append(-5)
                if (ag >= (med*.9)) and (ag < (med*1.1)):
                    classy.append(0)
                if (ag >= (med*1.1)) and (ag < (med*1.4)):
                    classy.append(5)
                if (ag >= (med*1.4)):
                    classy.append(10)
            elif (a == 'None'):
                classy.append(0)
        # print incs
        # print classy
        return classy

    def classEdu(data):
        someCollege = data['PSomeCol']
        collegePlus = data['PColPlus']
        postGrad = data['PPostGrad']
        classy = []
        i = 0
        while i < len(someCollege):
            somCol = float(someCollege[i])
            colPlus = float(collegePlus[i])
            pGrad = float(postGrad[i])
            if (colPlus < .25):
                classy.append(-10)
            elif (colPlus < .4):
                classy.append(-5)
            elif (colPlus >= .4) and (colPlus < .6):
                classy.append(5)
            elif (colPlus >= .6):
                classy.append(10)
            i = i + 1
        # print incs
        # print classy
        return classy

    def calcPercentile(data,varf,p):
        import numpy as np
        a = data[varf]
        co = 0
        pt = []
        for t in a:
            pop = data["Total_Population"]
            popr = float(pop[co])
            # print len(pop)
            # print len()
            ae = float(t)
            if popr != 0:
                pt.append(float(ae/popr))
            co = co + 1
        perc = np.percentile(pt, p) # return 50th percentile, e.g median.
        return perc

    def classUrban(ids):
        ## Using data from http://www.cdc.gov/nchs/data_access/urban_rural.htm#urbancountries2013
        classy = []
        dataC = {}
        f2 = paths["Params"] + "UrbanRuralClass.csv"

        with open(f2, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)

            for row in reader:
                state = str(row['stfips']).zfill(2)
                county = str(row['ctyfips']).zfill(3)
                stc = state + county
                dataC[stc] = row["CODE2013"]

        for id in ids:
            gstc = id[:5]
            urbrur = str(dataC[gstc])

            if urbrur == '6':
                classy.append(-10)
            if urbrur == '5':
                classy.append(-5)
            if urbrur == '4':
                classy.append(0)
            if urbrur == '3':
                classy.append(2)
            if urbrur == '2':
                classy.append(4)
            if urbrur == '1':
                classy.append(10)
        return classy

    def classOthers():
        classys = {}
        vcb = getVarClasses()
        # data = getCoefficients()
        for key in vcb:
            # someCollege = data['PSomeCol']
            # collegePlus = data['PColPlus']
            # postGrad = data['PPostGrad']
            # vldata = data[key]
            print ("key: " + key)
            print data
            dkey = data[key]
            classy = []
            vca = vcb[key]
            con = 0
            pop = data["Total_Population"]
            for h in dkey:
                print h
                popr = float(pop[con])
                ae = float(h)
                if popr != 0:
                    pt = (float(ae/popr))
                elif popr == 0:
                    pt = 0
                i = 0
                con = con + 1
                while i < len(vca):
                    set = False
                    vcaD = vca[i]
                    # print "YO SIR"
                    # print vcaD
                    pmin = (float(vcaD["Min"]) * 100)
                    # print "Po"
                    # print "Pmin"
                    pmax = (float(vcaD["Max"]) * 100)
                    pval = int(vcaD["Value"])
                    # print "PT"
                    print (pt)
                    percmin = calcPercentile(data,key,pmin)
                    percmax = calcPercentile(data,key,pmax)
                    # print "Pmin"
                    print (percmin)
                    # print "Pmax"
                    print (percmax)
                    if (pt > percmin) and (pt <= percmax):
                        classy.append(pval)
                        set = True
                        i = i + 1
                    elif (set == False):
                        i = i + 1
                        print "Haha"
                        # if (colPlus < .25):
                        #     classy.append(-10)
                        # elif (colPlus < .4):
                        #     classy.append(-5)
                        # elif (colPlus >= .4) and (colPlus < .6):
                        #     classy.append(5)
                        # elif (colPlus >= .6):
                        #     classy.append(10)
                if set != True:
                    classy.append(0)
                    set = True
            classys[key] = classy
        print ("Finished Classifying!")
        return classys

    def writeSegments(segments,floc,state):
        # segloc = r"C:\Users\kdenny\Documents\PostalSegmentation\DC_MD_VA/Segments/"
        if os.path.isfile(floc):
            print ("Do you wish to overwrite existing segmentation files? ")
            overwrite = raw_input("(Y/N) ")
            ow = overwrite.upper()
            if ow == 'Y':
                if os.path.isfile(floc):
                    os.remove(floc)
            if ow == 'N':
                floc = "C:\Users\kdenny\Documents\PostalSegmentation\DC_MD_VA/Segments1/{0}_Segments.csv".format(state)
                segloc = r"C:\Users\kdenny\Documents\PostalSegmentation\DC_MD_VA/Segments1/"
                if os.path.isfile(floc):
                    os.remove(floc)
        tx = "GEOID"
        keys = []
        keysA = [tx]

        for key in segments:
            a = segments[key]
            for key2 in a:
                if key2 not in keys:
                    keys.append(key2)
                    keysA.append(key2)
        keysA.append("Segment")
        # b = open(floc, 'wb')
        with open(floc, 'wb') as b:
            # ar = csv.writer(b)
            writer = csv.DictWriter(b, fieldnames=keysA)
            writer.writeheader()

            for key in segments:
                # r = []
                r = [str(key)]
                r2 = []
                for d in keys:
                    a = segments[key]
                    r.append(str(a[d]))
                    r2.append(float(a[d]))
                fr2 = []
                for u in r2:
                    j = float(u)
                    fr2.append(j)
                v1 = min(fr2)
                v2 = fr2.index(v1)
                r.append(keys[(v2)])
                count = 0
                segmDict = {}
                for m in keysA:
                    segmDict[m] = r[count]
                    count = count + 1

                # print r
                # ar.writerow(r)
                writer.writerow(segmDict)
        b.close()
        print "Segments written for " + floc

    def setAttributeWeightings(weightFile):
        with open(weightFile, 'rU') as infile:
          reader = csv.DictReader(infile)
          data = {}
          for row in reader:
              data[row['Attribute']] = row['Weight']
        return data

    def setSegmentWeightings(weightFile):
        with open(weightFile, 'rU') as infile:
          reader = csv.DictReader(infile)
          data = {}
          for row in reader:
              data[row['Segment']] = row['Weight']
        return data
        ## Enable functionality to weight certain variables more strongly in the RMSE for specific segmentations

    ### MAIN

    floc = paths["Main"]
    inStates = states
    cf = str(paths["Params"] + "coefficients.csv")
    segs = getSegments()
    segs = readSegments(cf)

    for st in inStates:
        f = paths["Data"] + st + "DataFields.csv"
        f2 = paths["Data"] + st + "DataFields_Result.csv"
        head = calcColumns(f,f2)

        with open(f2, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(str(value))
                    except KeyError:
                        data[header] = [str(value)]



        ids = data['GEOID']
        # avInc = calcAvgIncome(incs)
        avInc = calcAvgIncome(data)
        # agesT = classAges(ages)
        agesT = classAges(data)
        # incsT = classIncs(incs,avInc)
        incsT = classIncs(data,avInc)
        oclassesT = classOthers()
        # eduT = classEdu(someCollege,collegePlus,postGrad)
        eduT = classEdu(data)
        urbT = classUrban(ids)

        sloc = paths["Segments"] + st + "_Segments.csv"
        segWeightFile = paths["Params"] + "SegmentWeights.csv"
        coeffFile = paths["Params"] + "coefficients.csv"


        segmentWeights = setSegmentWeightings(segWeightFile)

        segments = calcScores2(ids,urbT,incsT,eduT,agesT,segmentWeights,cf,oclassesT)

        m = writeSegments(segments,sloc,st)

        print ("Segments written for {0}".format(st))

def joinTracts(shploc,segloc,states,segments):
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
        print ("Segments joined to shapefile for state {0}. Results located in {1}".format(state,ofile))