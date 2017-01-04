#simplex

import tkMessageBox
from Tkinter import *

import os
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from scipy.io import *

class StartWindow():
    
    def __init__(self):
            self.root = Tk()
            
    def CreateFirstWindow(self):
        self.root.title("Start")
        self.root.geometry("300x250")
        lab1 = Label(text="Liczba zmiennych decyzyjnych").place(x=5, y=20)
        self.variableCountTb = Entry(self.root, width =10)
        self.variableCountTb.place(x= 180, y=20)
        confirmButton = Button(text="Dalej", width=10,command=self.CreateSecondWindow).place(x=110, y=150)
        confirmButton1 = Button(text="Chce liczyc uzywajac pliku .mat", width=35,command=self.InputMatFile).place(x=15, y=200)
        self.root.mainloop()

    def CreateSecondWindow(self):
        self.varCount = self.variableCountTb.get()
        if(not self.varCount.isdigit() or int(self.varCount) == 0 ):
            tkMessageBox.showinfo( "Blad walidacji", "Liczba zmiennych musi byc liczba wieksza od 0")
        elif (int(self.varCount) > 10):
            tkMessageBox.showinfo( "Blad walidacji", "Maksymalna liczba zmiennych = 10")
        else:
            self.root.destroy()
            self.root = Tk()
            self.root.title("Rownania")
            self.root.geometry("700x500")
            self.listZfunc = []
            #dodaje tekstboxy do listy zeby mozna sie bylo do nich odniesc
            for i in range(0, int(self.varCount)):
                textBox = Entry(self.root, width =3)
                self.listZfunc.append(textBox)
            #rysuje textboxy
            lab1 = Label(text="Funkcja celu:").place(x=5, y=20)
            for i in range(0, int(self.varCount)):
                self.listZfunc[i].place(x= i*50+10, y=50)
                if i < int(self.varCount)-1:
                    x = "x" + str(i+1) + "+"
                else:
                    x = "x" + str(i+1)
                lab1 = Label(text=x).place(x=i*50+35, y=50)
            self.optimalizationType = StringVar(self.root)
            self.optimalizationType.set("MAX")
            self.optDropdown = OptionMenu(self.root, self.optimalizationType, "MAX", "MIN").place(x = int(self.varCount)*50+20, y=42)
            confirmButton = Button(text="Ustaw", width=10,command=self.ParseZFunction).place(x=600, y=45)
            confirmButton2 = Button(text="Licz Simplex", width=10,command=self.CreateCanonicEquals).place(x=600, y=280)
            
#####Parsowanie funkcji celu- rownanie wpisane do listZfunct[i]
    def ParseZFunction(self):
        self.listZfuncValue  = []
        self.yForEq=135
        self.DropdownMenuList = []
        self.ListOfEquals = []
        self.ResultsList = []
        z = self.optimalizationType.get() + " -> "
        for i in range(0, int(self.varCount)):
            try:
                #Sprawdzam czy szukam minimum czy maksimum funkcji
                if( str(self.optimalizationType.get()) == "MIN"):
                    self.listZfuncValue.append(int(self.listZfunc[i].get())*(-1.0))
                else:
                    self.listZfuncValue.append(int(self.listZfunc[i].get())*(1.0))
            except ValueError:
                 tkMessageBox.showinfo( "Blad walidacji", "Wszystie zmienne musza byc liczbami")
                 break
            z+=str(self.listZfuncValue[i])
            if i < int(self.varCount)-1:
                z += "x" + str(i+1) + " + "
            else:
                z += "x" + str(i+1)
        lab1 = Label(text=z).place(x=20, y=75)
        self.CreateEqualationTemplate()
        
