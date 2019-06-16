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
