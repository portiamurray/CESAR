def ProcessCoordinates(points,orig_id):
    import pandas as pd
    import numpy as np
    # Step 1 - Total Number of Building at Site
    #Assigning building numbers to all the buildings at Site
    n = len(points) # number of vertices (building corners)
    org_fid = points.loc[:, 'TARGET_FID'] # original fid ofArcGIS Building Shapes(all buildings for each vertex)
    bldng_nr = np.zeros(n) # building numberof each vertex(1...n_buildings at site)
    bldng_nr[0] = 1
    x_b = np.zeros(n)
    x_b[0] = 1
    for i in range(1,n):
        if org_fid[i] == org_fid[i - 1]: # if the original id of the previous vertex is the same
            bldng_nr[i] = bldng_nr[i - 1] # the building number will also be the same
        else:
            bldng_nr[i] = bldng_nr[i - 1] + 1 # else the building number will be increased by 1
        x_b[i] = bldng_nr[i] - bldng_nr[i - 1]
    # Finding the total number of buildings at site
    b_index = [i for i, x in enumerate(x_b) if x == 1] # find non - zero values --> vector with all the building numbers just once
    n_building = len(b_index) # total number of buildings at site
    #Assigning the building number to the buildings that will be simulated
    n_simbuildings = len(orig_id) # number of simulated buildings
    resid_id = np.zeros(n_simbuildings)
    for i in range(0,n):
        for j in range(0,n_simbuildings):
            if org_fid[i] == orig_id[j]:
                resid_id[j] = bldng_nr[i]
    # Step 2 - Assign points belonging to the same building points: columns including the information of 1(original% fid), 2(x), 3(y), 4(height)
    building = {}

    for x_building in range(0, n_building):
        if x_building < n_building - 1:
            building[x_building] = points.loc[b_index[x_building]:b_index[x_building + 1] - 1, :].reset_index()
        else:
            building[x_building] = points.loc[b_index[x_building]:n, :].reset_index()
    return [building, n_building,resid_id]

def BuildingsCenter(building,n_building):
    # Step 1.2: dataprocessing (note that: for anybuilding x_building, for each simulation job for x_building(center building), set the origin as v1(x_building) always, the
    # neighbour buildings working as other shading buildings are with the same origin.

    building_center = {} #cell(n_building, 1);

    for x_center in range(0,n_building):
        n_vertex = len(building[x_center])
        v_center = building[x_center].loc[0:n_vertex - 1,:] # footprint vertex of a single building matrix exclude last vertex
        # set the origin of the coordinate
        v0 = [v_center.loc[0, 'POINT_X'], v_center.loc[0, 'POINT_Y'], 0]  # set v1 as the origin(0, 0)
        building_center[x_center]=v_center.loc[:, ['POINT_X', 'POINT_Y', 'HEIGHT']] - 1 * v0
    return [building_center]

def BuildingsNeigh(building, n_building, r):
    import math
    # Step 1.2: dataprocessing
    # define the neighbour buildings to building i
    #calculate the distance between each building by the radius of the neighbourhood

    building_neigh = {}  # corresponding neighbour building vertex set from the origin
    building_neighnum = {}  # corresponding building number

    for x_center in range(0, n_building):

        n_vertex = len(building[x_center])
        # set the origin of the coordinate
        v_center = building[x_center].loc[0:n_vertex - 1, :]
        v0 = [v_center.loc[0, 'POINT_X'], v_center.loc[0, 'POINT_Y'], 0]  # set v1 as the origin(0, 0)
        count = 0  # counting the number of buildings in each neighbourhood for building i
        v_center = building[x_center].loc[0:n_vertex - 1,
                   :]  # footprint vertex of a single building matrix exclude last vertex

        for x_neigh in range(0, n_building):
            distance = math.sqrt((building[x_neigh].loc[0, 'POINT_X'] - building[x_center].loc[0, 'POINT_X']) ** 2 + (
                        building[x_neigh].loc[0, 'POINT_Y'] - building[x_center].loc[
                    0, 'POINT_Y']) ** 2)  # distance of the first vertex of each building

            if distance <= r:
                count = count + 1;  # x_neigh recognized as a neighbourbuilding

                # Use the vertex1(building{x_center}) as origin of the other neighbouring buildings
                n_vertex = len(building[x_neigh])
                v_neigh = building[x_neigh].loc[0:n_vertex - 1,
                          ['POINT_X', 'POINT_Y', 'HEIGHT']] - 1 * v0  # exclude the last vertex which is the same as v1

                building_neigh[x_center, count] = v_neigh
                building_neighnum[
                    x_center, count] = x_neigh  # corresponding neighbour building number(id), consistentwith ORIG_FID
    return [building_neigh, building_neighnum]
