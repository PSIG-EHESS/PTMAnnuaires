import requests
import csv
import json
import time


base_url = "https://api-adresse.data.gouv.fr/search/?"
out = open("4_DataGouv_histogeoloc_dom.csv", "w")
out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

with open('0_listeAdressesDedoubl_AZ.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            out_writer.writerow(['adresse', 'num', 'proprio[global]', 'collectif', 'sexe', 'statut_femme', 'proprio_titre*', 'proprio_particule*', 'proprio_name*', 'proprio_ad', 'proprio_numAd', 'commune_propio', 'proprio_region*', 'Pays', 'same_place*', 'commentaire', 'x_dom', 'y_dom', 'postcode_en2020_dom', 'source_dom', 'url_dom', 'score_dom'])
            print(['adresse', 'num', 'proprio[global]', 'collectif', 'sexe', 'statut_femme', 'proprio_titre*', 'proprio_particule*', 'proprio_name*', 'proprio_ad', 'proprio_numAd', 'commune_propio', 'proprio_region*', 'Pays', 'same_place*', 'x_dom', 'y_dom', 'commentaire', 'postcode_en2020_dom', 'source_dom', 'url_dom', 'score_dom'])
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
            adres = row[10] + " " + row[9]
            params = {"q": adres.replace(" ", "+"), "city": "paris"}
            #print("adresse: "+row[1]+" "+row[0])
            url_dom = base_url + "q" + "=" + adres.replace(" ", "+") + "&" + "city" + "=" + "paris"
            #print("requete: "+url)
            r = requests.get(base_url, params)
            if r.status_code == 200:
                if (r.json()):
                    if (len(r.json()['features']) > 0):
                        print(r.json()['features'][0])
                        x_dom = r.json()['features'][0]['geometry']['coordinates'][0]
                        y_dom = r.json()['features'][0]['geometry']['coordinates'][1]
                        postc_dom = r.json()['features'][0]['properties']['postcode']
                        score_dom = r.json()['features'][0]['properties']['score']
                        source_dom = "https://api-adresse.data.gouv.fr"
                        print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], x_dom, y_dom, postc_dom, source_dom, url_dom, score_dom])
                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], x_dom, y_dom, postc_dom, source_dom, url_dom, score_dom])
                    else:
                        print("ADRESSE A VERIFIER:" + row[1] + " " + row[0])
                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_dom, ""])
                        print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_dom, ""])
                else:
                    print("ADRESSE A VERIFIER:" + row[1] + " " + row[0])
                    out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_dom, ""])
                    print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], "", "", "", "", url_dom, ""])
            if (line_count % 500 == 0):
                time.sleep(5)
out.close()
