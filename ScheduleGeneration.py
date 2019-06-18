def my_triang(x, p05, p95, c):
    F = [((p05 - x[0])**2)/(x[1]-x[0])/(c-x[0]) - 0.05,((x[1] - p95)**2)/(x[1]-x[0])/(x[1]-c) - 0.05]
    return F

def rle_cumsum_diff(vals,runlens):
    import numpy as np
    clens = np.cumsum(runlens)
    idx=np.zeros(int(clens[-1]))
    difference = np.diff(vals)
    inter = clens[0:len(clens) - 1]
    for i in range(0, len(difference)):
        idx[int(inter[i])] = difference[i]
    out = np.cumsum(idx)
    return out

def randpermbreak(N,BP):
    # only use valid break points
    import numpy as np
    bpfixed=False
    BP = BP[(BP <= N) & (BP > 0)]

    if len(BP)==0:
        R = np.argsort(np.random.rand[N]))# trivial, simply randperm
    else:
        # mark the sections: section one is 2, section two is 4, etc.
        R = np.zeros(N)
        R[BP[BP<N]+1] = 2 # sections are labeled 0, 2, 4, take care of BP = N
        R = np.cumsum(R)

        if bpfixed:
            #if break points are not to be randomly permuted, these will
            # be treated as separate sections with labels 1, 3, 5, ...
            R[BP] = R[BP] + 1
        # we add a random number between 0 and 1.
        R = R + np.random.rand(N)
        # Note that floor(R) returns the section number. If we sort these
        # random numbers, the sections will stay in place.
        R = np.argsort(R) # the trick used by randperm
    return R

def horizontal_variabililty(profile, breaks):
    # Function that implements the "horizontal variability" aspect in the
    # variable SIA 2024 profiles
    import numpy as np
    perturb = breaks
    if len(breaks) == 0:
        perturbed_profile = profile
    else:
        for i in range(0,365):
            perturbed_profile = profile
            perturb = np.concatenate((perturb, breaks + 24 * (i+1)))
        [leng,prof_size]=profile.shape

        for i in range(0,prof_size):
            if np.random.rand() <= 0.6: # Probability that a profile will be perturbed or not; set to 1 to perturb all profiles
                perturbation_values = randpermbreak(8760,perturb)
                perturbed_profile[:,i] = profile[perturbation_values,i]
            else:
                perturbed_profile[:,i] = profile[:,i]
    return perturbed_profile


