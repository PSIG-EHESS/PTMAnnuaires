import requests
import csv
import json
import time


base_url = "https://api-adresse.data.gouv.fr/search/?"
out = open("3_DataGouv_histogeoloc_prop.csv", "w")
out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

with open('0_listeAdressesDedoubl_AZ.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            out_writer.writerow(['adresse', 'num', 'proprio[global]', 'collectif', 'sexe', 'statut_femme', 'proprio_titre*', 'proprio_particule*', 'proprio_name*', 'proprio_ad', 'proprio_numAd', 'commune_propio', 'proprio_region*', 'Pays', 'same_place*', 'commentaire', 'x_prop', 'y_prop', 'postcode_en2020_prop', 'source_prop', 'url_prop', 'score_prop'])
            print(['adresse', 'num', 'proprio[global]', 'collectif', 'sexe', 'statut_femme', 'proprio_titre*', 'proprio_particule*', 'proprio_name*', 'proprio_ad', 'proprio_numAd', 'commune_propio', 'proprio_region*', 'Pays', 'same_place*', 'commentaire', 'x_prop', 'y_prop', 'postcode_en2020_prop', 'source_prop', 'url_prop', 'score_prop'])
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
            adres = row[1] + " " + row[0]
            params = {"q": adres.replace(" ", "+"), "city": "paris"}
            #print("adresse: "+row[1]+" "+row[0])
            url_prop = base_url + "q" + "=" + adres.replace(" ", "+") + "&" + "city" + "=" + "paris"
            #print("requete: "+url)
            r = requests.get(base_url, params)
            if r.status_code == 200:
                if (r.json()):
                    if (len(r.json()['features']) > 0):
                        print(r.json()['features'][0])
                        x_prop = r.json()['features'][0]['geometry']['coordinates'][0]
                        y_prop = r.json()['features'][0]['geometry']['coordinates'][1]
                        postc_prop = r.json()['features'][0]['properties']['postcode']
                        score_prop = r.json()['features'][0]['properties']['score']
                        source_prop = "https://api-adresse.data.gouv.fr"
                        print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], x_prop, y_prop, postc_prop, source_prop, url_prop, score_prop])
                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], x_prop, y_prop, postc_prop, source_prop, url_prop, score_prop])
                    else:
                        print("ADRESSE A VERIFIER:" + row[1] + " " + row[0])
                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_prop, ""])
                        print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_prop, ""])
                else:
                    print("ADRESSE A VERIFIER:" + row[1] + " " + row[0])
                    out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_prop, ""])
                    print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_prop, ""])
            if (line_count % 500 == 0):
                time.sleep(5)
out.close()
