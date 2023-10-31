from flask import Flask, render_template, request, send_file
import sqlite3
import checkpoint as cp
import os
import chemlab_new as btp

app = Flask(__name__)
DB_NAME = "hyd.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_xyz/<filename>')
def get_xyz(filename):
    xyz_dir = os.path.join(app.root_path, 'templates', 'all-xyz')
    xyz_file_path = os.path.join(xyz_dir, filename)

    if os.path.exists(xyz_file_path):
        return send_file(xyz_file_path, as_attachment=True)

    return "XYZ file not found."

@app.route('/chemdata')
def chemdata():
    smile = request.args.get('smile')
    result = []
    try:
        result = cp.get_MolFromSmile(smile)
        print(result)
    except Exception as e:
        print("Molecule from smile Retrieving failed! " + str(e))

    return render_template("chemdata-test.html",
                   name=smile,
                   formula=result[0][0],
                   smiles_format=result[0][1],
                   mol_wt=result[0][2],
                   pubchem_status=result[0][3],
                   pubchem_cid=result[0][4],
                   iupac_name=result[0][5],
                   Name=result[0][6],
                   RotationalconstantA=result[0][7],
                   RotationalconstantB=result[0][8],
                   RotationalconstantC=result[0][9],
                   Dipolemoment=result[0][10],
                   HOMO=result[0][11],
                   LUMO=result[0][12],
                   EnergyGap=result[0][13],
                   Zeropointenergy=result[0][14],
                   Finalsinglepointenergy=result[0][15],
                   Totalthermalenergy=result[0][16],
                   TotalEnthalpy=result[0][17],
                   Totalentropy=result[0][18],
                   Gibbsfreeenergy=result[0][19])

@app.route('/results', methods=['POST'])
def results():
    molecule_name = request.form['molecule_name'].lower()

    if request.form['choice'] == 'choice1':
        try:
            properties = cp.get_physical_properties(molecule_name)
        except:
            return render_template('nophysicochemical.html', name=molecule_name)

        pic_url = cp.get_molecular_picture(molecule_name)
        property_key_list = ["MolecularWeight", "MolecularFormula", "IUPACName", "IsomericSMILES",
                             "CanonicalSMILES", "InChI", "InChIKey", "RotatableBondCount"]
        variable_list = [None] * len(property_key_list)

        for i in range(len(property_key_list)):
            if property_key_list[i] in properties.keys():
                variable_list[i] = properties[property_key_list[i]]

        return render_template('physicochemical.html', name=molecule_name, url=pic_url,
                               formula=variable_list[1], mw=variable_list[0], iupac=variable_list[2],
                               isomericsmile=variable_list[3], canonicalsmile=variable_list[4],
                               inchi=variable_list[5], inchikey=variable_list[6], rb=variable_list[7])

    elif request.form["choice"] == 'choice2':
        result = []
        try:
            result = cp.get_MolFromSmile(molecule_name)
            print(result)
        except Exception as e:
            print("Molecule from smile Retrieving failed! " + str(e))

        
        return render_template("chemdata-test.html",
                       name=molecule_name,
                       formula=result[0][0],
                       smiles_format=result[0][1],
                       mol_wt=result[0][2],
                       pubchem_status=result[0][3],
                       pubchem_cid=result[0][4],
                       iupac_name=result[0][5],
                       Name=result[0][6],
                       RotationalconstantA=result[0][7],
                       RotationalconstantB=result[0][8],
                       RotationalconstantC=result[0][9],
                       Dipolemoment=result[0][10],
                       HOMO=result[0][11],
                       LUMO=result[0][12],
                       EnergyGap=result[0][13],
                       Zeropointenergy=result[0][14],
                       Finalsinglepointenergy=result[0][15],
                       Totalthermalenergy=result[0][16],
                       TotalEnthalpy=result[0][17],
                       Totalentropy=result[0][18],
                       Gibbsfreeenergy=result[0][19])


    elif request.form["choice"] == "choice3":
        c_val = request.form.get("ElementC", "")
        h_val = request.form.get("ElementH", "")

        try:
            # res = cp.get_MolFromStoichiometry(c_val=cf_val, h_val=hf_val)
            res = btp.QueryDB.MolFromStoichiometry('hyd',int(c_val),int(h_val))
            
            print(res) # add this line to print the res variable
            if not res:
                return render_template('nophysicochemical.html', name='Molecule with stoichiometry Retrieving failed!')
            else:
                # results = [list(row) for row in res]
                # return render_template("MolStoichiometry-test.html", c_val=c_val, h_val=h_val, results=results)
                # return render_template("MolStoichiometry-test.html",  res=res)
                return render_template("molstochiometry-testview.html",  res=res, c_val=c_val, h_val=h_val)
        except Exception as e:
            print("Molecule with stoichiometry Retrieving failed! " + str(e))
            return render_template('nophysicochemical.html', name='Molecule with stoichiometry Retrieving failed!')
# data = MolFromStoichiometry(table_name, c_val, h_val)
# return render_template('MolStoichiometry-test.html', data=data)
# def test_choice3():
#     with app.test_client() as client:
#         response = client.post('/results', data={
#             'molecule_name': '',
#             'choice': 'choice3',
#             'ElementC': '1',
#             'ElementH': '4'
#         })
#         assert response.status_code == 200
#         assert b'MolStoichiometry-test.html' in response.data
#         print(response.data)


if __name__ == '__main__':
    app.run(port=5010, host='0.0.0.0')

