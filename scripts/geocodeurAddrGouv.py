import requests, csv, json, time


base_url = "https://api-adresse.data.gouv.fr/search/?"
out = open("listeAdressesDedoubl_AZ_histogeoloc_geolocdatagouv.csv","w") 
out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 
with open('listeAdressesDedoubl_AZ_histogeoloc.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			out_writer.writerow(['adresse', 'num', 'proprio[global]', 'proprio_titre*', 'proprio_particule*','proprio_name*', 'proprio_ad', 'proprio_numAd', 'proprio_region*', 'same_place*' , 'x', 'y', 'postcode_en2020', 'source', 'url', 'score'])
			print(['adresse', 'num', 'proprio[global]', 'proprio_titre*', 'proprio_particule*','proprio_name*', 'proprio_ad', 'proprio_numAd', 'proprio_region*', 'same_place*' , 'x', 'y', 'postcode_en2020', 'source', 'url', 'score'])
			#print(f'Column names are {", ".join(row)}')
			line_count += 1
		else:
			line_count += 1
			adres=row[1]+" "+row[0]
			params = {"q":adres.replace(" ", "+"), "city":"paris"}
			#print("adresse: "+row[1]+" "+row[0])
			url = base_url + "q"+"="+ adres.replace(" ", "+") + "&" +"city"+ "=" + "paris" 
			#print("requete: "+url)
			r = requests.get(base_url, params)
			if r.status_code == 200:
				if (r.json()):
					if (len(r.json()['features']) > 0):
						print(r.json()['features'][0])
						x = r.json()['features'][0]['geometry']['coordinates'][0]
						y = r.json()['features'][0]['geometry']['coordinates'][1]
						postc = r.json()['features'][0]['properties']['postcode']
						score = r.json()['features'][0]['properties']['score']
						source = "https://api-adresse.data.gouv.fr" #
						print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], x, y, postc, source, url, score])
						out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], x, y, postc, source, url, score])
					else:
						print("ADRESSE A VERIFIER:"+row[1]+" "+row[0])
						out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", "", "", "", url, ""])
						print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", "", "", "", url, ""])
				else:
					print("ADRESSE A VERIFIER:"+row[1]+" "+row[0])
					out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", "", "", "", url, ""])
					print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", "", "", "", url, ""])
			if (line_count % 500 == 0):
				time.sleep(5)
out.close()	