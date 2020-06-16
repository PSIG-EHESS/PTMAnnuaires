import requests
import csv
import json

base_url = "http://api.geohistoricaldata.org/geocoding?"
out = open("listeAdressesDedoubl_AZ_histogeoloc.csv","w") 
out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 
with open('listeAdressesDedoubl_AZ.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			out_writer.writerow(['adresse', 'num', 'proprio[global]', 'proprio_titre*', 'proprio_particule*','proprio_name*', 'proprio_ad', 'proprio_numAd', 'proprio_region*', 'same_place*' , 'x', 'y', 'source', 'url'])
			#print(f'Column names are {", ".join(row)}')
			line_count += 1
		else:
			line_count += 1
			params = {"address":row[1]+" "+row[0], "date":"1898", "precision":"true", "maxresults":1}
			print("adresse: "+row[1]+" "+row[0])
			print("requete: "+base_url + "address"+"="+ row[1]+" "+row[0] + "&" +"date"+ "=" + "1898" + "&precision=true&maxresults=1")
			r = requests.get(base_url, params)
			if r.status_code == 200:
				if (r.json()):
					source = str(r.json()[0]['historical_source'])
					print(source)
					url = base_url + "address"+"="+ row[1]+" "+row[0] + "&" +"date"+ "=" + "1898" + "&precision=true&maxresults=1"
					x = str(r.json()[0]['geometry']['geometries'][0]['coordinates'][0][0])
					print(x)
					y = str(r.json()[0]['geometry']['geometries'][0]['coordinates'][0][1])
					print(y)
					print("")
					out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], x, y, source, url])	
				else:
					print("ADRESSE A VERIFIER:"+row[1]+" "+row[0])
					out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
out.close()	