#tworzenie texboxow funkcji
    def CreateEqualationTemplate(self):
        self.TextBoxList = []
        self.TempList = []
        for i in range(0, int(self.varCount)):
            textBox = Entry(self.root, width =3)
            self.TextBoxList.append(textBox)
        lab1 = Label(text="Rownania i nierownosci:").place(x=5, y=100)
        for i in range(0, int(self.varCount)):
            self.TextBoxList[i].place(x= i*50+10, y=125)
            if i < int(self.varCount)-1:
                x = "x" + str(i+1) + "+"
            else:
                x = "x" + str(i+1)
            lab1 = Label(text=x).place(x=i*50+35, y=125)
        self.equalType = StringVar(self.root)
        self.equalType.set("<=")
        self.equalDropdown = OptionMenu(self.root, self.equalType, "<=", ">=", "=").place(x = int(self.varCount)*50+20, y=121)
#wyniki dla kazdej nierownosci
        self.resultValue = Entry(self.root, width =4)
        self.resultValue.place(x = int(self.varCount)*50+90, y=125)
        confirmButton = Button(text="Dodaj", width=10,command=self.ParseEqualFunctions).place(x=600, y=125)

#parsowanie rownan i nierownosci- wpisywanie do tablicy 2xi
    def ParseEqualFunctions(self):
        z = ""
        #z = self.optimalizationType.get() + " -> "
        for i in range(0, int(self.varCount)):
            try:  
                self.TempList.append(int(self.TextBoxList[i].get()))
                a = int(self.resultValue.get())
            except ValueError:
                 tkMessageBox.showinfo( "Blad walidacji", "Wszystie zmienne musza byc liczbami")
                 break
            z+= str(self.TextBoxList[i].get())
            if i < int(self.varCount)-1:
                z += "x" + str(i+1) + " + "
            else:
                z += "x" + str(i+1)
        if(self.equalType.get() == "<="):
            self.DropdownMenuList.append(1)
        elif (self.equalType.get() == "="):
            self.DropdownMenuList.append(2)
        else:
            self.DropdownMenuList.append(3)
        self.ListOfEquals.append(self.TempList)
        self.ResultsList.append(int(self.resultValue.get()))
        z+=self.equalType.get()
        z+=self.resultValue.get()
        self.yForEq+= 15
        lab1 = Label(text=z).place(x=20, y=self.yForEq)
        self.CreateEqualationTemplate()
        #self.tempEquals = [[0]*len(self.ListOfEquals) for _ in range(len(self.ListOfEquals[0]))]
        #self.tempEquals = self.ListOfEquals
        print 'temp equals po przepisaniu'
        #print self.tempEquals
        
        # wysuj wykres
