import csv

main_filename = 'files/assignee.tsv'
addition_filename_1 = 'files/location_assignee.tsv'
addition_filename_2 = 'files/location.tsv'
output_filename = 'files/assignee_locations_master.tsv'

def add_location(main, addition_1, addition_2, output):
    locationid_to_location = {}
    with open(addition_2, encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
        cnt = 0
        for row in reader:
            cnt += 1
            location_id = row['id']
            country = row['country']
            state = row['state']
            city = row['city']
            lat = row['latitude']
            lng = row['longitude']
            
            locationid_to_location[location_id] = {'country': country, 'state': state, 'city': city, 'lat': lat, 'lng': lng}
            
        print('Number of Rows in ' + addition_2.replace('files/','') + ': ' + str(cnt))
        print('Number of Entries: ' + str(len(locationid_to_location)))
        
    assigneeid_to_locationid = {}
    with open(addition_1, encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        cnt = 0
        for row in reader:
            cnt += 1
            location_id = row['location_id']
            assignee_id = row['assignee_id']
            
            if location_id == '' or assignee_id == '':
                continue
            if assignee_id in assigneeid_to_locationid:
                assigneeid_to_locationid[assignee_id].append(location_id)
            else:
                assigneeid_to_locationid[assignee_id] = [location_id]
            
        print('Number of Rows in ' + addition_1.replace('files/','') + ': ' + str(cnt))
        print('Number of Entries: ' + str(len(assigneeid_to_locationid)))
    
    with open(output, 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        header = ['id', 'organization', 'city', 'state', 'country', 'latitude', 'longitude']
        csv_writer.writerow(header)
        
        with open(main, encoding='utf-8-sig') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in reader:
                assignee_id = row['id']
                organization = row['organization']
                
                #make sure that we only carry over the rows that are organizations, not people
                if organization.strip() == '':
                    continue
                
                if not assignee_id in assigneeid_to_locationid:
                    csv_writer.writerow([assignee_id, organization, '', '', '', '', ''])
                    continue
                
                location_ids = assigneeid_to_locationid[assignee_id]
                
                #make sure that you only have one location per city
                seen_cities = set()
                
                for location_id in location_ids:
                    if not location_id in locationid_to_location:
                        continue
                    else:
                        location_dict = locationid_to_location[location_id]
                        country = location_dict['country']
                        state = location_dict['state']
                        city = location_dict['city']
                        lat = location_dict['lat']
                        lng = location_dict['lng']
                        
                        if city in seen_cities:
                            continue
                        else:
                            csv_writer.writerow([assignee_id, organization, city, state, country, lat, lng])
                            seen_cities.add(city)
    
        
if __name__ == '__main__':
    add_location(main_filename, addition_filename_1, addition_filename_2, output_filename)