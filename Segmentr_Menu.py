from Tkinter import *
from MenuDriver import *
from ACS_Import_Menu import *
import tkFileDialog as tkfd
import ttk

bc = ''
erra = ['WkDir','State']
coeffN = {}
dataM = {}
dataMSet = False

#### Define functions

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def setC(data, old):
    for b in old:
        if b in data:
            coeffN[b] = data[b]
        else:
            coeffN[b] = old[b]
    # print coeffN

def setWkDir():
    chooseDir('wk','folder',r'C:\Users\kdenny\Documents\PostalSegmentation\SegmentrTest')

def chooseDir(dirType,opType,defaultr):
    filewin = Toplevel(root)
    filewin.title("Choose {0} Directory".format(dirType))
    filewin.minsize(400, 250)

    def openChooser():
        if opType == 'folder':
            openFolderChooser()
        if opType == '':
            openFileChooser()
    def openFolderChooser():
        # filetypeslist = [('all files', '.*'), ('folders', '/')]
        # s = e.get()
        s = tkfd.askdirectory()
    def openFileChooser():
        filetypeslist = [(opType, '/{0}'.format(opType)), ('csv', '.csv'), ('all files', '.*'), ('folders', '/')]

        s = tkfd.askdirectory()

    def dircallback():
        # s = e.get()
        s = direntry.get()
        if s[-1:] != '/':
            s = s + '/'
        printr(s)
        if dirType == 'wk':
            pas = createFolders(s)
            for k in pas:
                paths[k] = pas[k]
                workdirSet = True
                workdir = s
            setPaths(paths)
        if dirType == 'Coefficient':
            coeffFile = s
        # setMessage("")
        deleteMessage(mo)
        createMessage(mo, bc)
        filewin.destroy()

    statusvar = StringVar(filewin, value="Input File", name="Status Bar")
    statusbar = ttk.Label(filewin, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    dirfile = StringVar(filewin, value="", name="{0}Dir".format(dirType))
    dirlabel = ttk.Label(filewin, text="{0} Directory".format(dirType))
    dirlabel.grid(row=1, column=0)
    direntry = Entry(filewin, width=50)
    direntry.grid(row=1, column=1, columnspan=5, sticky="EW")
    direntry.delete(0, END)
    direntry.insert(0, r"C:\Users\kdenny\Documents\PostalSegmentation\SegmentrTest/")
    dirbutton = ttk.Button(filewin, text="Open...", command=openFolderChooser)
    dirbutton.grid(row=1, column=6)
    b = Button(filewin, text="Set Directory", width=15, command=dircallback)
    b.grid(row=2, column=3)

    c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    c.grid(row=2, column=4)

def chooseDataLoc():
    filewin = Toplevel(root)
    filewin.title("Choose Data Directory")
    filewin.minsize(400, 250)

    def openChooser():
        # filetypeslist = [('all files', '.*'), ('folders', '/')]
        # s = e.get()
        s = tkfd.askdirectory()
        # s = tkfd.askopenfilename(filetypes=filetypeslist)

    def dircallback2():
        # s = e.get()
        s = datadirentry.get()
        if s[-1:] != '/':
            s = s + '/'
        printr(s)
        datadirSet = True
        datadir = s
        # setMessage("")
        filewin.destroy()

    statusvar = StringVar(filewin, value="Input File", name="Status Bar")
    statusbar = ttk.Label(filewin, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    datadirfile = StringVar(filewin, value="", name="DataDir")
    datadirlabel = ttk.Label(filewin, text="Data Location")
    datadirlabel.grid(row=1, column=0)
    datadirentry = Entry(filewin, width=50)
    datadirentry.grid(row=1, column=1, columnspan=5, sticky="EW")
    datadirentry.delete(0, END)
    datadirentry.insert(0, "C:/Users/kdenny/Documents/SegmentrBase")
    datadirbutton = ttk.Button(filewin, text="Open...", command=openChooser)
    datadirbutton.grid(row=1, column=6)
    b = Button(filewin, text="Set Directory", width=15, command=dircallback2)
    b.grid(row=2, column=3)

    c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    c.grid(row=2, column=4)
    # printr(paths)
    # filewin = Toplevel(root)
    # def dircallback2():
    #     s = e.get()
    #     if s[-1:] != '/':
    #         s = s + '/'
    #     datadirSet = True
    #     datadir = s
    #     setMessage("")
    #     filewin.destroy()
    #
    #
    # e = Entry(filewin, width=50)
    # e.pack()
    #
    # e.delete(0, END)
    # e.insert(0, "C:/Users/kdenny/Documents/SegmentrBase")
    #
    # b = Button(filewin, text="Set Data Directory", width=15, command=dircallback2)
    # b.pack()
    #
    # c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    # c.pack()


def rebuild(scc2):
    mo = LabelFrame(root)
    bc = scc2
    mo.pack(side="top")
    createMessage(mo,bc)

def selectState2():
    # filewin = Toplevel(root)
    cs = []
    scode = ''
    def reint(scode):
        e.delete(0, END)
        e.insert(0, scode)
        # e.after(100, reint)
        # printr("yo")

    def OnDouble(event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print (value)
        e.after(200, reint(value))

    def reloadMain():
        scc = e.get()
        mo.destroy()
        rebuild(scc)
        f.destroy()
        # mo = Frame(root)
        # mo.pack(side="top")

    def dircallback3():
        sm = []
        scode = e.get()
        s = textToFips(e.get(),paths)
        states[:] = []
        states.append(str(s))
        sm.append(str(s))
        # filewin.destroy()
        shpdata = datadir + "Shapefiles/"
        src_files = os.listdir(shpdata)
        for file_name in src_files:
            if str(s) == file_name[8:10]:
                full_file_name = os.path.join(shpdata, file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.copy(full_file_name, paths["Shapefiles"])
        ## Downloads ACS data if it does not already exist
        npath = str(paths["Data"] + str(s) + "DataFields.csv")
        if not (os.path.isfile(npath)):
            # setMessage("Getting ACS data")
            # a.set(message)
            getACS_base(paths["Main"],sm)
        stateSet = True
        # f.destroy()
        # scc = scode
        reloadMain()
        # setMessage("")

    # fwin2 = Toplevel(root)
    f = LabelFrame(root)
    f.pack()

    statusvar = StringVar(f, value="Select a state from the available states in memory", name="Status Bar")
    statusbar = ttk.Label(f, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    w = Label(f, text="Double click to select a state", font=("Helvetica", 12))
    w.grid(row=1, column=0)

    sty = getAvailStates(datadir)
    ly = len(sty)
    y = 1
    Lb1 = Listbox(f, height=(ly+1))
    for n in sty:
        name = fipsToText(n,paths)
        Lb1.insert(y, name)
        y = y + 1
    Lb1.bind("<Double-Button-1>", OnDouble)
    Lb1.grid(row=2, column=0)
    # Lb1.pack(side="top", fill="both", expand=True)
    h = Label(f, text="", font=("Helvetica", 12))
    h.grid(row=3, column=0)

    w = Label(f, text="Current state:")
    w.grid(row=4, column=0)
    e = Entry(f, width=20)
    e.grid(row=4, column=1)

    j = Label(f, text="", font=("Helvetica", 12))

    j.grid(row=5, column=0)

    e.delete(0, END)
    e.insert(0, scode)

    b = Button(f, text="Set State", width=15, command=dircallback3)
    b.grid(row=8, column=0)

    # m = Button(filewin, text="Select State", width=15, command=lbo)
    # m.pack()

    c = Button(f, text="Quit", width=15, command=reloadMain)
    c.grid(row=8, column=1)

def xpress():
    filewin = Toplevel(root)
    def dircallback4():
        sm = []
        s = e.get()
        pas = createFolders(workdir)
        for k in pas:
            paths[k] = pas[k]
        printr(paths)
        states.append(str(s))
        sm.append(str(s))
        filewin.destroy()
        shpdata = datadir + "Shapefiles/"
        src_files = os.listdir(shpdata)
        for file_name in src_files:
            if str(s) == file_name[8:10]:
                full_file_name = os.path.join(shpdata, file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.copy(full_file_name, paths["Shapefiles"])
        ## Downloads ACS data if it does not already exist
        npath = str(paths["Data"] + str(s) + "DataFields.csv")
        # if not (os.path.isfile(npath)):
        #     getACS_base(paths["Main"],sm)
        workdirSet = False
        datadirSet = True
        stateSet = False
        printr("Segmenting in progress")
        segmentz()
        printr("Joining in progress")
        joint()


    e = Entry(filewin, width=50)
    e.pack()

    e.delete(0, END)
    e.insert(0, "11")

    b = Button(filewin, text="Set State", width=15, command=dircallback4)
    b.pack()

    c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    c.pack()

def segmentz():
    if len(erra) != 0:
        return
    print "Herdle"
    print coeffN
    cn = getCoefficients()
    createSegments(paths,states,cn)

def joint():
    shploc = paths["Shapefiles"]
    segloc = paths["Segments"]
    cf = paths["Params"] + "coefficients.csv"
    segs = getSegments()
    joinTracts(shploc,segloc,states,segs)

def getHotspots():
    import csv

    # sgs =[]
    # cf = paths["Params"] + "coefficients.csv"
    #
    # with open(cf, 'rU') as infile2:
    #     reader2 = csv.DictReader(infile2)
    #     for row2 in reader2:
    #         if row2['Segment'] not in sgs:
    #             sgs.append(row2['Segment'])
    sgs = getSegments()

    calcHotspots(paths,states,sgs)

def displayMap():
    maploc = paths
    from mxdTesterF import mappr
    mappr(maploc, states)

def createMessage(mo,bc):
    for widget in mo.winfo_children():
        widget.destroy()
    atext = ''
    btext = ''
    if "Main" in paths:
        atext = "Current working directory: {0}".format(paths["Main"])
        if "WkDir" in erra:
            erra.remove("WkDir")
    elif "Main" not in paths:
        atext = "Working directory not set!"

    if bc != '':
        btext = "Current state: {0}".format(bc)
        if "State" in erra:
            erra.remove("State")
    elif bc == '':
        btext = "Current state not set!"

    labelA = Label(mo, text=atext)
    labelA.pack()
    labelB = Label(mo, text=btext)
    labelB.pack()

    # labelA.tag_add("start", "1.1", "3.1")
    # labelA.tag_config("start", background="black", foreground="yellow")

def deleteMessage(mo):
    for widget in mo.winfo_children():
        widget.destroy()

def editSegmentCoefficients():
    import csv
    sr = 'A'
    # segOpen = False
    # def openAChooser():
    #     # filetypeslist = [('all files', '.*'), ('folders', '/')]
    #     # s = e.get()
    #     # s = tkfd.askdirectory()

    # coeffFile = paths["Params"] + "coefficients.csv"
    data = {}
    newCof = {}
    ps = getVariables()
    sgs = []
    windowsOpen = [1]
    coeffFile = paths["Params"] + "coefficients.csv"

    def setSegLoc():
        cyp = paths["Params"] + "coefficients.csv"
        chooseDir('Coefficient','folder',cyp)
    # tf = PanedWindow(root)
    # tf.pack(fill=BOTH, expand=1)

    # def setSegOpen(a):
    #     segOpen = a

    # def getSegOpen():
    #     return segOpen

    # ps = ['Urban','Income','Education','Age']
    # with open(coeffFile, 'rU') as infile:
    #     reader = csv.DictReader(infile)
    #     for row in reader:
    #         for key in row:
    #             # print key
    #             if (key not in ps) and (key != 'Segment'):
    #                 ps.append(key)
    # with open(coeffFile, 'rU') as infile2:
    #     reader2 = csv.DictReader(infile2)
    #     for row2 in reader2:
    #         data2 = {}
    #         for p in ps:
    #             data2[p] = row2[p]
    #         data[row2['Segment']] = data2
    #         if dataMSet == False:
    #             data[row2['Segment']] = data2
    #         if row2['Segment'] not in sgs:
    #             sgs.append(row2['Segment'])
    data = getCoefficients()

    curSeg = data[sr]

    # if coeffNEdit == True:
    #     for c in coeffN:
    #         # data[c] = coeffN[c]
    #         newCof[c] = coeffN[c]
    #     curSeg = newCof[sr]
    #
    # if coeffNEdit == False:
    #     curSeg = data[sr]


    def reint4(sr):
        e.delete(0, END)
        e.insert(0, sr)
        # e.after(100, reint)

    def OnDouble(event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print (value)
        e.after(200, reint4(value))
        # if segOpen == True:
        #     f1.destroy()
        dircallback8()

    def reloadMainr():
        fe3.destroy()
        # deleteMessage(mo)
        # createMessage(mo)


    def exportr():
        # printr(newCof)
        # setC(newCof,data)
        setCoefficients(newCof,data)
        # coeffNEdit = True
    # def dircallbackF():

    def dircallback5():

        # def show_values():
        #     print (sr, w1.get(), w2.get(), w3.get(), w4.get())
            # for es in entries.keys():
            #     print es
        def printm():
            print(getCoefficients())

        def set_marks():

            vc0 = {}
            vcF = {}
            vc0["Min"] = 0
            vc0["Max"] = (float(entry1.get()) / 100)
            vc0["Value"] = int(entry2.get())
            variableClasses[0] = vc0
            vcF["Min"] = (float(entryo.get()) / 100)
            vcF["Max"] = 1
            vcF["Value"] = int(entryo2.get())
            count = 1
            for et in entries:
                entr = entries[et]
                vc = {}
                vc["Min"] = (float((entr["Less"]).get()) / 100)
                vc["Max"] = (float((entr["More"]).get()) / 100)
                vc["Value"] = int(entr["Value"].get)
                variableClasses[count]  = vc
                # print (entries[et]).get()
                count = count + 1
                print et
            variableClasses[count] = vcF
            addVarClassesToData(vard,variableClasses)
            f1.destroy()
            fa.destroy()
            addVariableToSegments(vard)


        # if getSegOpen() == True:
        #     f1.destroy()
        sr = e.get()
        j = int(sr)
        k = 1
        entries = {}
        lbls = {}
        data = getCoefficients()
        curSeg = data[sr]
        if sr in newCof:
            curSeg = newCof[sr]
            print "YaYa"
        # f.destroy()
        f1 = LabelFrame(root)
        f1.pack()
        # segOpen = True
        windowsOpen.append(2)
        printr(sr)
        r = Label(f1, text="Current Segment: {}".format(sr), font = "Helvetica 16 bold")
        r.pack()
        # rb = Label(f1, text="Set Variable Percentile Classifications for {0}".format(vard), font = "Helvetica 18")
        # rb.grid(row=1,column=1)


        # r = Label(f1, text="Less than x percentile", font = "Helvetica 12")
        # r.grid(row=2,column=1)
        # entry1 = Entry(f1, width=5)
        # entry1.grid(row=2, column=3, columnspan=1, sticky="EW")
        # entry1.delete(0, END)
        # entry1.insert(0, "0")
        # r2 = Label(f1, text="Value:", font = "Helvetica 12")
        # r2.grid(row=2,column=4)
        # entry2 = Entry(f1, width=5)
        # entry2.grid(row=2, column=5, columnspan=1, sticky="EW")
        # entry2.delete(0, END)
        # entry2.insert(0, "")

        while k < (j-1):
            lbl = {}
            lbl["One"] = Label(f1, text="Between x and x percentile", font = "Helvetica 12")
            lbl["One"].grid(row=(k+2),column=1)
            ent = {}
            ent["Less"] = Entry(f1, width=3)
            ent["Less"].grid(row=(k+2), column=3, columnspan=1, sticky="EW")
            ent["Less"].delete(0, END)
            ent["Less"].insert(0, "")
            ent["More"] = Entry(f1, width=3)
            ent["More"].grid(row=(k+2), column=4, columnspan=1, sticky="EW")
            ent["More"].delete(0, END)
            ent["More"].insert(0, "")
            lbl["Two"] = Label(f1, text="Value:", font = "Helvetica 12")
            lbl["Two"].grid(row=(k+2),column=5)
            ent["Value"] = Entry(f1, width=3)
            ent["Value"].grid(row=(k+2), column=6, columnspan=1, sticky="EW")
            ent["Value"].delete(0, END)
            ent["Value"].insert(0, "")
            entries[k] = ent
            lbls[k] = lbl

            k = k + 1

        o = Label(f1, text="Greater than x percentile", font = "Helvetica 12")
        o.grid(row=(j+2),column=1)
        entryo = Entry(f1, width=5)
        entryo.grid(row=(j+2), column=3, columnspan=1, sticky="EW")
        entryo.delete(0, END)
        entryo.insert(0, "")
        o2 = Label(f1, text="Value:", font = "Helvetica 12")
        o2.grid(row=(j+2),column=4)
        entryo2 = Entry(f1, width=5)
        entryo2.grid(row=(j+2), column=5, columnspan=1, sticky="EW")
        entryo2.delete(0, END)
        entryo2.insert(0, "10")

        bb = Button(f1, text='Set Values', command=set_marks)
        bb.grid(row=(j+3),column=1)

        cc = Button(f1, text='Print Values', command=printm)
        cc.grid(row=(j+3),column=3)

    def dircallback8():

        def show_values():
            print (sr, w1.get(), w2.get(), w3.get(), w4.get())
        def set_values():
            df = {}
            df[ps[0]] = w1.get()
            df[ps[1]] = w2.get()
            df[ps[2]] = w3.get()
            df[ps[3]] = w4.get()
            # data[sr] = df
            newCof[sr] = df
            f1.destroy()
            setCoefficients(newCof,data)


        # if getSegOpen() == True:
        #     f1.destroy()
        inputs = {}
        sr = e.get()
        data = getCoefficients()
        curSeg = data[sr]
        if sr in newCof:
            curSeg = newCof[sr]
            print "YaYa"
        # f.destroy()
        f1 = LabelFrame(root)
        f1.pack()
        # segOpen = True
        windowsOpen.append(2)
        printr(sr)
        r = Label(f1, text="Current Segment: {}".format(sr), font = "Helvetica 16 bold")
        r.pack()

        wa = Label(f1, text=ps[0])
        wa.pack()
        w1 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        w1.set(curSeg[ps[0]])
        w1.pack()
        wb = Label(f1, text=ps[1])
        wb.pack()
        w2 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        w2.set(curSeg[ps[1]])
        w2.pack()
        wc = Label(f1, text=ps[2])
        wc.pack()
        w3 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        w3.set(curSeg[ps[2]])
        w3.pack()
        wd = Label(f1, text=ps[3])
        wd.pack()
        w4 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        w4.set(curSeg[ps[3]])
        w4.pack()
        # for

        Button(f1, text='Set Values', command=set_values).pack()
        Button(f1, text='Print Values', command=show_values).pack()

        mainloop()
        f1.quit()

        # setSegOpen(segOpen)
        # setMessage("")


    # filewin = Toplevel(root)
    # frame2 = Frame(root)
    # frame2.pack()
    fe3 = Frame(root)
    fe3.pack()
    gt = False

    statusvar = StringVar(fe3, value="Select a segment from the available segments", name="Status Bar")
    statusbar = ttk.Label(fe3, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    q = Label(fe3, text="Double click to select a segment", font=("Helvetica", 12))
    q.grid(row=1, column=0)

    sty = getSegments()
    # print sty
    ly = len(sty)
    y = 1
    Lb1 = Listbox(fe3, height=(ly+1))
    for n in sty:
        Lb1.insert(y, n)
        y = y + 1
    Lb1.bind("<Double-Button-1>", OnDouble)
    Lb1.grid(row=2, column=0)
    # Lb1.pack(side="top", fill="both", expand=True)
    h = Label(fe3, text="", font=("Helvetica", 12))
    h.grid(row=3, column=0)

    u = Label(fe3, text="Current segment:")
    u.grid(row=4, column=0)
    e = Entry(fe3, width=20)
    e.grid(row=4, column=1)

    # e.delete(0, END)
    # e.insert(0, sr)

    j = Label(fe3, text="", font=("Helvetica", 12))
    j.grid(row=5, column=0)

    lbut = Button(fe3, text="Load Segments", width=15, command=setSegLoc)
    lbut.grid(row=6, column=4)

    lbut = Button(fe3, text="Export ALL Segments", width=15, command=exportr)
    lbut.grid(row=6, column=1)

    kbut = Button(fe3, text="Set Segment", width=10, command=dircallback8)
    kbut.grid(row=6, column=0)
    # kbut.pack()

    cbut = Button(fe3, text="Quit", width=10, command=reloadMainr)
    cbut.pack()
    cbut.grid(row=6, column=3)

def addSegment():

    filewin = Toplevel(root)
    filewin.title("Name New Segment")
    filewin.minsize(400, 250)

    def dircallbackSeg():
        # s = e.get()
        data6 = getCoefficients()
        newCof = {}
        s = datadirentry.get()
        segmentName = s
        ps = getVariables()
        df = {}
        df[ps[0]] = 0
        df[ps[1]] = 0
        df[ps[2]] = 0
        df[ps[3]] = 0
        # data[sr] = df
        newCof[segmentName] = df
        # f1.destroy()
        addSegm(s)
        setCoefficients(newCof,data6)
        filewin.destroy()

    statusvar = StringVar(filewin, value="New Segment", name="Status Bar")
    statusbar = ttk.Label(filewin, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    segmentTx = StringVar(filewin, value="", name="New Segment")
    label = ttk.Label(filewin, text="New Segment")
    label.grid(row=1, column=0)
    datadirentry = Entry(filewin, width=50)
    datadirentry.grid(row=1, column=1, columnspan=5, sticky="EW")
    datadirentry.delete(0, END)
    datadirentry.insert(0, "")
    # datadirbutton = ttk.Button(filewin, text="Open...", command=openChooser)
    # datadirbutton.grid(row=1, column=6)
    b = Button(filewin, text="Create", width=15, command=dircallbackSeg)
    b.grid(row=2, column=3)

    c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    c.grid(row=2, column=4)


   # # filewin = Toplevel(root)
   #  cs = []
   #  scode = ''
   #  def reint(scode):
   #      e.delete(0, END)
   #      e.insert(0, scode)
   #      # e.after(100, reint)
   #      # printr("yo")
   #
   #  def OnDouble(event):
   #      widget = event.widget
   #      selection=widget.curselection()
   #      value = widget.get(selection[0])
   #      print (value)
   #      e.after(200, reint(value))
   #
   #  def reloadMain():
   #      scc = e.get()
   #      mo.destroy()
   #      rebuild(scc)
   #      f.destroy()
   #      # mo = Frame(root)
   #      # mo.pack(side="top")
   #
   #  def dircallback3():
   #      sm = []
   #      scode = e.get()
   #      s = textToFips(e.get(),paths)
   #      states.append(str(s))
   #      sm.append(str(s))
   #      # filewin.destroy()
   #      shpdata = datadir + "Shapefiles/"
   #      src_files = os.listdir(shpdata)
   #      for file_name in src_files:
   #          if str(s) == file_name[8:10]:
   #              full_file_name = os.path.join(shpdata, file_name)
   #              if (os.path.isfile(full_file_name)):
   #                  shutil.copy(full_file_name, paths["Shapefiles"])
   #      ## Downloads ACS data if it does not already exist
   #      npath = str(paths["Data"] + str(s) + "DataFields.csv")
   #      if not (os.path.isfile(npath)):
   #          # setMessage("Getting ACS data")
   #          # a.set(message)
   #          getACS_base(paths["Main"],sm)
   #      stateSet = True
   #      # f.destroy()
   #      # scc = scode
   #      reloadMain()
   #      # setMessage("")
   #
   #  # fwin2 = Toplevel(root)
   #  f = LabelFrame(root)
   #  f.pack()
   #
   #  statusvar = StringVar(f, value="Select a state from the available states in memory", name="Status Bar")
   #  statusbar = ttk.Label(f, textvariable=statusvar, background="#FFFFCC")
   #  statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")
   #
   #  w = Label(f, text="Double click to select a state", font=("Helvetica", 12))
   #  w.grid(row=1, column=0)
   #
   #  sty = getAvailStates(datadir)
   #  ly = len(sty)
   #  y = 1
   #  Lb1 = Listbox(f, height=(ly+1))
   #  for n in sty:
   #      name = fipsToText(n,paths)
   #      Lb1.insert(y, name)
   #      y = y + 1
   #  Lb1.bind("<Double-Button-1>", OnDouble)
   #  Lb1.grid(row=2, column=0)
   #  # Lb1.pack(side="top", fill="both", expand=True)
   #  h = Label(f, text="", font=("Helvetica", 12))
   #  h.grid(row=3, column=0)
   #
   #  w = Label(f, text="Current state:")
   #  w.grid(row=4, column=0)
   #  e = Entry(f, width=20)
   #  e.grid(row=4, column=1)
   #
   #  j = Label(f, text="", font=("Helvetica", 12))
   #
   #  j.grid(row=5, column=0)
   #
   #  e.delete(0, END)
   #  e.insert(0, scode)
   #
   #  b = Button(f, text="Set State", width=15, command=dircallback3)
   #  b.grid(row=8, column=0)
   #
   #  # m = Button(filewin, text="Select State", width=15, command=lbo)
   #  # m.pack()
   #
   #  c = Button(f, text="Quit", width=15, command=reloadMain)
   #  c.grid(row=8, column=1)

def addVariable():

    filewin = Toplevel(root)
    filewin.title("Select New Variable")
    filewin.minsize(400, 250)

    acsV = getACSDataFields(paths)
    acsVariables = []
    for key in acsV:
        if key not in acsVariables:
            acsVariables.append(key)


    # def dircallbackSeg():
    #     # s = e.get()
    #     data6 = getCoefficients()
    #     newCof = {}
    #     s = datadirentry.get()
    #     segmentName = s
    #     ps = getVariables()
    #     df = {}
    #     df[ps[0]] = 0
    #     df[ps[1]] = 0
    #     df[ps[2]] = 0
    #     df[ps[3]] = 0
    #     # data[sr] = df
    #     newCof[segmentName] = df
    #     # f1.destroy()
    #     addSegm(s)
    #     setCoefficients(newCof,data6)
    #     filewin.destroy()

    statusvar = StringVar(filewin, value="New Variable", name="Status Bar")
    statusbar = ttk.Label(filewin, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    variableTx = StringVar(filewin, value="", name="New Variable")
    label = ttk.Label(filewin, text="New Variable")
    label.grid(row=1, column=0)

    var = StringVar(filewin)
    var.set("None") # initial value
    w = apply(OptionMenu, (filewin, var) + tuple(acsVariables))
    # option = OptionMenu(filewin, var, "one", "two", "three", "four")
    w.grid(row=2,column=0)

    #
    # test stuff

    def ok():
        addVarToData(var.get())
        addVariableClassifications(var.get())
        # quitMe()
        # filewin.quit()

    def quitMe():
        filewin.quit()

    button = Button(filewin, text="OK", command=ok)
    button.grid(row=5,column=0)

    button2 = Button(filewin, text="Quit", command=quitMe)
    button.grid(row=5,column=2)



    # datadirentry = Entry(filewin, width=50)
    # datadirentry.grid(row=1, column=1, columnspan=5, sticky="EW")
    # datadirentry.delete(0, END)
    # datadirentry.insert(0, "")
    # # datadirbutton = ttk.Button(filewin, text="Open...", command=openChooser)
    # # datadirbutton.grid(row=1, column=6)
    # b = Button(filewin, text="Create", width=15, command=dircallbackSeg)
    # b.grid(row=2, column=3)
    #
    # c = Button(filewin, text="Quit", width=15, command=filewin.destroy)
    # c.grid(row=2, column=4)

def addVariableToSegments(vard):

    def dircallback5():

        def show_values():
            print (sr, w1.get())
        def set_values():
            newCof = {}
            coj = getCoefficients()
            df = coj[sr]
            df[vard] = w1.get()
            # df[ps[0]] = w1.get()
            # df[ps[1]] = w2.get()
            # df[ps[2]] = w3.get()
            # df[ps[3]] = w4.get()
            # data[sr] = df
            newCof[sr] = df

            fb.destroy()
            setCoefficients(newCof,coj)


        # if getSegOpen() == True:
        #     f1.destroy()
        sr = var.get()
        # data = getCoefficients()
        # curSeg = data[sr]
        # if sr in newCof:
        #     curSeg = newCof[sr]
        #     print "YaYa"
        # f.destroy()
        fb = LabelFrame(root)
        fb.pack()
        # segOpen = True
        printr(sr)
        r = Label(fb, text="Current Segment: {}".format(sr), font = "Helvetica 16 bold")
        r.pack()
        wa = Label(fb, text=vard)
        wa.pack()
        w1 = Scale(fb, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        w1.set(0)
        w1.pack()
        # wb = Label(f1, text=ps[1])
        # wb.pack()
        # w2 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        # w2.set(curSeg[ps[1]])
        # w2.pack()
        # wc = Label(f1, text=ps[2])
        # wc.pack()
        # w3 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        # w3.set(curSeg[ps[2]])
        # w3.pack()
        # wd = Label(f1, text=ps[3])
        # wd.pack()
        # w4 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
        # w4.set(curSeg[ps[3]])
        # w4.pack()
        Button(fb, text='Set Values', command=set_values).pack()
        Button(fb, text='Print Values', command=show_values).pack()

        # mainloop()
        # f1.quit()

    fl = LabelFrame(root)
    fl.pack()
    # fl.minsize(400, 250)


    segms = getSegments()
    segNames = []
    for key in segms:
        if key not in segNames:
            segNames.append(key)




    # def dircallbackSeg():
    #     # s = e.get()
    #     data6 = getCoefficients()
    #     newCof = {}
    #     s = datadirentry.get()
    #     segmentName = s
    #     ps = getVariables()
    #     df = {}
    #     df[ps[0]] = 0
    #     df[ps[1]] = 0
    #     df[ps[2]] = 0
    #     df[ps[3]] = 0
    #     # data[sr] = df
    #     newCof[segmentName] = df
    #     # f1.destroy()
    #     addSegm(s)
    #     setCoefficients(newCof,data6)
    #     filewin.destroy()

    statusvar = StringVar(fl, value="New Variable", name="Status Bar")
    statusbar = ttk.Label(fl, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    variableTx = StringVar(fl, value="", name="New Variable")
    label = ttk.Label(fl, text="Select Segment to add new variable {0}".format(vard))
    label.grid(row=1, column=0)

    var = StringVar(fl)
    var.set("None") # initial value
    w = apply(OptionMenu, (fl, var) + tuple(segNames))
    # option = OptionMenu(filewin, var, "one", "two", "three", "four")
    w.grid(row=2,column=0)

    #
    # test stuff

    def ok():
        # addVarToData(var.get())
        # addVariableClassifications(var.get())
        printr("Yo")
        # quitMe()
        # filewin.quit()

    def quittr():
        fl.destroy()

    button = Button(fl, text="OK", command=dircallback5)
    button.grid(row=5,column=0)

    button2 = Button(fl, text="Quit", command=quittr)
    button2.grid(row=5,column=2)

def addVariableClassifications(vard):

    # filewin = Toplevel(root)
    # filewin.title("Enter Number of classifications for variable {0}".format(vard))
    # filewin.minsize(400, 250)
    variableClasses = {}

    def reint4(num):
        classientry.delete(0, END)
        classientry.insert(0, "0")
        # e.after(100, reint)

    # def reloadMainr():
    #     f1.destroy()
        # deleteMessage(mo)
        # createMessage(mo)




    def exportr():
        printr("Waddup")
        # setC(newCof,data)
        # setCoefficients(newCof,data)
        # coeffNEdit = True


    def dircallback5():

        # def show_values():
        #     print (sr, w1.get(), w2.get(), w3.get(), w4.get())
            # for es in entries.keys():
            #     print es
        def printm():
            print(getVarClasses())

        def set_marks():

            vc0 = {}
            vcF = {}
            vc0["Min"] = 0
            vc0["Max"] = (float(entry1.get()) / 100)
            vc0["Value"] = int(entry2.get())
            variableClasses[0] = vc0
            vcF["Min"] = (float(entryo.get()) / 100)
            vcF["Max"] = 1
            vcF["Value"] = int(entryo2.get())
            count = 1
            for et in entries:
                entr = entries[et]
                vc = {}
                vc["Min"] = (float((entr["Less"]).get()) / 100)
                vc["Max"] = (float((entr["More"]).get()) / 100)
                vc["Value"] = int(entr["Value"].get())
                variableClasses[count]  = vc
                # print (entries[et]).get()
                count = count + 1
                print et
            variableClasses[count] = vcF
            addVarClassesToData(vard,variableClasses)
            f1.destroy()
            fa.destroy()
            addVariableToSegments(vard)


        # if getSegOpen() == True:
        #     f1.destroy()
        sr = classientry.get()
        j = int(sr)
        k = 1
        entries = {}
        lbls = {}
        f1 = LabelFrame(root)
        f1.pack()
        statusvar = StringVar(f1, value="New Variable", name="Status Bar")
        statusbar = ttk.Label(f1, textvariable=statusvar, background="#FFFFCC")
        statusbar.grid(row=0, column=0, columnspan=9, sticky="EW")
        rb = Label(f1, text="Set Variable Percentile Classifications for {0}".format(vard), font = "Helvetica 18")
        rb.grid(row=1,column=1)
        r = Label(f1, text="Less than x percentile", font = "Helvetica 12")
        r.grid(row=2,column=1)
        entry1 = Entry(f1, width=5)
        entry1.grid(row=2, column=3, columnspan=1, sticky="EW")
        entry1.delete(0, END)
        entry1.insert(0, "0")
        r2 = Label(f1, text="Value:", font = "Helvetica 12")
        r2.grid(row=2,column=4)
        entry2 = Entry(f1, width=5)
        entry2.grid(row=2, column=5, columnspan=1, sticky="EW")
        entry2.delete(0, END)
        entry2.insert(0, "")
        while k < (j-1):
            lbl = {}
            lbl["One"] = Label(f1, text="Between x and x percentile", font = "Helvetica 12")
            lbl["One"].grid(row=(k+2),column=1)
            ent = {}
            ent["Less"] = Entry(f1, width=3)
            ent["Less"].grid(row=(k+2), column=3, columnspan=1, sticky="EW")
            ent["Less"].delete(0, END)
            ent["Less"].insert(0, "")
            ent["More"] = Entry(f1, width=3)
            ent["More"].grid(row=(k+2), column=4, columnspan=1, sticky="EW")
            ent["More"].delete(0, END)
            ent["More"].insert(0, "")
            lbl["Two"] = Label(f1, text="Value:", font = "Helvetica 12")
            lbl["Two"].grid(row=(k+2),column=5)
            ent["Value"] = Entry(f1, width=3)
            ent["Value"].grid(row=(k+2), column=6, columnspan=1, sticky="EW")
            ent["Value"].delete(0, END)
            ent["Value"].insert(0, "")
            entries[k] = ent
            lbls[k] = lbl

            k = k + 1

        o = Label(f1, text="Greater than x percentile", font = "Helvetica 12")
        o.grid(row=(j+2),column=1)
        entryo = Entry(f1, width=5)
        entryo.grid(row=(j+2), column=3, columnspan=1, sticky="EW")
        entryo.delete(0, END)
        entryo.insert(0, "")
        o2 = Label(f1, text="Value:", font = "Helvetica 12")
        o2.grid(row=(j+2),column=4)
        entryo2 = Entry(f1, width=5)
        entryo2.grid(row=(j+2), column=5, columnspan=1, sticky="EW")
        entryo2.delete(0, END)
        entryo2.insert(0, "10")

        bb = Button(f1, text='Set Values', command=set_marks)
        bb.grid(row=(j+3),column=1)

        cc = Button(f1, text='Print Values', command=printm)
        cc.grid(row=(j+3),column=3)


    fa = LabelFrame(root)
    fa.pack()

    statusvar = StringVar(fa, value="Number of classifications", name="Status Bar")
    statusbar = ttk.Label(fa, textvariable=statusvar, background="#FFFFCC")
    statusbar.grid(row=0, column=0, columnspan=7, sticky="EW")

    variableTx = StringVar(fa, value="", name="Number of Classifications")
    label = ttk.Label(fa, text="# Of Classifications")
    label.grid(row=1, column=0)

    classientry = Entry(fa, width=5)
    classientry.grid(row=1, column=1, columnspan=5, sticky="EW")
    classientry.delete(0, END)
    classientry.insert(0, "")

    b = Button(fa, text="Create", width=15, command=dircallback5)
    b.grid(row=2, column=3)

    c = Button(fa, text="Quit", width=15, command=fa.quit)
    c.grid(row=2, column=4)


    # data = getCoefficients()
    # curSeg = data[sr]
    # if sr in newCof:
    #     curSeg = newCof[sr]
    #     print "YaYa"
    # # f.destroy()
    # f1 = LabelFrame(root)
    # f1.pack()
    # # segOpen = True
    # printr(sr)
    # r = Label(f1, text="Current Segment: {}".format(sr), font = "Helvetica 16 bold")
    # r.pack()
    # wa = Label(f1, text=ps[0])
    # wa.pack()
    # w1 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
    # w1.set(curSeg[ps[0]])
    # w1.pack()
    # wb = Label(f1, text=ps[1])
    # wb.pack()
    # w2 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
    # w2.set(curSeg[ps[1]])
    # w2.pack()
    # wc = Label(f1, text=ps[2])
    # wc.pack()
    # w3 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
    # w3.set(curSeg[ps[2]])
    # w3.pack()
    # wd = Label(f1, text=ps[3])
    # wd.pack()
    # w4 = Scale(f1, from_=-10, to=10, length=600,tickinterval=.5, orient=HORIZONTAL)
    # w4.set(curSeg[ps[3]])
    # w4.pack()

    # w = apply(OptionMenu, (filewin, var) + tuple(acsVariables))
    # # option = OptionMenu(filewin, var, "one", "two", "three", "four")
    # w.grid(row=2,column=0)

    #
    # test stuff

    # def ok():
    #     addVarToData(var.get())
    #     addVariableClassifications(var.get())
    #     filewin.quit()
    #
    # def quitMe():
    #     filewin.quit()
    #
    # button = Button(filewin, text="OK", command=ok)
    # button.grid(row=5,column=0)
    #
    # button2 = Button(filewin, text="Quit", command=quitMe)
    # button.grid(row=5,column=2)


def init_GUI():
    # root = Tk()
    # root.title("Segmentr")
    # root.minsize(1000, 400)

    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Set Working Directory", command=setWkDir)
    filemenu.add_command(label="Set Data Location", command=chooseDataLoc)
    filemenu.add_command(label="Select State", command=selectState2)
    filemenu.add_command(label="New Variable", command=addVariable)
    filemenu.add_command(label="New Segment", command=addSegment)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    segmentmenu = Menu(menubar, tearoff=0)
    segmentmenu.add_command(label="Edit Segmentation Coefficients", command=editSegmentCoefficients)
    segmentmenu.add_command(label="Edit Segment Weightings", command=donothing)
    segmentmenu.add_command(label="Edit Variable Weightings", command=donothing)
    menubar.add_cascade(label="Edit", menu=segmentmenu)

    runmenu = Menu(menubar, tearoff=0)
    runmenu.add_command(label="Run Segmentr", command=segmentz)
    runmenu.add_separator()
    runmenu.add_command(label="Run Mappr", command=displayMap)
    menubar.add_cascade(label="Run", menu=runmenu)

    exportmenu = Menu(menubar, tearoff=0)
    exportmenu.add_command(label="Export CSV", command=donothing)
    exportmenu.add_command(label="Export SHP", command=joint)
    exportmenu.add_command(label="Export Hotspots SHP", command=getHotspots)
    menubar.add_cascade(label="Export", menu=exportmenu)

    expressmenu = Menu(menubar, tearoff=0)
    expressmenu.add_command(label="Express Download + Write to SHP", command=xpress)
    menubar.add_cascade(label="Express", menu=expressmenu)

    root.config(menu=menubar)

    createMessage(mo,bc)

    # sm = StringVar()
    # label = Label( root, textvariable=sm)
    # smessage = getWDStatus()
    # sm.set(smessage)

    root.mainloop()

# def reloadMain():


#### Global Variables

scc = ''
workdirSet = True
datadirSet = True
stateSet = False

workdir = 'C:/Sego/'

datadir = "C:/Users/kdenny/Documents/SegmentrBase/"
paths = {}
states = []

### Tkinter GUI

root = Tk()
root.title("Segmentr")
root.minsize(1000, 400)
mo = LabelFrame(root)
mo.pack(side="top")

# a = StringVar()
# message = ""
# setMessage("")
# a.set(message)

init_GUI()