#        myEquation = []
#        t = np.arange(0., 10., 0.5)
#        for j in range (0, len(self.ListOfEquals)):
#             mytemp = []
#             mytemp.append(self.ResultsList[j]/(self.ListOfEquals[j][0])*(1.0))
#             for i in range (1, int(self.varCount)):
#                 mytemp.append((self.ListOfEquals[j][i])*(-1.0)/(self.ListOfEquals[j][0]))
#             myEquation.append(mytemp)
#        if (int(self.varCount) == 3):
#            plt.plot(t, mytemp[0][0]-t*mytemp[0][1] - t*mytemp[0][2], 'r--', 
#                     t, mytemp[1][0]-t*mytemp[1][1] - t*mytemp[1][2], 'bs',
#                     t, mytemp[2][0]-t*mytemp[2][1] - t*mytemp[2][2], 'g^')
#        plt.show()
#        print 'myEquation'
#        print myEquation
 
    def CreateCanonicEquals(self):
        #tworzenie tabelki 0 i jedynek
        self.howManyRows = len(self.ListOfEquals)
        self.howManyColumn = 0        
        for i in range (0, len(self.DropdownMenuList)):
            if(self.DropdownMenuList[i] == 3):
                self.howManyColumn+=2
            else:
                self.howManyColumn+=1
        additional = self.ZerosMatrix()
        row = 0
        col = 0
        while row < self.howManyRows:
            while col < self.howManyColumn:
                if(self.DropdownMenuList[row]==3):                    
                    additional[row][col]=-1
                    additional[row][col+1]=1
                    row += 1
                    col += 2
                else:
                    additional[row][col]=1
                    row+=1
                    col+=1
        #dodanie tabeli 0 i 1 do tabeli rownan
        for rows in range(0, self.howManyRows):
            self.ListOfEquals[rows].extend(additional[rows])            
        print(self.ListOfEquals)
        #Dodanie odpowiednich wartosci do funkcji celu
        for i in range (0, len(self.DropdownMenuList)):
            if (self.DropdownMenuList[i] == 1):
                self.listZfuncValue.extend([0])
            elif (self.DropdownMenuList[i] == 2):
                self.listZfuncValue.extend([-999999])
            else:
                self.listZfuncValue.extend([0])
                self.listZfuncValue.extend([-999999])
        print (self.listZfuncValue)
        self.CreateCbMatrix()
        #Wywolanie Simplex
        sim = Simplex(self.listZfuncValue, self.ListOfEquals, self.ResultsList, self.CbMatrix, self.root, self.baseVarMatrix)
        sim.CalculateFirstSimplex()
        
    def CreateCbMatrix(self):
        self.CbMatrix = []
        self.baseVarMatrix = []
        position = len(self.ResultsList)-1
        for i in range (0, len(self.DropdownMenuList)):
            if (self.DropdownMenuList[i] == 1):
                self.CbMatrix.extend([0])
                position+=1
                self.baseVarMatrix.append(position)
            elif(self.DropdownMenuList[i] == 2):
                self.CbMatrix.extend([-999999])
                position+=1
                self.baseVarMatrix.append(position)
            else:
                self.CbMatrix.extend([-999999])
                position+=2
                self.baseVarMatrix.append(position)
        print (self.CbMatrix)
        print (self.baseVarMatrix)

    
    def ZerosMatrix(self):
        matrix = [[0]*self.howManyColumn for _ in range(self.howManyRows)]
        return matrix
        
    def InputMatFile(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title("Wczytaj plik .mat")
        self.root.geometry("700x100")
        lab1 = Label(text="Sciezka pliku .mat:").place(x=10, y=20)
        self.myPath = Entry(self.root, width =90)
        self.myPath.place(x= 111, y=20)
        confirmButton = Button(text="Wczytaj plik", width=15, command=self.ReadMatFile).place(x=300, y=55)
        
    def ReadMatFile(self):
        self.path = os.path.abspath(self.myPath.get())
        
        if not os.path.exists(self.path):
            tkMessageBox.showinfo( "Blad walidacji", "Podana sciezka jest niepoprawna")
        elif not self.path.endswith('.mat'):
            tkMessageBox.showinfo( "Blad walidacji", "Probujesz podac plik z innym rozszerzeniem niz .mat")
        else:
            x = loadmat(self.path)
            self.A = x['A'].toarray() #30x48 nierownosci- 30 wierszy
            self.Aeq = x['Aeq'].toarray() #20x48 rownan- 20 wierszy
            self.matB = x['b'] #wyniki nierownosci- lista list
            self.matBeq = x['beq'] #wyniki rownosci
            self.matF = x['f'] #funkcja celu
            self.ListsCreationMatFile()
            
    def ListsCreationMatFile(self):
        self.Amatrix=[]
        for i in range(0, len(self.A)):
            self.Amatrix.append(self.A[i])
        for i in range(0, len(self.Aeq)):
            self.Amatrix.append(self.Aeq[i])
        
        tempmatrix = [[0]*len(self.Amatrix) for _ in range(len(self.Amatrix))]
        for i in range(0, len(self.Amatrix)):
            for j in range(0,len(self.Amatrix)):
                if (i == j):
                    tempmatrix[j][i] = 1
        
        #for i in range(0, len(self.Amatrix)):
        self.Amatrix = np.append(self.Amatrix, tempmatrix, 1) 
        print len(self.Amatrix)
        print len(self.Amatrix[0])
        print (self.Amatrix)
        #### Z function conversion
        tempmatrix = []
        self.Cbmat = []
        self.AddVarmat = []
        for i in range(0, len(self.matF)):
            tempmatrix.append(self.matF[i][0])
            
        for i in range(0, len(self.A)):
            tempmatrix.append(0)
            self.Cbmat.append(0)
        for i in range(0, len(self.Aeq)):
            tempmatrix.append(-999999)
            self.Cbmat.append(-999999)
        for i in range(len(self.A[0]), len(self.Amatrix[0])):
            self.AddVarmat.append(i)
        self.matF = tempmatrix
        print self.AddVarmat
        print len(self.AddVarmat)
        ### List of results
        self.Resultsmat = []
        for i in range(0, len(self.matB)):
            self.Resultsmat.append(self.matB[i][0])
        for i in range(0, len(self.matBeq)):
            self.Resultsmat.append(self.matBeq[i][0])
        print self.Resultsmat
        print  len(self.Resultsmat)
        
        sim = Simplex(self.matF, self.Amatrix, self.Resultsmat, self.Cbmat, self.root, self.AddVarmat)
        sim.CalculateFirstSimplex()


###########################################     SIMPLEX       ######################################################


class Simplex:

    def __init__(self, zFunctionList, equalsList, resultList, CbMatrix, myroot, addVariables):
        self.zList = zFunctionList
        self.equals = equalsList
        self.results = resultList
        self.cb = CbMatrix
        self.zj = []
        self.cj_zj = []
        self.root = myroot
        self.additionalVariables = addVariables
        
        
    def DrawSimplexTable(self, funZ, cb, eq, res, zj,addV, cj_zj ):
    #zlikwidowanie poprzedniego okna i nowe puste
        self.root.destroy()
        self.root = Tk()
        self.root.title("Tabela Simplex")
        self.root.geometry("700x500")
        self.myY = 30
        z=""
        z+=  "Cb" + "\t" + "Cj"
        for i in range (0, len(funZ)):
            z+= "\t"
            if(funZ[i]>=9999):
                z+="m"
            elif(funZ[i]<=-9999):
                z+="-m"
            else:            
                z+= str(funZ[i])
        lab1 = Label(text=z).place(x=30, y=self.myY)
        z ="\t"
        z+="Zm."

        for i in range (0, len(funZ)):
            z+="\t"
            z+= "x" + str(i+1)
        z+= "\tRozwiazania"
        self.myY+=20
        lab1 = Label(text=z).place(x=30, y=self.myY)
        
        
        for i in range(0, len(cb)):
            z=""
            if(cb[i]>=9999):
                z+="m"
            elif(cb[i]<=-9999):
                z+="-m"
            else:            
                z+= str(cb[i]) 

            z+= "\t" + "x"+str(addV[i]+1 )
            for j in range(0,len(zj)):
                z+="\t"
                z+=str(eq[i][j])
            z+="\t" +str(res[i])
            self.myY+=20
            lab1 = Label(text=z).place(x=30, y=self.myY)

        z="\tZj"        
        for i in range(0, len(zj)):
            z+="\t"
            if(zj[i]>=9999):
                z+="m"
            elif(zj[i]<=-9999):
                z+="-m"
            else:            
                z+= str(zj[i])
        self.myY+=20
        lab1 = Label(text=z).place(x=30, y=self.myY)

        z="\tCj-Zj"        
        for i in range(0, len(cj_zj)):
            z+="\t"
            if(cj_zj[i]>=9999):
                z+="m"
            elif(cj_zj[i]<=-9999):
                z+="-m"
            else:            
                z+= str(cj_zj[i])
        self.myY+=20
        lab1 = Label(text=z).place(x=30, y=self.myY)
        
    def CalculateFirstSimplex(self):
        self.CalculateZj() # liczy zj i wywoluje Coutzj_cj        

        self.DrawSimplexTable(self.zList,self.cb, self.equals, self.results, self.zj, self.additionalVariables, self.cj_zj)
        self.myY +=50         
        confirmButton = Button(text="Dalej", width=10,command=self.CalculateSimplex).place(x=600, y=10)#y=self.myY) 

    def CalculateSimplex(self):
          
        if(self.SimplexCheck(self.cj_zj)):
            self.myY+=30
            lab1 = Label(text="Rozwiazanie optymalne").place(x=30, y=self.myY)
            #rysowanie wykresu
            plt.plot(self.results[0], self.results[1], 'ro')
            plt.axis([0, 20, 0, 20])
            plt.show()
            for i in range(0, len(self.additionalVariables)):
                z = ""
                z+="x"+str(self.additionalVariables[i]+1) + " = " + str(self.results[i])
                self.myY+=30
                lab1 = Label(text=z).place(x=30, y=self.myY)
        else:
            self.myY+=30
            lab1 = Label(text="m -> Bardzo duza liczba").place(x=30, y=self.myY)
            self.myY+=30
            lab1 = Label(text="Rozwiazanie nie optymalne").place(x=30, y=self.myY)
            
            self.CreateNewSimplexTable(self.cj_zj, self.results, self.equals)
            
            self.CalculateZj() # liczy zj i wywoluje Coutzj_cj        
            self.DrawSimplexTable(self.zList,self.cb, self.equals, self.results, self.zj, self.additionalVariables, self.cj_zj)
            self.myY +=50         
            confirmButton = Button(text="Dalej", width=10,command=self.CalculateSimplex).place(x=600, y=10)#y=self.myY)   

    def FindNewColumn(self, cj_zj):
        mx = max(cj_zj)
        print("new col")
        print(cj_zj.index(mx))
        return cj_zj.index(mx)

    def FindNewRow(self, cj_zj, resultList, equals):
        tmp = []
        columnIndex = self.FindNewColumn(cj_zj)
        for i in range(0,len(resultList)):
            if (equals[i][columnIndex] == 0):
                tmp.append(999999)
            else:
                tmp.append(resultList[i]/equals[i][columnIndex])
        print("tmp row")
        print(tmp)
        mi = min(filter(lambda x: x >= 0, tmp))
        print("new row")
        print(tmp.index(mi))
        return tmp.index(mi)

    def CreateNewSimplexTable(self, cj_zj,resultList, equals):
        col = self.FindNewColumn(cj_zj)
        row = self.FindNewRow(cj_zj, resultList, equals)
        self.cb[row] = self.zList[col]
        self.additionalVariables[row] = col
        self.CalculateNewEqualsFirstRow(row, col)

    def CalculateNewEqualsFirstRow(self, row, col):
        self.tempMatrix = self.equals
        self.tempResult = self.results
        self.simplexCrit = self.tempMatrix[row][col]

        for i in range(0, len(self.tempMatrix[0])):
            self.tempMatrix[row][i] = self.tempMatrix[row][i]/self.simplexCrit*(1.0)
        self.tempResult[row] = self.tempResult[row]/self.simplexCrit*(1.0)

        self.CalculateNewEqualsOthers(row, col)


    def CalculateNewEqualsOthers(self, row, col):
        
        for i in range(0,len(self.results)):
            simplexC = self.tempMatrix[i][col]
            if(i != row):
                for j in range(0, len(self.tempMatrix[0])):
                    mult = simplexC * self.tempMatrix[row][j]*(1.0)
                    self.tempMatrix[i][j] = self.tempMatrix[i][j] - mult
                self.tempResult[i] = self.tempResult[i]-( simplexC* self.tempResult[row])

        self.results = self.tempResult
        self.equals = self.tempMatrix
        # self.CalculateSimplex()
                          


    def CalculateZj(self):
        self.zj = []
        for i in range(0, len(self.zList)):
            temp = 0
            for j in range(0, len(self.cb)):                
                temp+= self.cb[j]*self.equals[j][i]
            self.zj.append(temp)

        print(self.zj)
        self.CalculateCj_Zj()

    def CalculateCj_Zj(self):
        self.cj_zj = []
        for i in range(0, len(self.zList)):            
            self.cj_zj.append(self.zList[i] - self.zj[i])
        print("cj_zj z funkcji cj zj")
        print(self.cj_zj)        
        

    def SimplexCheck(self, cj_zj):
        print("cj_zj z funkcji sprawdzajacej")
        print(cj_zj)
        res = False   
        for i in range(0,len(cj_zj)):
            if(cj_zj[i]>0):
                res =  False
                break                
            else:
                res = True
        return res
        


    


###################################  Main () ######################################
x = StartWindow()
x.CreateFirstWindow()


