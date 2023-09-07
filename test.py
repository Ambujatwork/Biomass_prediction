import csv
import pandas as pd
REFINERIES = 4
DEPOT_CAP = 20000
REFINERY_CAP = 100000
biomass_forecast_2018 = pd.read_csv('forecast2.csv').set_index('Index')['2018'].to_dict()
biomass_forecast_2019 = pd.read_csv('forecast2.csv').set_index('Index')['2019'].to_dict()
distance_matrix = pd.read_csv("Distance_Matrix.csv", index_col=0).values

def assign_biomass_to_depot(biomass_data, depots, distance_matrix):
    heap = []
    for loc in biomass_data:
        for depot_id, depot_index in enumerate(depots):
            distance = distance_matrix[loc, depot_index]
            heap.append((distance, loc, depot_id,depots[depot_id]))
    heap = sorted(heap)
    
    assignment = [None]*len(biomass_data)
    depot_load = [0]*len(depots)
    biomass_processed = 0
    for i in heap:
        distance,loc,depot_id, depot = i[0],i[1],i[2],i[3]
        if assignment[loc] is None:
            depot_load[depot_id]+=biomass_data[loc]
            if depot_load[depot_id]< DEPOT_CAP:
                assignment[loc] = [depot,biomass_data[loc]]
                biomass_processed+=biomass_data[loc]
            else:
                depot_load[depot_id]-=biomass_data[loc]          
    return assignment, depot_load

def assign_refinery_to_depot(biomass_load, refineries, distance_matrix):
    heap = []
    # print(f"biomass_load: {biomass_load}, refineries: {refineries}")
    for depot_loc in range(len(biomass_load)):
        for refinery_id, refinery_index in enumerate(refineries):
            distance = distance_matrix[depot_loc, refinery_index]
            heap.append((distance, depot_loc, refinery_id, refineries[refinery_id]))
    heap = sorted(heap)

    assignment = [None]*len(biomass_load)
    refinery_load = [0]*len(refineries)
     
    for i in heap:
        distance,depot_loc,refinery_id, refinery = i[0],i[1],i[2],i[3]
        if assignment[depot_loc]==None:
            refinery_load[refinery_id]+=biomass_load[depot_loc]
            if refinery_load[refinery_id]>= REFINERY_CAP:
                refinery_load[refinery_id]-=biomass_load[depot_loc]
                continue
            else:
                assignment[depot_loc] = [refinery,biomass_load[depot_loc]]
    return assignment

def write_year_output(biomass_forecast,year,refinery_indices,depot_indices):
    print(f"writing for year {year} started")
    with open('solution.csv','a',newline='') as output:
        csvwriter = csv.writer(output)
        for i in range(len(biomass_forecast)):
            datatype = 'biomass_forecast'
            source_index = i
            destination = ''
            value = biomass_forecast[i]
            csvwriter.writerow([year,datatype,source_index,destination,value])
        #adding biomass destinaiton value pairs
        assignments_of_depots,depot_load = assign_biomass_to_depot(biomass_forecast,depot_indices,distance_matrix)
 
        for i in range(len(assignments_of_depots)):
            datatype = 'biomass_demand_supply'
            source_index = i
            if assignments_of_depots[i] is None:
                continue
            else:
                destination = assignments_of_depots[i][0]
            value = assignments_of_depots[i][1]
            csvwriter.writerow([year,datatype,source_index,destination,value])
        #adding refinery depts value pairs
        assignments_of_refineries = assign_refinery_to_depot(depot_load,refinery_indices,distance_matrix)
        for i in range(len(assignments_of_refineries)):
            datatype = 'pellet_demand_supply'
            source_index = depot_indices[i]
            destination = assignments_of_refineries[i][0]
            value = assignments_of_refineries[i][1]
            csvwriter.writerow([year,datatype,source_index,destination,value])

########################################################################################################
def csv_output(max_solution):
    print('writing initiated')
    refinery_indices = max_solution[:REFINERIES]
    depot_indices = max_solution[REFINERIES:]
    with open("solution.csv", 'w', newline='') as output:
        csvwriter = csv.writer(output)
        #adding header:
        csvwriter.writerow(['year','data_type','source_index','destination_index', 'value'])
        print("adding depot indices")
        #adding depot indices:
        for i in range(len(depot_indices)):
            year = '20182019'
            datatype = "depot_location"
            source_index = depot_indices[i]
            destination = ''
            value = ''
        
            csvwriter.writerow([year, datatype,source_index,destination,value])
        print("adding refinery indices")
        #adding refineries indices:
        for i in range(len(refinery_indices)):
            year = '20182019'
            datatype = "refinery_location"
            source_index = refinery_indices[i]
            destination = ''
            value = ''
            csvwriter.writerow([year, datatype,source_index,destination,value])
    print("writing for year 2018")
    write_year_output(biomass_forecast_2018,'2018',refinery_indices,depot_indices)
    write_year_output(biomass_forecast_2019,'2019',refinery_indices,depot_indices)
        

soln = [2405,  127, 1459,  963, 2125,   21, 1161, 2272, 1798,  247, 1419, 1550, 1866,  895,
 2082, 1390, 2249,  552, 1076, 2395, 2348,  151,  421 , 490]

csv_output(soln)