def CESAR_function_Variability_case_multiroom_selection(prof_nr, value_nr, variable_schedules, schedulepath, bldg, project_directory):
    import numpy as np
    import pandas as pd
    from scipy.stats import uniform
    from scipy.optimize import fsolve
    import scipy as sp
    # Uncertainty - Yes or no?
    # == == == == == == == == == == == == =

    # rng(1) % Fix random generators to generate predictable sequence of numbers

    # Do you want the creation of uncertainty profiles? (Y = 1; N = 0)
    # ----------------------------------------------------------------
    uncertainty = 1

    # Background | Introduction
    # == == == == == == == == == == == ==

    # Building type
    # -------------
    # Building type
    # -------------

    # bldg = 'mfh'  # This is only a name (FIX LATER, NON-INTUITIVE)

    # Number of rooms
    # ---------------

    # Room types
    # ----------
    room = {}
    name, area, occ_breaks, appliance_breaks, setback, set_back_temp, night, night_DHW, night_light, mech_vent, pressurisation, row, infiltration_rate_nominal, ruhetage, monthly_variation_nominal, daily_occupancy_nominal, monthly_variation_variable, yearly_variation_nominal, daily_variation_variable, daily_variation_nominal, yearly_variation_variable, yearly_occupancy_variable, yearly_occupancy_nominal = "name", "area", "occ_breaks", "appliance_breaks", "setback", "set_back_temp", "night", "night_DHW", "night_light", "mech_vent", "pressurisation", "row", "infiltration_rate_nominal", "ruhetage", "monthly_variation_nominal", "daily_occupancy_nominal", "monthly_variation_variable", "yearly_variation_nominal", "daily_variation_variable", "daily_variation_nominal", "yearly_variation,variable", "yearly_occupancy_variable", "yearly_occupancy_nominal"
    area_per_person_nominal, area_per_person_min, area_per_person_max, area_per_person_variable, therm_h_nominal, therm_c_nominal, therm_h_variable, therm_c_variable, activity_nominal, activity_variable, therm_h_min, therm_h_max, therm_c_min, therm_c_max, yearly_thermostat_heating_nominal, yearly_thermostat_cooling_nominal, yearly_thermostat_heating_variable, yearly_thermostat_cooling_variable = "area_per_person_nominal", "area_per_person_min", "area_per_person_max", "area_per_person_variable", "therm_h_nominal", "therm_c_nominal", "therm_h_variable", "therm_c_variable", "activity_nominal", "activity_variable", "therm_h_min", "therm_h_max", "therm_c_min", "therm_c_max", "yearly_thermostat_heating_nominal", "yearly_thermostat_cooling_nominal", "yearly_thermostat_heating_variable", "yearly_thermostat_cooling_variable"
    light_density_nominal, light_density_variable, light_stp_nominal, light_stp_variable, ventilation_nominal, ventilation_variable, yearly_ventilation_nominal, ventilation_night_nominal_per_person, yearly_dhw_nominal, yearly_dhw_variable, yearly_appliances_nominal, yearly_appliances_variable, yearly_infiltration_variable, yearly_activity_nominal, yearly_activity_variable = "light_density_nominal", "light_density_variable", "light_stp_nominal", "light_stp_variable", "ventilation_nominal", "ventilation_variable", "yearly_ventilation_nominal", "ventilation_night_nominal_per_person", "yearly_dhw_nominal", "yearly_dhw_variable", "yearly_appliances_nominal", "yearly_appliances_variable", "yearly_infiltration_variable", "yearly_activity_nominal", "yearly_activity_variable"
    room[name] = {}
    room[area] = {}
    room[occ_breaks] = {}
    room[setback] = {}
    room[set_back_temp] = {}
    room[appliance_breaks] = {}
    room[mech_vent] = {}
    room[night] = {}
    room[night_DHW] = {}
    room[night_light] = {}
    room[pressurisation] = {}
    room[row] = {}
    room[infiltration_rate_nominal] = {}
    room[monthly_variation_nominal] = {}
    room[daily_occupancy_nominal] = {}
    room[monthly_variation_variable] = {}
    room[yearly_variation_nominal] = {}
    room[daily_variation_variable] = {}
    room[daily_variation_nominal] = {}
    room[yearly_variation_variable] = {}
    room[yearly_occupancy_variable] = {}
    room[yearly_occupancy_nominal] = {}
    room[ruhetage] = {}
    room[area_per_person_nominal] = {}
    room[area_per_person_min] = {}
    room[area_per_person_max] = {}
    room[area_per_person_variable] = {}
    room[therm_h_nominal] = {}
    room[therm_c_nominal] = {}
    room[therm_h_variable] = {}
    room[therm_c_variable] = {}
    room[activity_nominal] = {}
    room[activity_variable] = {}
    room[therm_h_min] = {}
    room[therm_h_max] = {}
    room[therm_c_min] = {}
    room[therm_c_max] = {}
    room[yearly_thermostat_heating_nominal] = {}
    room[yearly_thermostat_cooling_nominal] = {}
    room[yearly_thermostat_heating_variable] = {}
    room[yearly_thermostat_cooling_variable] = {}
    room[light_density_nominal] = {}
    room[light_density_variable] = {}
    room[light_stp_nominal] = {}
    room[light_stp_variable] = {}
    room[ventilation_nominal] = {}
    room[ventilation_variable] = {}
    room[yearly_ventilation_nominal] = {}
    room[ventilation_night_nominal_per_person] = {}
    room[yearly_infiltration_variable] = {}
    room[yearly_dhw_variable] = {}
    room[yearly_appliances_nominal] = {}
    room[yearly_appliances_variable] = {}
    room[yearly_activity_nominal] = {}
    room[yearly_activity_variable] = {}
    if bldg == 'mfh':
        room_num = 2
        # MFH composition according to SIA 2024 v.2016
        room[name][0] = 'MFH'
        room[name][1] = 'Staircase'
    elif bldg == 'efh':
        # EFH composition according to SIA2024 v.2016
        room_num = 1
        room[name][0] = 'EFH'
    elif bldg == 'office':
        # Office composition according to SIA 2024 v .2016
        room_num = 10
        room[name][0] = 'Single_office'
        room[name][1] = 'Office'
        room[name][2] = 'Meeting_room'
        room[name][3] = 'Lobby'
        room[name][4] = 'Corridor'
        room[name][5] = 'Staircase'
        room[name][6] = 'Storage_space'
        room[name][7] = 'Kitchen'
        room[name][8] = 'WC'
        room[name][9] = 'Server room'
    elif bldg == 'school':
        # School composition according to SIA 2024 v.2016
        room_num = 9
        room[name][0] = 'Classroom'
        room[name][1] = 'Staff room, Common room'
        room[name][2] = 'Library'
        room[name][3] = 'Lecture hall'
        room[name][4] = 'School physics, chemistry room'
        room[name][5] = 'Corridor'
        room[name][6] = 'Staircase'
        room[name][7] = 'Storage_space'
        room[name][8] = 'WC'
    elif bldg == 'shop':
        # Shop composition according to SIA2024 v.2016
        room_num = 8
        room[name][0] = 'Single_office'
        room[name][1] = 'Food_store'
        room[name][2] = 'Shopping mall'
        room[name][3] = 'Furniture store'
        room[name][4] = 'Corridor'
        room[name][5] = 'Staircase'
        room[name][6] = 'Storage_space'
        room[name][7] = 'Locker room, shower'
    elif bldg == 'restaurant':
        # Restaurant composition accordingto SIA 2024 v.2016
        room_num = 6
        room[name][0] = 'Single_office'
        room[name][1] = 'Restaurant'
        room[name][2] = 'Restaurant_kitchen'
        room[name][3] = 'Corridor'
        room[name][4] = 'Storage_space'
        room[name][5] = 'Locker room, shower'
    elif bldg == 'hospital':
        # Hospital composition according to SIA2024 v.2016
        room_num = 9
        room[name][0] = 'Single_office'
        room[name][1] = 'Hospital ward'
        room[name][2] = 'Hospital unit room'
        room[name][3] = 'Medical treatment room'
        room[name][4] = 'Corridor'
        room[name][5] = 'Corridor_24h'
        room[name][6] = 'Staircase'
        room[name][7] = 'Storage_space'
        room[name][8] = 'WC'
    # Breakdown of total area( in % or m2)
    # ------------------------------------
    if bldg == 'mfh':
        room[area][0] = 90
        room[area][1] = 10
    elif bldg == 'efh':
        room[area][0] = 100
    elif bldg == 'office':
        room[area][0] = 10
        room[area][1] = 50
        room[area][2] = 10
        room[area][3] = 5
        room[area][4] = 10
        room[area][5] = 5
        room[area][6] = 5
        room[area][7] = 2
        room[area][8] = 2
        room[area][9] = 1
    elif bldg == 'school':
        room[area][0] = 50
        room[area][1] = 5
        room[area][2] = 5
        room[area][3] = 5
        room[area][4] = 5
        room[area][5] = 15
        room[area][6] = 5
        room[area][7] = 5
        room[area][8] = 5
    elif bldg == 'shop':
        room[area][0] = 5
        room[area][1] = 20
        room[area][2] = 20
        room[area][3] = 20
        room[area][4] = 10
        room[area][5] = 5
        room[area][6] = 15
        room[area][7] = 5
    elif bldg == 'restaurant':
        room[area][0] = 5
        room[area][1] = 60
        room[area][2] = 10
        room[area][3] = 10
        room[area][4] = 10
        room[area][5] = 5
    elif bldg == 'hospital':
        room[area][0] = 5
        room[area][1] = 50
        room[area][2] = 5
        room[area][3] = 10
        room[area][4] = 5
        room[area][5] = 5
        room[area][6] = 5
        room[area][7] = 10
        room[area][8] = 5
    # Number of profiles generated
    # ----------------------------
    prof_number = prof_nr

    # Number of scalar values generated
    # ---------------------------------
    value_number = prof_number

    # Vertical variability value
    # --------------------------
    vert_var = 0.15

    # Horizontal variability breaks
    # -----------------------------
    room[occ_breaks][0] = [6, 8, 12, 15, 17, 21, 24]
    room[occ_breaks][1] = [6, 19, 24]
    room[occ_breaks][2] = []
    room[occ_breaks][3] = []
    room[occ_breaks][4] = []
    room[occ_breaks][5] = []
    room[occ_breaks][6] = []
    room[occ_breaks][7] = []
    room[occ_breaks][8] = []
    room[occ_breaks][9] = []

    room[appliance_breaks][0] = [6, 8, 12, 15, 17, 21, 24]
    room[appliance_breaks][1] = [6, 19, 24]
    room[appliance_breaks][2] = []
    room[appliance_breaks][3] = []
    room[appliance_breaks][4] = []
    room[appliance_breaks][5] = []
    room[appliance_breaks][6] = []
    room[appliance_breaks][7] = []
    room[appliance_breaks][8] = []
    room[appliance_breaks][9] = []
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Night | Unoccupied setback for thermostats
    # == == == == == == == == == == == == == == == == == == == ==
    for rm in range(0, room_num):
        room[setback][rm] = 1  # (1 = YES, 0 = NO)
        room[set_back_temp][rm] = 3  # Number of degrees celsiusfor setback

        # Do people sleep in the room?
        # ----------------------------
        # This implies that during occupancy setback temperatures could be valid  and lights could be off
        # Examples: Residential building | Hotel room | Hospital ward

        room[night][rm] = 1  # Use with thermostats
        room[night_DHW][rm] = 1  # Use with DHW
        room[night_light][rm] = 1  # Use with lighting
        # Ventilation and infiltration data
        # == == == == == == == == == == == == == == == == == == == =

        # Is the building mechanically ventilated or not? (1 for YES, 0 for NO)
        # ---------------------------------------------------------------------
        room[mech_vent][rm] = 0

        room[pressurisation][rm] = 0

        # What is the nominal infiltration value in ACH?
        # ----------------------------------------------
        room[infiltration_rate_nominal][rm] = 0.3

    # Define nominal night time hours
    # -------------------------------
    sleep = 23
    wake = 7

    sleep_var = np.random.randint(sleep - 1, sleep + 1, size=(365, prof_number))
    wake_var = np.random.randint(wake - 1, wake + 1, size=(365, prof_number))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    # Do you want infiltration uncertainty?
    # -------------------------------------
    infilt_uncertainty = 1

    # Do you want ventilation uncertainty?
    # -------------------------------------
    vent_uncertainty = 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Load data and create calendar variables
    # == == == == == == == == == == == == == == == == == == == =

    # Load bldg list
    # --------------
    f_bldg = open(project_directory + '/01_Code/CESAR/bldg_types.txt', 'r')
    bldg_types = f_bldg.read().splitlines()
    f_bldg.close()

    # Find bldg row from d / b
    # ----------------------
    for rm in range(0, room_num):
        room[row][rm] = bldg_types.index(room[name][rm])

    # Load bldg data
    # --------------
    filename = r'/Users/portia_murray/Desktop/03_CESAR_Tool_the_15022018_PM/01_Code/CESAR/SIA_data_for_MATLAB.xlsx'
    sheet = 'Eingabedaten_edit'
    db2024 = pd.read_excel(filename, sheet, usecols='C:DL', skiprows=9)

    # Creationof days(Mondays, Tuesdays, etc.) for a full year
    # ----------------------------------------------------------
    week = range(0,7)
    #'; % Day number for a week (1,2,3,...,7)
    day_year = np.append(np.kron(np.ones((52)), range(0,7)),1) # Weekday number for a full year
    days_per_month = [31,28,31,30,31,30,31,31,30,31.30,31] # Number of days per month
    runlens = np.kron(np.ones(365), 24)

    day_for_each_hour_of_year =rle_cumsum_diff(day_year,runlens)# Vectorwith the weekday (0-6) number for each hour of the year

    # Rest days
    # ---------
    for rm in range(0,room_num):
        room[ruhetage][rm] = db2024.loc[room[row][rm], 93]


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Occupancy
    # == == == == ==

    for rm in range(0, room_num):

        # Create nominal profile
        # == == == == == == == == == == ==
        room[monthly_variation_nominal][rm] = db2024.loc[room[row][rm], range(81, 93)].as_matrix()
        room[daily_occupancy_nominal][rm] = db2024.loc[room[row][rm], range(33, 57)].as_matrix()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Add vertical monthly variability
        # == == == == == == == == == == == == == == == ==

        # Create variable values for each month
        # -------------------------------------
        X0 = np.random.rand(12, prof_number)

        # Remap variable values between the limits dictated by the vertical variation
        # ---------------------------------------------------------------------------
        X0 = (vert_var * X0 + (1 - X0) * (-vert_var))

        # Create variations for the monthly profile equal to "prof_number"
        # ----------------------------------------------------------------
        room[monthly_variation_variable][rm] = np.zeros((12, prof_number))

        for i in range(0, prof_number):
            room[monthly_variation_variable][rm][:, i] = room[monthly_variation_nominal][rm] * (1 + X0[:, i])

        # Correct values that are higher than 1 \
        # ------------------------------------- \
        room[monthly_variation_variable][rm][room[monthly_variation_variable][rm] > 1] = 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Expand monthly variabilities to the whole year
        # == == == == == == == == == == == == == == == == == == == == == == ==

        # Repeat the nominal monthly profile values for each day and each hour of the year
        # --------------------------------------------------------------------------------
        room[daily_variation_nominal][rm] = rle_cumsum_diff(room[monthly_variation_nominal][rm],
                                                            days_per_month)  # repeat each monthly variation value as many times as the days of the month
        room[yearly_variation_nominal][rm] = rle_cumsum_diff(room[monthly_variation_nominal][rm],
                                                             24 * days_per_month)  # repeat each monthly variation value for each hour based on the month it belongs

        # Repeat the variable monthly profiles values for each day and each hour of the year
        # ----------------------------------------------------------------------------------
        room[daily_variation_variable][rm] = np.zeros((365, prof_number))
        room[yearly_variation_variable][rm] = np.zeros((8760, prof_number))

        for i in range(0, prof_number):
            room[daily_variation_variable][rm][:, i] = rle_cumsum_diff(room[monthly_variation_variable][rm][:, i],
                                                                       days_per_month)
            room[yearly_variation_variable][rm][:, i] = rle_cumsum_diff(room[monthly_variation_variable][rm][:, i],
                                                                        24 * days_per_month)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Create occupancy profile
        # == == == == == == == == == == == ==

        # Initialization of occupancy profile \
        # ----------------------------------- \
        room[yearly_occupancy_nominal][rm] = np.zeros(8760)
        room[yearly_occupancy_variable][rm] = np.zeros((8760, prof_number))

        # Creation of occupancy profile according to monthly nominal and variable schedules
        # ----------------------------------------------------------------------------------
        for i in range(0, 365):
            room[yearly_occupancy_nominal][rm][range(i * 24, (i + 1) * 24)] = room[daily_occupancy_nominal][rm] * \
                                                                              room[daily_variation_nominal][rm][i]
        for j in range(0, prof_number):
            room[yearly_occupancy_variable][rm][range(i * 24, (i + 1) * 24), j] = room[daily_occupancy_nominal][rm] * \
                                                                                  room[daily_variation_variable][rm][
                                                                                      i, j]
        # Add vertical variability to the occupancy profiles
        # --------------------------------------------------

        # Create random values in the range[-vert_var, vert_var] for each hour of each variable hourly occupancy profile
        # ------------------------------------------------------------------------
        X0 = -vert_var + (vert_var - (-vert_var)) * np.random.rand(8760, prof_number)

        # Apply vertical variability to hourly profiles
        # -----------------------------------------------
        room[yearly_occupancy_variable][rm] = room[yearly_occupancy_variable][rm] * (1 + X0)

        # Correct for weekend days
        # ------------------------
        if room[ruhetage][rm] == 1:
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 6] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 6, :] = 0
        elif room[ruhetage][rm] == 2:
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 5] = 0
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 6] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 5, :] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 6, :] = 0

        room[yearly_occupancy_variable][rm][room[yearly_occupancy_variable][rm] > 1] = 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Add horizontal variability to the occupancy profiles
        # == == == == == == == == == == == == == == == == == == == == == == == == ==
        room[yearly_occupancy_variable][rm] = horizontal_variabililty(room[yearly_occupancy_variable][rm],
                                                                      room[occ_breaks][rm])

        # Constant nighttime occupancy if place where people sleep
        # (Correction required only for the variable case)
        # --------------------------------------------------------
        if room[night][rm] == 1:
            for j in range(0, prof_number):
                for i in range(0, 365):
                    if i == 0:
                        room[yearly_occupancy_variable][rm][range(i, wake_var[i, j]), j] = room[yearly_variation_variable][rm][range(i, wake_var[i, j]), j]
                        room[yearly_occupancy_variable][rm][range(24 * i - sleep_var[i, j], 24 * i + wake_var[i, j]), j] = room[yearly_variation_variable][rm][range(24 * i - sleep_var[i, j], 24 * i + wake_var[i, j]), j]
                    elif i == 364:
                        room[yearly_occupancy_variable][rm][range(24 * i - sleep_var[i, j], len(room[yearly_occupancy_variable][rm])), j] = room[yearly_variation_variable][rm][range(24 * i - sleep_var[i, j], len(room[yearly_variation_variable][rm])), j]
                    else:
                        room[yearly_occupancy_variable][rm][range(24 * i - sleep_var[i, j], 24 * i + wake_var[i, j]), j] = room[yearly_variation_variable][rm][range(24 * i - sleep_var[i, j], 24 * i + wake_var[i, j]), j]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Calculate presence and activity values for occupancy
        # == == == == == == == == == == == == == == == == == == == == == == == == == ==

        # Number of people per unit area (nominal, minimum, maximum)
        # ----------------------------------------------------------
        room[area_per_person_nominal][rm] = db2024.loc[room[row][rm], 3]  # m2 / Person
        room[area_per_person_min][rm] = db2024.loc[room[row][rm], 106]  # m2 / Person
        room[area_per_person_max][rm] = db2024.loc[room[row][rm], 105]  # m2 / Person

        x0 = [room[area_per_person_min][rm] - 1, room[area_per_person_max][rm] + 1]
        # my_triang(x, p05, p95, c)
        x = fsolve(my_triang, x0, args=(room[area_per_person_min][rm], room[area_per_person_max][rm], room[area_per_person_nominal][rm]))

        # Sample from triangular distribution
        # -----------------------------------
        if room[area_per_person_nominal][rm] == 0:
            room[area_per_person_variable][rm] = np.zeros(value_number)
        else:
            room[area_per_person_variable][rm] = np.random.triangular(x[0], room[area_per_person_nominal][rm], x[1],
                                                                      value_number)
            room[area_per_person_variable][rm] = np.round(room[area_per_person_variable][rm],
                                                          1)  # round to 1 decimal digit
        # Occupant activities
        # -----------------------------
        # Calculations are directly made in W / P terms
        # -----------------------------
        room[activity_nominal][rm] = db2024.loc[room[row][rm], 5] * room[area_per_person_nominal][rm]  # W / P
        # If we want uncertain activity, then uncomment the following:
        # room[activity_variable][rm] = np.random.normal(activity_nominal, activity_nominal / 20,value_number)
        # If activity uncertainty is not considered, then:
        room[activity_variable][rm] = np.matlib.repmat(room[activity_nominal][rm], value_number, 1)

        # Create activity profile \
        # ----------------------- \
        room[yearly_activity_nominal][rm] = np.matlib.repmat(room[activity_nominal][rm], 8760, 1)
        room[yearly_activity_variable][rm] = np.matlib.repmat(room[activity_variable][rm], 8760, 1)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    Rarea_per_person_nominal = 0
    Ryearly_occupancy_nominal = 0
    Ryearly_activity_nominal = 0

    Rarea_per_person_variable = np.zeros(value_number)
    room[area][sum] = 0
    for rm in range(0, room_num):
        room[area][sum] = room[area][sum] + room[area][rm]
    # Calculation
    # -----------
    for rm in range(0, room_num):
        # Nominal values
        # --------------
        if room[area_per_person_nominal][rm] == 0:
            Rarea_per_person_nominal = Rarea_per_person_nominal
        else:
            Rarea_per_person_nominal = Rarea_per_person_nominal + (
                        room[area][rm] * 1 / room[area_per_person_nominal][rm]) / room[area][sum]
        # Variable values
        # ---------------
        if room[area_per_person_nominal][rm] == 0:
            Rarea_per_person_variable = Rarea_per_person_variable
        else:
            Rarea_per_person_variable = Rarea_per_person_variable + (
                        room[area][rm] * 1 / room[area_per_person_variable][rm]) / room[area][sum]

    if Rarea_per_person_nominal != 0:
        Rarea_per_person_nominal = 1 / Rarea_per_person_nominal
    if Rarea_per_person_variable.sum() != 0:
        Rarea_per_person_variable = 1 / Rarea_per_person_variable
    else:
        Rarea_per_person_variable = np.zeros(value_number)

    for rm in range(0, room_num):
        # Nominal values
        # --------------
        if room[area_per_person_nominal][rm] == 0:
            Ryearly_occupancy_nominal = Ryearly_occupancy_nominal
            Ryearly_activity_nominal = Ryearly_activity_nominal
        else:
            Ryearly_occupancy_nominal = Ryearly_occupancy_nominal + (room[area][rm] / room[area][sum]) * \
                                        room[yearly_occupancy_nominal][rm] * (1 / room[area_per_person_nominal][rm]) / (
                                                    1 / Rarea_per_person_nominal)
            Ryearly_activity_nominal = Ryearly_activity_nominal + room[area][rm] * room[activity_nominal][rm] * (
                        1 / room[area_per_person_nominal][rm])

    if Rarea_per_person_nominal != 0:
        Ryearly_activity_nominal = Ryearly_activity_nominal / (1 / Rarea_per_person_nominal) / room[area][sum]
        Ryearly_activity_nominal = np.matlib.repmat(Ryearly_activity_nominal, 8760,
                                                    1)  # Creation of activity profile end
    Ryearly_occupancy_variable = np.zeros((8760, prof_number))
    Ryearly_activity_variable = np.zeros(prof_number)
    for j in range(0, prof_number):
        Ryearly_activity_variable[j] = 0
        for rm in range(0, room_num):
            # Variable values
            # ---------------
            if room[area_per_person_nominal][rm] == 0:
                Ryearly_occupancy_variable[:, j] = Ryearly_occupancy_variable[:, j]
                Ryearly_activity_variable[j] = Ryearly_activity_variable[j]
            else:
                Ryearly_occupancy_variable[:, j] = Ryearly_occupancy_variable[:, j] + (
                            room[area][rm] / room[area][sum]) * room[yearly_occupancy_variable][rm][:, j] * (
                                                               1 / room[area_per_person_variable][rm][j]) / (
                                                               1 / Rarea_per_person_variable[j])
                Ryearly_activity_variable[j] = Ryearly_activity_variable[j] + room[area][rm] * \
                                               room[activity_variable][rm][j] * (
                                                           1 / room[area_per_person_variable][rm][j])  # check!!!!!

    Ryearly_activity_variable = Ryearly_activity_variable / (1 / Rarea_per_person_variable) / room[area][sum]
    Ryearly_activity_variable = np.tile(Ryearly_activity_variable, (8760, 1))

    # Creation of activity profile

    # Thermostats
    # == == == == == ==

    for rm in range(0,room_num):

                     # Thermostat values
        # == == == == == == == == =

        # Heating setpoints(nominal, minimum, maximum) \
        # --------------------------------------------- \
        room[therm_h_nominal][rm] = db2024.loc[room[row][rm], 2]
        room[therm_h_min][rm] = db2024.loc[room[row][rm], 107]
        room[therm_h_max][rm] = db2024.loc[room[row][rm], 108]

        # Cooling setpoints(nominal, minimum, maximum) \
        # --------------------------------------------- \
        room[therm_c_nominal][rm] = db2024.loc[room[row][rm], 1]
        room[therm_c_min][rm] = db2024.loc[room[row][rm], 109]
        room[therm_c_max][rm] = db2024.loc[room[row][rm], 110]

        # SAMPLE FROM NORMAL DISTRIBUTIONS
        # == == == == == == == == == == == == == == == ==
        room[therm_h_variable][rm] = normrnd(room[therm_h_nominal][rm], 1, [prof_number, 1])
        room[therm_c_variable][rm] = normrnd(room[therm_c_nominal][rm], 1, [prof_number, 1])

        # Prevent heating setpoint being higher than cooling setpoint \
        # ----------------------------------------------------------- \
            non_compliant_points = find(room[therm_h_variable][rm] > room[therm_c_variable][rm])
        if not non_compliant_points:
        for nc in range(0,max(len(non_compliant_points))
        while room[therm_h_variable][rm][non_compliant_points[nc]] > room[therm_c_variable][rm][non_compliant_points[nc]]
            room[therm_h_variable][rm][non_compliant_points[nc]] = normrnd(room[therm_h_nominal][rm], 1, [1, 1])
            room[therm_c_variable][rm](non_compliant_points[nc]) = normrnd(room[therm_c_nominal][rm], 1, [1, 1])

        # SAMPLE FROM TRIANGULAR DISTRIBUTIONS
        # == == == == == == == == == == == == == == == == == ==
        # Create triangular distribution
        # ------------------------------
        x0 = [room[therm_h_min][rm] - 1, room[therm_h_max][rm] + 1]
        [x, ~] = fsolve( @ (x)my_triang(x, room[therm_h_min][rm], room[therm_h_max][rm], room[therm_h_nominal][rm]), x0) # Callsolver
        # Sample from triangular distribution
        # -----------------------------------
         pd = makedist('Triangular', 'a', x(1), 'b', room[rm].therm_h_nominal, 'c', x(2))
        # room[rm].therm_h_variable = random(pdd, value_number, 1)
        #
        # Create triangular distribution
        # ------------------------------
        # x0 = [room[rm].therm_c_min - 1, room[rm].therm_c_max + 1];
        # [x, ~] = fsolve( @ (x)
        my_triang(x, room[therm_c_min][rm], room[therm_c_max][rm], room[therm_c_nominal][rm]), x0)# Call solver
        #
        # Sample from triangular distribution
        # -----------------------------------
        # pd1 = makedist('Triangular', 'a', x(1), 'b', room[rm].therm_c_nominal, 'c', x(2));
        # room[rm].therm_c_variable = random(pd1, value_number, 1);

        # Prevent heating setpoint being higher than cooling setpoint
        # -----------------------------------------------------------
        # non_compliant_points = find(room[rm].therm_h_variable > room[rm].therm_c_variable);
        # if isempty(non_compliant_points) == 0
            # for nc = 1:1:max(size(non_compliant_points))
        # while room[rm].therm_h_variable(non_compliant_points(nc)) > room[rm].therm_c_variable(non_compliant_points(nc))
            # room[rm].therm_h_variable(non_compliant_points(nc)) = random(pdd, 1);
        # room[rm].therm_c_variable(non_compliant_points(nc)) = random(pd1d, 1);

        room[therm_h_variable][rm] = round(room[therm_h_variable][rm], 1)# round to 1 decimal digit
        room[therm_c_variable][rm] = round(room[therm_c_variable][rm], 1) # round to 1 decimal digit

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Create thermostat profiles
        # == == == == == == == == == == == == ==
        room[yearly_thermostat_heating_nominal][rm] = repmat(room[therm_h_nominal][rm], 8760, 1)
        room[rm].yearly_thermostat_cooling_nominal = repmat(room[rm].therm_c_nominal, 8760, 1)

        room[rm].yearly_thermostat_heating_variable = repmat(room[rm].therm_h_variable', 8760, 1)
        room[rm].yearly_thermostat_cooling_variable = repmat(room[rm].therm_c_variable', 8760, 1)

        # Unoccupied setback
        if room[rm].setback == 1
            room[yearly_thermostat_heating_nominal][rm](room[yearly_occupancy_nominal][rm] == 0) = room[yearly_thermostat_heating_nominal][rm](room[yearly_occupancy_nominal][rm] == 0) - room[set_back_temp][rm]
            room[yearly_thermostat_cooling_nominal][rm](room[yearly_occupancy_nominal][rm] == 0) = room[yearly_thermostat_cooling_nominal][rm](room[yearly_occupancy_nominal][rm] == 0) + room[set_back_temp][rm]

            room[yearly_thermostat_heating_variable][rm](room[yearly_occupancy_variable][rm] == 0) = room[yearly_thermostat_heating_variable][rm](room[yearly_occupancy_variable][rm] == 0) - room[set_back_temp][rm]
            room[yearly_thermostat_cooling_variable][rm](room[yearly_occupancy_variable][rm] == 0) = room[yearly_thermostat_cooling_variable][rm](room[yearly_occupancy_variable][rm] == 0) + room[set_back_temp][rm]

        # Night setback for nominal profile
        if room[night][rm] == 1:
            for i in range(0:365):
                if i == 1:
                   # Heating
                    room[yearly_thermostat_heating_nominal][rm](i:(wake - 1)) = room[yearly_thermostat_heating_nominal][rm](i:(wake - 1)) - room[set_back_temp][rm]
                    room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) - room[set_back_temp][rm]
                # Cooling
                    room[yearly_thermostat_cooling_nominal][rm](i:(wake - 1)) = room[yearly_thermostat_cooling_nominal][rm](i:(wake - 1)) + room[set_back_temp][rm]
                    room[yearly_thermostat_cooling_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room[rm].yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) + room[set_back_temp][rm]
                elif i == 365:
                # Heating
                    room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):end) = room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):end) - room[set_back_temp][rm]
                # Cooling
                    room[yearly_thermostat_cooling_nominal][rm]((24 * i - (24 - sleep)):end) = room[yearly_thermostat_cooling_nominal][rm]((24 * i - (24 - sleep)):end) + room[set_back_temp][rm]
                else:
                # Heating
                    room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room[yearly_thermostat_heating_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) - room[set_back_temp][rm]
                # Cooling
                    room[yearly_thermostat_cooling_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room[yearly_thermostat_cooling_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) + room[set_back_temp][rm]
        end
        end
        end

        # Night setback for variable profile
        if room[night]rm] == 1:
        for j in range(0,prof_number):
        for i in range(0:365):
        if i == 1:
           # Heating
        room[yearly_thermostat_heating_variable][rm](i:(wake_var(i, j) - 1), j) = room[rm][yearly_thermostat_heating_variable](i:(wake_var(i, j) - 1), j) - room[set_back_temp][rm]
        room[yearly_thermostat_heating_variable][rm].((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room[yearly_thermostat_heating_variable][rm](24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) - room[set_back_temp][rm]
        # Cooling
        room[yearly_thermostat_cooling_variable][rm](i:(wake_var(i, j) - 1), j) = room[rm].yearly_thermostat_cooling_variable(i:(wake_var(i, j) - 1), j) + room[rm].set_back_temp;
        room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) + room[set_back_temp][rm]
        elseif
        i == 365
        # Heating
        room[yearly_thermostat_heating_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) = room[yearly_thermostat_heating_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) - room[rm].set_back_temp
        # Cooling
        room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) = room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) + room[rm].set_back_temp
        else
        # Heating
        room[yearly_thermostat_heating_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room[yearly_thermostat_heating_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) - room[set_back_temp][rm]
        # Cooling][rm]
        room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room[yearly_thermostat_cooling_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) + room[set_back_temp][rm]
        end
        end
        end
        end

        end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    Rtherm_h_nominal = 0
    Rtherm_c_nominal = 0
    Ryearly_thermostat_heating_nominal = 0
    Ryearly_thermostat_cooling_nominal = 0

    Rtherm_h_variable = 0
    Rtherm_c_variable = 0
    Ryearly_thermostat_heating_variable = 0
    Ryearly_thermostat_cooling_variable = 0

    # Calculation
    # -----------
    for rm in range(0,room_num):
        # Nominal values \
        # -------------- \
        Rtherm_h_nominal = therm_h_nominal + (room[area][rm] * room[therm_h_nominal][rm]) / sum(cat(1, room[area]))
        Rtherm_c_nominal = therm_c_nominal + (room[area][rm] * room[therm_c_nominal][rm]) / sum(cat(1, room[area]))
        Ryearly_thermostat_heating_nominal = yearly_thermostat_heating_nominal + (room[area][rm] * room[yearly_thermostat_heating_nominal][rm]) / sum(cat(1, room[area]))
        Ryearly_thermostat_cooling_nominal = yearly_thermostat_cooling_nominal + (room[area][rm] * room[yearly_thermostat_cooling_nominal][rm]) / sum(cat(1, room[area]))
        # Variable values \
    # --------------- \
        Rtherm_h_variable = therm_h_variable + (room[area][rm] * room[therm_h_variable][rm]) / sum(cat(1, room[area]))
        Rtherm_c_variable = therm_c_variable + (room[area][rm] * room[therm_c_variable][rm]) / sum(cat(1, room[area]))
        Ryearly_thermostat_heating_variable = yearly_thermostat_heating_variable + (room[area][rm] * room[yearly_thermostat_heating_variable][rm]) / sum(cat(1, room[area]))
        Ryearly_thermostat_cooling_variable = yearly_thermostat_cooling_variable + (room[area][rm] * room[yearly_thermostat_cooling_variable][rm]) / sum(cat(1, room[area]))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Ventilation
    # == == == == == ==

    for rm in range(0,room_num):

                 # Create ventilation profile \
    # -------------------------- \
        room[yearly_ventilation_nominal][rm] = room[yearly_occupancy_nominal][rm]
        room[yearly_ventilation_variable][rm] = room[yearly_occupancy_variable][rm]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Ventilation rate
    # == == == == == == == ==
        room[ventilation_nominal][rm] = db2024(room[row][rm], 24) / 3600 # m3 / m2s
        room[ventilation_nominal_per_person][rm] = db2024(room[row][rm], 22) # m3 / (Ph)
        room[ventilation_night_nominal_per_person][rm] = db2024(room[row][rm], 23) # m3 / (Ph)

    if vent_uncertainty == 1:
            # If we consider the ventilation rate per person variable, then:
        #---------------------------------------------------------------
        if room[ventilation_nominal_per_person][rm] == 0: # e.g. for a kitchen or a bathroom
            room[ventilation_variable][rm] = normrnd(room[ventilation_nominal][rm], room[ventilation_nominal][rm] / 10, [value_number 1]) # m3 / (m2s)
        else:
            room[ventilation_per_person_variable][rm]= normrnd(room[ventilation_nominal_per_person][rm], room[ventilation_nominal_per_person][rm] / 10, [value_number 1]) # m3 / (Ph)
            room[ventilation_variable][rm] = room[ventilation_per_person_variable][rm]/ room[area_per_person_variable][rm] / 3600 # m3 / (m2s)
    else:
    # If per person ventilation rate uncertainty is not considered, then:
        #------------------------------------------------------------------- \
        room[ventilation_variable][rm]= repmat(room[ventilation_nominal][rm], value_number, 1); # m3 / m2s

    # Nominal profiles
    if room[ventilation_night_nominal_per_person][rm]!= 0:
        for i in range(0,365):
            if i == 1:
                room[yearly_ventilation_nominal][rm](i:(wake - 1)) = room[yearly_ventilation_nominal][rm](i:(wake - 1)) *room[ventilation_night_nominal_per_person][rm] / room[ventilation_nominal_per_person][rm]
                room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):(24 * i + wake)) = room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):(24 * i + wake)) *room[ventilation_night_nominal_per_person ][rm]/ room[ventilation_nominal_per_person][rm]

    elif i == 365:
        room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):end) = room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):end) *room[ventilation_night_nominal_per_person][rm] / room[ventilation_nominal_per_person][rm]
    else:
        room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room[yearly_ventilation_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) *room[ventilation_night_nominal_per_person][rm] / room[ventilation_nominal_per_person][rm]


    # Variable profiles
    if room[rm].ventilation_night_nominal_per_person
    ~ = 0
    for j = 1:1:prof_number
    for i = 1:365
    if i == 1:
        room[rm].yearly_ventilation_variable(i:(wake_var(i, j) - 1), j) = room[rm].yearly_ventilation_variable(i:(wake_var(i, j) - 1), j) *room[rm].ventilation_night_nominal_per_person / room[rm].ventilation_nominal_per_person;
        room[rm].yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + wake_var(i, j)), j) = room[rm].yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + wake_var(i, j)), j) *room[rm].ventilation_night_nominal_per_person / room[rm].ventilation_nominal_per_person;
    elif i == 365:
    room[rm].yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):end, j) = room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):end, j) *room(rm).ventilation_night_nominal_per_person / room[rm].ventilation_nominal_per_person;
    else
    room[rm].yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room[rm].yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) *room[rm].ventilation_night_nominal_per_person / room[rm].ventilation_nominal_per_person;
    end
    end
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    #Initialization \
      # -------------- \
    ventilation_nominal = 0
    yearly_ventilation_nominal = 0

    ventilation_variable = 0

    # Calculation
    # -----------
    for rm in range(0,room_num):
    # Nominal values \
    # -------------- \
        ventilation_nominal = ventilation_nominal + (room[area][rm] * room[ventilation_nominal][rm]) / sum(cat(1, room[area]))

    # Variable values \
    # --------------- \
        ventilation_variable = ventilation_variable + (room[area][rm] * room[ventilation_variable][rm]) / sum(cat(1, room.area))
    end

    for rm in range(0,room_num):
                 # Nominal values \
    # -------------- \
        yearly_ventilation_nominal = yearly_ventilation_nominal + room[yearly_ventilation_nominal][rm] * (room[area][rm] / sum(cat(1, room.area))) * room[ventilation_nominal][rm] / ventilation_nominal
    end

    for j in range(0,prof_number):
    yearly_ventilation_variable(:, j) = np.zeros(8760)
    for rm in range(0,room_num):
                 # Variable values
    # ---------------
    yearly_ventilation_variable[:, j] = yearly_ventilation_variable[:, j] + room[yearly_ventilation_variable][rm][:, j] *(room[area][rm] / sum(cat(1, room.area))) * room[ventilation_variable][rm][j] / ventilation_variable[j]
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Infiltration profile(new)
    # == == == == == == == == == == == == == =

    for rm in range(0,room_num):

                 # Create profile for infiltration
    # -------------------------------
    room[yearly_infiltration_nominal][rm] = repmat(ones(1, 1), 8760, 1) # Constant infiltration profile for the whole year
    room[yearly_infiltration_variable][rm] = repmat(ones(1, 1), 8760, prof_number) # Constant infiltration profile for the whole year

    # If the building is mechanically ventilated, the infiltration is reduced to 25 percent of its nominal value during occupancy hours
    # -------------------------------------------------------------------------
    if room[mech_vent][rm] == 1:
    if room[pressurisation][rm] == 1:
        room[yearly_infiltration_nominal][rm][room[early_occupancy_nominal][rm] > 0] = 0.25 # Infiltration not considered during occupied hours
        room[yearly_infiltration_variable][rm](room[yearly_occupancy_variable][rm] > 0] = 0.25 # Infiltration not considered during occupied hours
        end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Infiltration value
    # ------------------

    if infilt_uncertainty == 1:
    # If we consider the Infiltration rate variable, then:
       #----------------------------------------------------
        room[infiltration_rate_variable][rm] = normrnd(room[infiltration_rate_nominal][rm],room[infiltration_rate_nominal][rm] / 5, [value_number,1]) # ACH
    else:
    # If Infiltration rate uncertainty is not considered, then:
    # --------------------------------------------------------- \
        room[infiltration_rate_variable][rm] = repmat(room[infiltration_rate_nominal][rm], value_number, 1) # ACH

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    infiltration_rate_nominal = 0
    yearly_infiltration_nominal = 0

    infiltration_rate_variable = 0
    yearly_infiltration_variable = 0

    # Calculation
    # -----------
    for rm range(0,room_num):
        # Nominal values \
        # -------------- \
        infiltration_rate_nominal = infiltration_rate_nominal + (room[area][rm] * room[infiltration_rate_nominal][rm]) / sum(cat(1, room.area))
        yearly_infiltration_nominal = yearly_infiltration_nominal + (room[area][rm] * room[yearly_infiltration_nominal][rm]) / sum(cat(1, room.area))
    # Variable values \
    # --------------- \
        infiltration_rate_variable = infiltration_rate_variable + (room[area][rm]* room[infiltration_rate_variable][rm]) / sum(cat(1, room.area))
        yearly_infiltration_variable = yearly_infiltration_variable + (room[area][rm] * room[yearly_infiltration_variable][rm]) / sum(cat(1, room.area))
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # DHW
    # == ==

    for rm in range(0,room_num):

                     # DHW profile
        # == == == == == =

        # DHW profile follows occupancy \
        # ----------------------------- \
        room[rm].yearly_dhw_nominal = room[yearly_occupancy_nominal][rm]
        room[rm].yearly_dhw_variable = room[yearly_occupancy_variable][rm]

    # DHW profile for rooms that people sleep in, hence occupied at night, must  be zero during nighttime.For an office building, that is not necessary
    # as the occupancy during these times is equal to zero, hence, the DHW  profile will also be zero.
    # -------------------------------------------------------------------------

    # Nominal profiles
    if room[night_dhw][rm] == 1
        for i in range(0,365):
            if i == 1:
                room[yearly_dhw_nominal][rm](i:(wake - 1)) = 0
                room[yearly_dhw_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0
            elif i == 365:
                room[yearly_dhw_nominal][rm]((24 * i - (24 - sleep)):end) = 0
            else:
                room[yearly_dhw_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0
    end
    end
    end

    # Variable profiles
    if room[rm].night_dhw == 1
    for j = 1:prof_number
    for i = 1:365
    if i == 1
    room[yearly_dhw_variable][rm](i:(wake_var(i, j) - 1), j) = 0
    room[yearly_dhw_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0
    elseif
    i == 365
    room[yearly_dhw_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) = 0
    else:
        room[yearly_dhw_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0
    end
    end
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # DHW values
    # == == == == ==

    # DHW level(nominal, minimum, maximum) \
    # ------------------------------------- \
    room[dhw_nominal][rm] = db2024.loc[room[row][rm], 30] # W / m2
    room[dhw_min][rm] = db2024.loc[room[row][rm], 111] # W / m2
    room[dhw_max][rm] = db2024.loc[room[row][rm], 112]# W / m2

                                                    # Create triangular distribution \
    # ------------------------------ \
    x0 = [room[rm].dhw_min - 1, room[rm].dhw_max + 1]
    [x, fval, flag] = fsolve( @ (x)my_triang(x, room[dhw_min][rm], room[dhw_max][rm], room[dhw_nominal][rm]), x0) # Callsolver

    if flag == -2
        x[1] = room[dhw_min][rm]
        x[2] = room[dhw_max][rm]
    end

    # Sample from triangular distribution
    # -----------------------------------
    if x(1) == x(2) & & x(2) == room[rm].dhw_nominal
    room[rm].dhw_variable = zeros(value_number, 1)
    else
    pdd = makedist('Triangular', 'a', x(1), 'b', room[rm].dhw_nominal, 'c', x(2))
    room[rm].dhw_variable = random(pdd, value_number, 1)
    room[rm].dhw_variable = round(room[rm].dhw_variable, 1)# round to 1 decimal digit
    en
    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    dhw_nominal = 0
    yearly_dhw_nominal = 0

    dhw_variable = np.zeros(prof_number)

    # Calculation
    # -----------
    for rm i in range(0,room_num):
                 # Nominal values
    # --------------
        if room[dhw_nominal][rm] == 0:
            dhw_nominal = dhw_nominal
        else:
            dhw_nominal = dhw_nominal + (room[area][rm] * room[dhw_nominal][rm]) / sum(cat(1, room.area))
        # Variable values
    # ---------------
    if room[dhw_nominal][rm] == 0:
        dhw_variable = dhw_variable
    else:
        dhw_variable = dhw_variable + (room[area][rm] * room[dhw_variable][rm]) / sum(cat(1, room.area))

    for rm in range(0,room_num):
    # Nominalvalues
    # --------------
        if dhw_nominal!= 0:
            yearly_dhw_nominal = yearly_dhw_nominal + room[yearly_dhw_nominal][rm] * (room[area][rm] / sum(cat(1, room.area))) * room[dhw_nominal][rm] / dhw_nominal

    for j in range(0,prof_number):
        yearly_dhw_variable[:, j] = np.zeros(8760)
        for rm in range(0,room_num):
            # Variable values
            # ---------------
            if dhw_variable[j] ! = 0:
                yearly_dhw_variable[:, j] = yearly_dhw_variable[:, j] + room[yearly_dhw_variable][rm][:, j] *(room[area][rm] / sum(cat(1, room.area))) * room[dhw_variable][rm](j) / dhw_variable(j)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Lighting
    # == == == == =

    for rm in range(0,room_num):

    # Lightingprofile
    # == == == == == == == ==

    # Should the lighting profile follow the occupancy profile? (1 = YES, 0 = NO)
    # ---------------------------------------------------------------------------
    room[Follow_occupancy][rm] = db2024.loc[room[row][rm], 113]

    # Initialization of lighting profile \
    # ---------------------------------- \
    room[yearly_lighting_nominal][rm] = np.zeros(8760)
    room[yearly_lighting_variable][rm] = np.zeros(8760, prof_number)

    if room[Follow_occupancy][rm] == 1:
        room[yearly_lighting_nominal][rm] = room[yearly_occupancy_nominal][rm]
        room[yearly_lighting_variable][rm] = room[yearly_occupancy_variable][rm]
    else:
        room[yearly_lighting_nominal][rm](room[yearly_occupancy_nominal][rm]> 0) = 1 * room[yearly_variation_nominal][rm](room[yearly_occupancy_nominal][rm] > 0)
        room[yearly_lighting_variable][rm](room[yearly_occupancy_variable][rm] > 0) = 1 * room[yearly_variation_variable][rm](room[yearly_occupancy_variable][rm] > 0)

    # Correct for weekend days
    # ------------------------
    if room[ruhetage][rm]==1:
        room[yearly_lighting_nominal][rm][day_for_each_hour_of_year == 7] = 0
        room[yearly_lighting_variable][rm][day_for_each_hour_of_year == 7,:] = 0
    elif room[ruhetage][rm]==2:
        room[yearly_lighting_nominal][rm](day_for_each_hour_of_year == 6) = 0
        room[yearly_lighting_nominal][rm](day_for_each_hour_of_year == 7) = 0
        room[yearly_lighting_variable][rm]day_for_each_hour_of_year == 6,:) = 0
        room[yearly_lighting_variable][rm](day_for_each_hour_of_year == 7,:) = 0

    room[yearly_lighting_variable][rm](room[yearly_lighting_variable][rm] > 1) = 1

    # Correct for nighttime lighting
    # ------------------------------
    # Building types that will have the lights off during occupied hours are
    # buildings where people are sleeping.These are: residences, hotels, hospitals.

    # Turn of the lights during night for the building types specified
    # ----------------------------------------------------------------

    # Nominal profiles
    if room[night_light][rm] == 1:
        for i in range(0,365):
            if i == 0:
                room[yearly_lighting_nominal][rm](i:(wake - 1)) = 0
                room[yearly_lighting_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0
            elif i == 364:
                room[yearly_lighting_nominal][rm]((24 * i - (24 - sleep)):end) = 0
            else:
                room[yearly_lighting_nominal][rm]((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0

    # Variable profiles
    if room[night_light][rm] == 1:
        for j in range(0,prof_number):
            for i in range(0,365):
                if i == 0:
                    room[yearly_lighting_variable][rm](i:(wake_var(i, j) - 1), j) = 0
                    room[yearly_lighting_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0
                elif i == 364:
                    room[yearly_lighting_variable][rm]((24 * i - (24 - sleep_var(i, j))):end, j) = 0
                else:
                    room[yearly_lighting_variable][rm]((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Lighting setpoint
    # == == == == == == == == =
    room[light_stp_nominal][rm] = db2024.loc[room[row][rm], 13] # Use for daylighting

    # If we consider the lighting setpoint variable, then:
    # ---------------------------------------------------------------
    room[light_stp_variable][rm] = normrnd(room[light_stp_nominal][rm], room[light_stp_nominal][rm] / 10,[value_number 1])

    # If lighting setpoint uncertainty is not considered, then:
    # ---------------------------------------------------------------
    room[light_stp_variable][rm] = repmat(room[light_stp_nominal][rm], value_number, 1)

    # Lighting density(nominal, minimum, maximum) \
    # -------------------------------------------- \
    room[light_density_nominal][rm] = db2024.loc[room[row][rm], 16] + db2024[room[row][rm], 20] #Use for internal gains and energy consumption
    room[light_density_min][rm] = db2024.loc[room[row][rm], 17] + db2024[room[row][rm], 21] # Use for internal gains and energy consumption
    room[light_density_max][rm] = db2024[room[row][rm], 18] + + db2024[room[row][rm], 20] # Use for internal gains and energy consumption

    # Create triangular distribution
    # ------------------------------
    x0 =[room[light_density_min][rm] - 1, room[light_density_max + 1][rm]
    [x, ~] = fsolve( @ (x)my_triang(x, room[light_density_min][rm], room[light_density_max][rm], room[light_density_nominal][rm]), x0) # Call solver

    # Sample from triangular distribution
    # -----------------------------------
    pdd = makedist('Triangular', 'a', x[1], 'b', room[light_density_nominal][rm], 'c', x[2])
    room[light_density_variable][rm] = random(pdd, value_number, 1)
    room[ight_density_variable][rm] = round(room[rm].light_density_variable, 1) # round to 1 decimal digit

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization
    # --------------
    light_density_nominal = 0
    light_stp_nominal = 0
    yearly_lighting_nominal = 0

    light_density_variable = 0
    light_stp_variable = 0

    # Calculation
    # -----------
    for rm in range(0,room_num):
                 # Nominalvalues
    # --------------
    if room[light_density_nominal][rm] == 0:
        light_density_nominal = light_density_nominal
        light_stp_nominal = light_stp_nominal
    else:
        light_density_nominal = light_density_nominal + (room[area][rm] * room[light_density_nominal][rm]) / sum(cat(1, room[area]))
        light_stp_nominal = light_stp_nominal + (room[area][rm] * room[rm].light_stp_nominal) / sum(cat(1, room.area))

    # Variable values
    # ---------------
    if room[rm].light_density_nominal == 0:
        light_density_variable = light_density_variable
        light_stp_variable = light_stp_variable
    else:
        light_density_variable = light_density_variable + (room[area][rm] * room[light_density_variable][rm]) / sum(cat(1, room.area))
        light_stp_variable = light_stp_variable + (room[area][rm] * room[light_stp_variable][rm]) / sum(cat(1, room.area))

    for rm in range(0,room_num):
        # Nominal values \
        # -------------- \
        yearly_lighting_nominal = yearly_lighting_nominal + room[yearly_lighting_nominal][rm] * (room[area][rm] / sum(cat(1, room.area))) * room[light_density_nominal][rm] / light_density_nominal

    for j in range(0,prof_number):
        yearly_lighting_variable[:, j] = np.zeros(8760)
    for rm in range(0,room_num):
        # Variablevalues
        # ---------------
        yearly_lighting_variable(:, j) = yearly_lighting_variable(:, j) + room[yearly_lighting_variable][rm](:, j) *(room[area][rm] / sum(cat(1, room.area))) * room[light_density_variable][rm][j] / light_density_variable[j]


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Appliances
    # == == == == == =

    for rm in range(0,room_num)

    # Daily appliances profile
    # == == == == == == == == == == == ==

    # Read nominal profile
    # --------------------
    room[daily_appliances_nominal][rm] = db2024.loc(room[row][rm], range(57,81)) # Profile from SIA 2024

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Add vertical variation
    # == == == == == == == == == == ==

    #Initialization of appliances profile \
    # ------------------------------------ \
    room[yearly_appliances_nominal][rm] = np.zeros(8760)
    room[yearly_appliances_variable][rm] = np.zeros((8760, prof_number))

    # Creation of appliances profile according to monthly nominal and variable schedules
    # ----------------------------------------------------------------------------------
    for i in range(0,365):
        room[yearly_appliances_nominal][rm]((i - 1) * 24 + 1:i * 24) = room[daily_appliances_nominal][rm] * room[daily_variation_nominal[i]][rm]
    for j in range(0,prof_number)
        room[yearly_appliances_variable][rm].((i - 1) * 24 + 1:i * 24, j) = room[daily_appliances_nominal][rm] * room[daily_variation_variable][rm][i, j]

    # Create random values in the range[-vert_var, vert_var] for each hour of each variable hourly appliance usage profile
    # ------------------------------------------------------------------------
    X0 = -vert_var + (vert_var - (-vert_var)) * rand(8760, prof_number)

    # Apply vertical variability to hourly profiles
    # -----------------------------------------------
    room[yearly_appliances_variable ][rm]= room[yearly_appliances_variable][rm]* (1 + X0)

    # Set yearly_appliances profile minimum to 10 percent and maximum 100 percent
    # -------------------------------------------------------------
    room[yearly_appliances_nominal][rm](room[yearly_appliances_nominal][rm] < 0.1) = 0.10
    room[yearly_appliances_variable][rm](room[yearly_appliances_variable][rm] < 0.1) = 0.10
    room[yearly_appliances_nominal][rm](room[yearly_appliances_nominal][rm] > 1) = 1
    room[yearly_appliances_variable][rm](room[yearly_appliances_variable][rm] > 1) = 1

    # Check for weekends
    # ------------------
    if room[ruhetage][rm]==1:
        room[yearly_appliances_nominal][rm](day_for_each_hour_of_year == 7) = 0.10
        room[yearly_appliances_variable][rm](day_for_each_hour_of_year == 7) = 0.10
    elif room[ruhetage][rm]==2:
        room[yearly_appliances_nominal][rm](day_for_each_hour_of_year == 6) = 0.10
        room[yearly_appliances_nominal][rm](day_for_each_hour_of_year == 7) = 0.10
        room[yearly_appliances_variable][rm](day_for_each_hour_of_year == 6) = 0.10
        room[yearly_appliances_variable][rm](day_for_each_hour_of_year == 7) = 0.10
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Add horizontal variability to the appliances profiles
    # == == == == == == == == == == == == == == == == == == == == == == == == == =
    room[yearly_appliances_variable][rm] = horizontal_variability(room[yearly_appliances_variable][rm], room[appliance_breaks][rm])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Appliances level value (nominal, minimum, maximum)
    # --------------------------------------------------
    room[appliances_level_nominal][rm] = db2024(room[row][rm], 6) # W / m2  ** ** ** ** ** **
    room[appliances_level_min][rm] = db2024(room[row][rm], 7) # W / m2  ** ** ** ** ** **
    room[appliances_level_max][rm] = db2024(room[row][rm], 8) # W / m2  ** ** ** ** ** **

    # Create triangular distribution
    # ------------------------------
    x0 =[room[appliances_level_min][rm] - 1, room[appliances_level_max][rm] + 1]
    [x, ~] = fsolve( @ (x)my_triang(x, room[appliances_level_min][rm], room[rm]., room[rm].appliances_level_nominal), x0) # Call solver

    # Sample from triangular distribution
    # -----------------------------------
    pdd = makedist('Triangular', 'a', x(1), 'b', room[rm].appliances_level_nominal, 'c', x(2))
    room[appliances_level_variable][rm] = random(pdd, value_number, 1)
    room[appliances_level_variable][rm] = round(room[rm].appliances_level_variable, 1) # round to 1 decimal digit

    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization
    # --------------
    appliances_level_nominal = 0
    yearly_appliances_nominal = 0

    appliances_level_variable = np.zeros(prof_number, 1)

    # Calculation
    # -----------
    for rm = 1:1:room_num
                 # Nominal values
    # --------------
    if room[appliances_level_nominal][rm] == 0:
        appliances_level_nominal = appliances_level_nominal
    else:
        appliances_level_nominal = appliances_level_nominal + (room[area][rm] * room[appliances_level_nominal][rm]) / sum(cat(1, room.area))
    # Variable values
    # ---------------
    if room[appliances_level_nominal][rm] == 0:
        appliances_level_variable = appliances_level_variable
    else:
        appliances_level_variable = appliances_level_variable + (room[area][rm] * room[appliances_level_variable][rm]) / sum(cat(1, room.area))

    for rm in range(0,room_num):
        # Nominal values
        # --------------
        if appliances_level_nominal != 0:
             yearly_appliances_nominal = yearly_appliances_nominal + room[yearly_appliances_nominal][rm] * (room[area][rm] / sum(cat(1, room.area))) * room[appliances_level_nominal][rm] / appliances_level_nominal

    for j in range(0,prof_number):
        yearly_appliances_variable[:, j] = np.zeros(8760)
    for rm in range(0,room_num) # Variable values
    # ---------------
    if appliances_level_variable[j] != 0:
        yearly_appliances_variable[:, j] = yearly_appliances_variable[:, j] + room[yearly_appliances_variable][rm][:, j] *(room[area][rm] / sum(cat(1,room.area))) * room[appliances_level_variable[j]][rm] / appliances_level_variable[j]

    # Correction if appliances schedule exceeds 1
    yearly_appliances_variable(yearly_appliances_variable > 1) = 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Final report nominal values
    # == == == == == == == == == == == == == ==

    # Write scalar values
    # == == == == == == == == == =
    if variable_schedules == 'variable': # if only nominal schedules should be generated
        Explanations = ['This factor (m2/person) is used, along with the Zone Floor Area to determine the maximum number of people as described in the Number of People field. The choice from the method field should be Area/Person',
        'The heating setpoint temperature in degrees C if constant throughout the year. If the previous field is used this field should be left blank and will be ignored',
        'The cooling setpoint temperature in degrees C if constant throughout the year. If the previous field is used this field should be left blank and will be ignored',
        'The design outdoor air volume flow rate per person (m3/s/m2). This input is used if Outdoor Air Method is Flow/Area. The default value for this field is 0',
        'This factor (ACH) is used to determine the maximum Design Flow Rate as described in the Design Flow Rate field. The choice from the method field should be AirChanges/Hour',
        'This factor (watts/m2) is used, along with the Zone Area to determine the maximum equipment level as described in the Design Level field. The choice from the method field should be Watts/Area',
        'This factor (watts/m2) is used, along with the Zone Floor Area to determine the maximum lighting level as described in the Lighting Level field. The choice from the method field should be Watts/Area',
        'The desired lighting level (in lux) at the First Reference Point. This is the lighting level that would be produced at this reference point at night if the overhead electric lighting were operating at full input power. Recommended values depend on type of activity',
        'This factor (watts/m2) is used, along with the Zone Area to determine the maximum equipment level as described in the Design Level field. The choice from the method field should be Watts/Area']

        C = [area_per_person_nominal 'm2/P' Explanations(1),therm_h_nominal 'degrees C' Explanations(2),therm_c_nominal 'degrees C' Explanations(3),ventilation_nominal 'm3/(m2s)' Explanations(4),
        infiltration_rate_nominal 'ACH' Explanations(5),
        dhw_nominal 'W/m2' Explanations(6),
        light_density_nominal 'W/m2' Explanations(7),
        light_stp_nominal 'lux' Explanations(8),appliances_level_nominal 'W/m2' Explanations(9)]

        RowNames = {'People:People per Zone Floor Area', 'HVACTemplate:Thermostat:Constant Heating Setpoint', 'HVACTemplate:Thermostat:Constant Cooling Setpoint', ...
        'DesignSpecification:OutdoorAir:Outdoor Air Flow per Zone Floor Area', 'ZoneInfiltration:DesignFlowRate:Flow per Zone Floor Area', ...
        'HotWaterEquipment:Power per Zone Floor Area', 'Lights:Watts per Zone Floor Area', ...
        'Daylighting:Controls:Illuminance Setpoint at First Reference Point', 'ElectricEquipment:Watts per Zone Floor Area'};

        VariableNames = {'Value', 'Units', 'Explanation'};

        T = cell2table(C, 'RowNames', RowNames, 'VariableNames', VariableNames);

        writetable(T, strcat(path_nominal, bldg, '_summary', '.xlsx'), 'WriteVariableNames', 1, 'WriteRowNames', 1);

        # Write profiles
        # == == == == == == == =

        # Occupancy
        # ---------
        csvwrite(strcat(path_nominal, bldg, '_nominal_occupancy.csv'), yearly_occupancy_nominal);
        csvwrite(strcat(path_nominal, bldg, '_nominal_activity.csv'), yearly_activity_nominal);

        # Thermostats
        # -----------
        csvwrite(strcat(path_nominal, bldg, '_nominal_thermostat_heating.csv'), yearly_thermostat_heating_nominal);
        csvwrite(strcat(path_nominal, bldg, '_nominal_thermostat_cooling.csv'), yearly_thermostat_cooling_nominal);

        # Infiltration
        # ------------
        csvwrite(strcat(path_nominal, bldg, '_nominal_infiltration.csv'), yearly_infiltration_nominal);

        # Ventilation
        # -----------
        csvwrite(strcat(path_nominal, bldg, '_nominal_ventilation.csv'), yearly_ventilation_nominal);

        # DHW
        # ---
        csvwrite(strcat(path_nominal, bldg, '_nominal_dhw.csv'), yearly_dhw_nominal);

        # Lighting
        # --------
        csvwrite(strcat(path_nominal, bldg, '_nominal_lighting.csv'), yearly_lighting_nominal);

        # Appliances
        # ----------
        csvwrite(strcat(path_nominal, bldg, '_nominal_appliances.csv'), yearly_appliances_nominal);

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # % Final report uncertain values
        # == == == == == == == == == == == == == == ==
    elif uncertainty == 1:

        # Write profiles
        # == == == == == == ==

        # fmt =[repmat('%6.2f ', 1, prof_number), '\n']; % formatSpec for fprintf

        # Occupancy
        # ---------
        csvwrite(strcat(path_variable, bldg, '_variable_occupancy.csv'), yearly_occupancy_variable)
        csvwrite(strcat(path_variable, bldg, '_variable_activity.csv'), yearly_activity_variable)

        # Thermostats
        #-----------
        csvwrite(strcat(path_variable, bldg, '_variable_thermostat_heating.csv'), yearly_thermostat_heating_variable)
        csvwrite(strcat(path_variable, bldg, '_variable_thermostat_cooling.csv'), yearly_thermostat_cooling_variable)

        # Infiltration
        # ------------
        csvwrite(strcat(path_variable, bldg, '_variable_infiltration.csv'), yearly_infiltration_variable)

        # Ventilation
        # -----------
        csvwrite(strcat(path_variable, bldg, '_variable_ventilation.csv'), yearly_ventilation_variable)

        # DHW
        # ---
        csvwrite(strcat(path_variable, bldg, '_variable_dhw.csv'), yearly_dhw_variable)

        # Lighting
        # --------
        csvwrite(strcat(path_variable, bldg, '_variable_lighting.csv'), yearly_lighting_variable)

        # Appliances
        # ----------
        csvwrite(strcat(path_variable, bldg, '_variable_appliances.csv'), yearly_appliances_variable)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Write variable scalar values
        # == == == == == == == == == == == == == ==

        # fmt =['%6.2f\n']; % formatSpec for fprintf

        csvwrite(strcat(path_variable, bldg, '_area_per_person_variable.csv'), area_per_person_variable)
        # fid = fopen(strcat(path_variable, bldg, '_area_per_person_variable.txt'), 'wt');
        # fprintf(fid, '%6.3f\n', area_per_person_variable); fclose(fid);

        fid = fopen(strcat(path_variable, bldg, '_therm_h_variable.txt'), 'wt')
        fprintf(fid, '%6.3f\n', therm_h_variable); fclose(fid);

        fid = fopen(strcat(path_variable, bldg, '_therm_c_variable.txt'), 'wt')
        fprintf(fid, '%6.3f\n', therm_c_variable); fclose(fid)

        csvwrite(strcat(path_variable, bldg, '_infiltration_rate_variable.csv'), infiltration_rate_variable)
        # fid = fopen(strcat(path_variable, bldg, '_infiltration_rate_variable.txt'), 'wt');
        # fprintf(fid, '%6.7f\n', infiltration_rate_variable); fclose(fid);

        csvwrite(strcat(path_variable, bldg, '_ventilation_rate_variable.csv'), ventilation_variable)
        # fid = fopen(strcat(path_variable, bldg, '_ventilation_rate_variable.txt'), 'wt');
        # fprintf(fid, '%6.7f\n', ventilation_variable); fclose(fid);

        csvwrite(strcat(path_variable, bldg, '_dhw_variable.csv'), dhw_variable)
        # fid = fopen(strcat(path_variable, bldg, '_dhw_variable.txt'), 'wt');
        # fprintf(fid, '%6.3f\n', dhw_variable); fclose(fid);

        csvwrite(strcat(path_variable, bldg, '_light_density_variable.csv'), light_density_variable)
        # fid = fopen(strcat(path_variable, bldg, '_light_density_variable.txt'), 'wt');
        # fprintf(fid, '%6.3f\n', light_density_variable); fclose(fid);

        fid = fopen(strcat(path_variable, bldg, '_light_stp_variable.txt'), 'wt')
        fprintf(fid, '%6.3f\n', light_stp_variable);
        fclose(fid)

        csvwrite(strcat(path_variable, bldg, '_appliances_level_variable.csv'), appliances_level_variable)
        # fid = fopen(strcat(path_variable, bldg, '_appliances_level_variable.txt'), 'wt')
        # fprintf(fid, '%6.3f\n', appliances_level_variable);
        # fclose(fid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Write combinatorial files
    # == == == == == == == == == == == == =

    # The first file will contain a column number for each occupancy, activity, thermostat, ventilation, dhw and lighting schedule.Each
    # subsequent column will have the required "capacities" for the occupancy, ventilation, dhw, and lighting."Capacities" for activity
    # and thermostat are not needed as they are directly defined in the  schedules.

    first_file =[(1:prof_number)', area_per_person_variable, ventilation_variable, dhw_variable, light_density_variable];
    dlmwrite(strcat(path_variable, bldg, '_occ_act_therm_vent_dhw_light_col_levels.txt'), first_file, 'delimiter', '|','precision', 3)

    # The second file will perform a similar task but with a column for  each appliance profile and the corresponding installed appliances capacity.

    second_file =[(1:prof_number)', appliances_level_variable];
    dlmwrite(strcat(path_variable, bldg, '_appliances_col_level.txt'), second_file, 'delimiter', '|', 'precision', 3)

    # The final file that would be needed is the infiltration.However, the previously written infiltration_rate_variable.txt is adequate for the  way that infiltration is modelled.
    return

