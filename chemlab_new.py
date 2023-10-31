import sys
import sqlite3
import csv
import pandas as pd
import csv


class Molecules():
    # Initializing the connection and cursor object to it.
    def __init__(self):
        self.connection = None
        self.cursor = None

    # connect with a database --argument is database name!
    def CreateConnection(self, database_name):
        try:
            self.connection = sqlite3.connect(
                database_name, check_same_thread=False)
        except Exception as e:
            print("Error: "+str(e))
        else:
            print("Database connection succeeded")
        return self.connection

    # Databse Management - loading all information present in csv file
    def Load_Molecules(self, file_):
        # All Commands related to database;
        # Chemdatafile - CSV file
        print("Loading database")

        query_drop = "DROP TABLE IF EXISTS hyd;"
        try:
            self.cursor.execute(query_drop)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        query1 = '''
            CREATE TABLE IF NOT EXISTS hyd (
                formula VARCHAR(50) NOT NULL,
                smiles_format VARCHAR(50) NOT NULL,
                mol_wt DECIMAL(38, 5) NOT NULL,
                pubchem_status VARCHAR(50) NOT NULL,
                pubchem_cid VARCHAR(50) NOT NULL,
                iupac_name VARCHAR(100) NOT NULL,
                Name VARCHAR(200) NOT NULL,
                RotationalconstantA DECIMAL(38, 5) NOT NULL,
                RotationalconstantB DECIMAL(38, 5) NOT NULL,
                RotationalconstantC DECIMAL(38, 5) NOT NULL,
                Dipolemoment DECIMAL(38, 5) NOT NULL,
                HOMO DECIMAL(38, 5) NOT NULL,
                LUMO DECIMAL(38, 5) NOT NULL,
                EnergyGap DECIMAL(38, 5) NOT NULL,
                Zeropointenergy DECIMAL(38, 5) NOT NULL,
                Finalsinglepointenergy DECIMAL(38, 5) NOT NULL,
                Totalthermalenergy DECIMAL(38, 5) NOT NULL,
                TotalEnthalpy DECIMAL(38, 5) NOT NULL,
                Totalentropy DECIMAL(38, 5) NOT NULL,
                Gibbsfreeenergy DECIMAL(38, 5) NOT NULL
            );
        '''

        if (file_):
            file = open('./hyd.csv')
        else:
            file = open('./hyd.csv')
        # Now, Read the contents from the file using csv reader
        contents = csv.reader(file)
        contents2 = next(contents)
        # Already the table has been created, the rest is to insert all the info
        query2 = "INSERT INTO hyd values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        try:
            self.cursor.execute(query1)
            self.cursor.executemany(query2, contents)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))

        print("Loading database has been done...")


        # connect with a database --argument is database name!
        def CreateConnection(self, database_name):
            try:
                self.connection = sqlite3.connect(
                    database_name, check_same_thread=False)
            except Exception as e:
                print("Error: "+str(e))
            else:
                print("Database connection succeeded")
            return self.connection

        

        # Retrieving information using and condition -- molecules with only the specified elements
        def RetrieveElements_AND(self, table_name):
            RetrievedList = []
            query = f"SELECT * FROM {table_name} WHERE (smiles_format like '%C%' or smiles_format like '%c%') AND (smiles_format like '%H%' or smiles_format like '%h%');"
            try:
                self.cursor.execute(query)
                RetrievedList = self.cursor.fetchall()
            except Exception as e:
                print("Query failed while executing the defined statement!: "+str(e))
            return RetrievedList


    # Retrieving all the Information using the table name
    def RetrieveFullInfo(self, table_name):
        RetrievedList = []
        query = f"SELECT * FROM {table_name};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
   
    def RetrieveSmiles(self, table_name):
        RetrievedList = []
        query = f"SELECT smiles_format FROM {table_name}"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
            print(RetrievedList)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    
    def Retrieveformula(self, table_name):
        RetrievedList = []
        query = f"SELECT formula FROM {table_name}"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
            # RetrievedList = Molecules().Retrieveformula("my_table_name")
            # print(RetrievedList)
            # print(RetrievedList)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList

    # RetrievedList = Molecules().Retrieveformula("my_table_name")
    # print(RetrievedList)
    
    # def MolFromStoichiometry(self, table_name, c_val, h_val):
    #     print("the stochiometry is: "+'C'+str(c_val)+'H'+str(h_val))
    #     RetrievedList = []
    #     # query = f"SELECT * FROM {table_name} WHERE formula=(?);"
    #     query = f"SELECT * FROM {table_name} WHERE formula LIKE 'C{c_val}H{h_val}';"
    #     try:
    #         self.cursor.execute(query, ('C'+str(c_val)+'H'+str(h_val),))
    #         RetrievedList = self.cursor.fetchall()
    #         RetrievedList = [list(row) for row in RetrievedList if row[2] == 'C'+str(c_val)+'H'+str(h_val)]
    #         # print(RetrievedList)
    #         print("query:", query)
    #         print("params:", ('C'+str(c_val)+'H'+str(h_val),))
    #     except Exception as e:
    #         print("Query failed while executing the defined statement!: "+str(e))
    #     return RetrievedList
    
    # Testing function
    # class ChemLab:
    def MolFromStoichiometry(self, table_name, c_val, h_val):
        """
        Retrieve a list of chemical compounds from a database table based on the stoichiometry of carbon and hydrogen atoms.

        Args:
        - table_name (str): the name of the database table to query.
        - c_val (int): the number of carbon atoms in the compound.
        - h_val (int): the number of hydrogen atoms in the compound.

        Returns:
        - RetrievedList (list): a list of chemical compounds that match the specified stoichiometry.
        """
        print("the stochiometry is: "+'C'+str(c_val)+'H'+str(h_val))
        RetrievedList = []
        # query = f"SELECT * FROM {table_name} WHERE formula=(?);"
        # query = f"SELECT * FROM {table_name} WHERE formula LIKE 'C{c_val}H{h_val}';"
        # query = f"SELECT * FROM {table_name} WHERE TRIM(formula) LIKE 'C{c_val}H{h_val}';"
        query = f"SELECT * FROM {table_name} WHERE TRIM(formula) = TRIM('C{c_val}H{h_val}');"
        # query = f"SELECT * FROM {table_name} WHERE TRIM(formula) = 'C{c_val}H{h_val}';"

        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
            RetrievedList = [list(row) for row in RetrievedList if row[0] == 'C'+str(c_val)+'H'+str(h_val)]
            print(RetrievedList)
            print("query:", query)
            print("params:", ('C'+str(c_val)+'H'+str(h_val),))
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
        
     # Retrieving properties using smile representation
    def MolFromSmile(self, table_name, smile_rep):
        print("the smile rep is: "+smile_rep)
        RetrievedList = []
        query = "SELECT * FROM {} WHERE smiles_format=(?) or smiles_format=(?);".format(table_name)
        try:
            self.cursor.execute(query, (smile_rep, smile_rep.upper()))
            RetrievedList = self.cursor.fetchall()
            print(RetrievedList)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))

        return RetrievedList

     # Retrieving info using molecular weight
    def RetrieveMolecularWeight(self, table_name, mol_wt):
        query = f"SELECT * FROM {table_name} WHERE mol_wt={mol_wt};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    
    # Retrieving info using pubchem status
    def RetrievePubchemStatus(self, table_name, status):
        query = f"SELECT * FROM {table_name} WHERE pubchem_status='{status}';"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    
    # Retrieving info using pubchem cid

    def RetrievePubchemCID(self, table_name, cid):
        query = f"SELECT * FROM {table_name} WHERE pubchem_cid='{cid}';"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using iupac name

    def RetrieveIUPACName(self, table_name, iupac_name):
        query = f"SELECT * FROM {table_name} WHERE iupac_name='{iupac_name}';"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    
    # Retrieving info using name
    def RetrieveInfoByName(self, table_name, name):
        query = f"SELECT * FROM {table_name} WHERE Name='{name}';"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList


    # Retrieving info using a,b,c constants
    def RetrieveRotationalConstants(self, table_name, a, b, c):
        query = f"SELECT * FROM {table_name} WHERE RotationalconstantA=? AND RotationalconstantB=? AND RotationalconstantC=?;"
        self.cursor.execute(query, (a, b, c,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using dipole moment
    def RetrieveDipoleMoment(self, table_name, DipoleMoment):
        query = f"SELECT * FROM {table_name} WHERE Dipolemoment=?;"
        self.cursor.execute(query, (DipoleMoment,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
  
    def RetrieveHighestOccupiedMolecularOrbit(self, table_name, MO):
        query = f"SELECT * FROM {table_name} WHERE HOMO=?;"
        self.cursor.execute(query, (MO,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using lumo value
    def RetrieveLowestUnoccupiedMolecularOrbit(self, table_name, MO):
        query = f"SELECT * FROM {table_name} WHERE LUMO=?;"
        self.cursor.execute(query, (MO,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using gap value
    def RetrieveGap(self, hl, table_name):
        query = f"SELECT * FROM {table_name} WHERE EnergyGap={hl};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
  
    # Retrieving info using ZPVE value
    def RetrieveZeroPointVibrationalEnergy(self, table_name, VE):
        query = f"SELECT * FROM {table_name} WHERE Zeropointenergy={VE};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using single-point energy 
    def RetrieveSinglePointEnergy(self, table_name, SE):
        query = f"SELECT * FROM {table_name} WHERE Finalsinglepointenergy={SE};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using u  
    def RetrieveInternalEnergy(self, table_name, u=None):
        query = f"SELECT * FROM {table_name} WHERE Totalthermalenergy={u};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using h 
    def RetrieveEnthalpy(self, table_name, h=None):
        query = f"SELECT * FROM {table_name} WHERE TotalEnthalpy={h};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using s
    def RetrieveEntropy(self, table_name, s=None):
        query = f"SELECT * FROM {table_name} WHERE Totalentropy={s};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using g 
    def RetrieveGibbsFreeEnergy(self, table_name, g=None):
        query = f"SELECT * FROM {table_name} WHERE Gibbsfreeenergy={g};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
 
if (__name__ == "__main__"):
    QueryDB = Molecules()
    # Connect with the sqlite databse
    QueryDB.CreateConnection("hyd.db")
    QueryDB.cursor = QueryDB.connection.cursor()
    # Load molecules
    QueryDB.Load_Molecules(True)
    QueryDB = Molecules()
    # Connect with the sqlite database
    QueryDB.CreateConnection("hyd.db")
    # add cursor object to the molecules prototype
    QueryDB.cursor = QueryDB.connection.cursor()
    QueryDB.MolFromStoichiometry('hyd', 5, 4)
    QueryDB.connection.commit()
    QueryDB.MolFromSmile('hyd', 'C[C][CH][CH2]')
    QueryDB.connection.commit()
else:
    QueryDB = Molecules()
    # Connect with the sqlite databse
    QueryDB.CreateConnection("hyd.db")
    # add cursor object to the molecules prototype
    QueryDB.cursor = QueryDB.connection.cursor()
    QueryDB.Load_Molecules(False)
    QueryDB.connection.commit()
