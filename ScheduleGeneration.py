def rle_cumsum_diff(vals,runlens):
    import numpy as np
    clens = np.cumsum(runlens)
    idx = np.zeros(8760)
    difference = np.diff(vals)
    inter = clens[0:len(clens) - 1]
    for i in range(0, 364):
        idx[int(inter[i])] = difference[i]
    out = np.cumsum(idx)
    return [out]

def horizonal_variability(profile, breaks):
    # Function that implements the "horizontal variability" aspect in the
    # variable SIA 2024 profiles
    perturb = breaks

    if len(breaks) == 0:
        perturbed_profile = profile
    else:
        for i in range(1,365):
            perturb = [perturb, breaks + 24 * (i - 1)]

    [~, prof_size] = len(profile)

    for i in range(0,prof_size):
        if rand() <= 0.6 # Probability that a profile will be perturbed or not; set to 1 to perturb all profiles
            perturbation_values = randpermbreak(8760, perturb)
            perturbed_profile(:, i) = profile(perturbation_values, i)
        else:
            perturbed_profile(:, i) = profile(:, i)
    return perturbed_profile


def CESAR_function_Variability_case_multiroom_selection(prof_nr, value_nr, variable_schedules, schedulepath, bldg, project_directory):
    import numpy as np
    import pandas as pd
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
    if bldg == 'mfh':
        room_num = 2
        # MFH composition according to SIA 2024 v.2016
        room[name][0] = 'MFH'
        room[1] = 'Staircase'
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

    for rm in range(0,room_num):

            # Create nominal profile
        # == == == == == == == == == == ==
        room[monthly_variation_nominal][rm] = db2024.loc[room[row][rm], 81:92]
        room[daily_occupancy_nominal][rm] = db2024.loc[room[row][rm], 33:56]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Add vertical monthly variability
        # == == == == == == == == == == == == == == == ==

        # Create variable values for each month
        # -------------------------------------
        X0 = np.random.rand(prof_number, 12)

        # Remap variable values between the limits dictated by the vertical variation
        # ---------------------------------------------------------------------------
        X0=(vert_var*X0+(1-X0)*(-vert_var))

        # Create variations for the monthly profile equal to "prof_number"
        # ----------------------------------------------------------------
        room[monthly_variation_variable][rm] = np.zeros(12, prof_number)

        for i in range(0,prof_number):
            room[monthly_variation_variable][rm][:, i] = room[monthly_variation_nominal][rm] * (1 + X0[:, i])

        # Correct values that are higher than 1 \
        # ------------------------------------- \
        room[monthly_variation_variable][rm] = 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Expand monthly variabilities to the whole year
        # == == == == == == == == == == == == == == == == == == == == == == ==

        # Repeat the nominal monthly profile values for each day and each hour of the year
        # --------------------------------------------------------------------------------
        room[daily_variation_nominal][rm] = rle_cumsum_diff(room[monthly_variation_nominal][rm], days_per_month) # repeat each monthly variation value as many times as the days of the month
        room[yearly_variation_nominal][rm] = rle_cumsum_diff(room[monthly_variation_nominal][rm], 24 * days_per_month) # repeat each monthly variation value for each hour based on the month it belongs

        # Repeat the variable monthly profiles values for each day and each hour of the year
        # ----------------------------------------------------------------------------------
        room[daily_variation_variable][rm] = np.zeros(365, prof_number)
        room[yearly_variation_variable][rm] = np.zeros(8760, prof_number)

        for i in range(0,prof_number):
            room[daily_variation_variable][rm][:, i] = rle_cumsum_diff(room[monthly_variation_variable][rm][:, i], days_per_month)
            room[yearly_variation_variable][rm][:, i] = rle_cumsum_diff(room[monthly_variation_variable][rm][:, i], 24 * days_per_month)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Create occupancy profile
        # == == == == == == == == == == == ==

        # Initialization of occupancy profile \
        # ----------------------------------- \
        room[yearly_occupancy_nominal][rm] = np.zeros(8760, 1)
        room[yearly_occupancy_variable][rm] = np.zeros(8760, prof_number)

        # Creation of occupancy profile according to monthly nominal and variable schedules
        # ----------------------------------------------------------------------------------
        for i in range(0,365):
            room[yearly_occupancy_nominal][rm][(i - 1) * 24 + 1:i * 24] = room[rm][daily_occupancy_nominal] * room[daily_variation_nominal][rm][i]
        for j in range(0,prof_number):
            room[yearly_occupancy_variable][rm][(i - 1) * 24 + 1:i * 24, j] = room[daily_occupancy_nominal][rm] * room[daily_variation_variable][rm][i, j]

        # Add vertical variability to the occupancy profiles
        # --------------------------------------------------

        # Create random values in the range[-vert_var, vert_var] for each hour of each variable hourly occupancy profile
        # ------------------------------------------------------------------------
        X0 = -vert_var + (vert_var - (-vert_var)) * np.random.rand(8760, prof_number)

        # Apply vertical variability to hourly profiles
        # -----------------------------------------------
        room[yearly_occupancy_variable][rm] = room[yearly_occupancy_variable][rm]* (1 + X0)

        # Correct for weekend days
        # ------------------------
        if room[ruhetage][rm]== 1:
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 6] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 6,:] = 0
        elif room[ruhetage][rm]== 2:
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 5] = 0
            room[yearly_occupancy_nominal][rm][day_for_each_hour_of_year == 6] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 5,:] = 0
            room[yearly_occupancy_variable][rm][day_for_each_hour_of_year == 6,:] = 0

        room[yearly_occupancy_variable][rm][room[yearly_occupancy_variable ][rm]> 1] = 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Add horizontal variability to the occupancy profiles
        # == == == == == == == == == == == == == == == == == == == == == == == == ==
        room[yearly_occupancy_variable][rm] = horizontal_variability(room[yearly_occupancy_variable][rm],room[occ_breaks][rm])

        # Constant nighttime occupancy if place where people sleep
        # (Correction required only for the variable case)
        # --------------------------------------------------------

        if room[night][rm] == 1:
            for j in range(0,prof_number):
                for i in range(0,365):
                    if i == 1:
                        room[yearly_occupancy_variable][rm][i:[wake_var[i, j] - 1], j] = room[yearly_variation_variable][rm][i:[wake_var[i,j] - 1], j]
                        room[yearly_occupancy_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:[24 * i + [wake_var[i, j] - 1]], j] = room[yearly_variation_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:[24 * i + [wake_var[i, j] - 1]], j]
        elif i == 365:
            room[yearly_occupancy_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:end, j] = room[yearly_variation_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:end, j]
        else:
            room[yearly_occupancy_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:[24 * i + [wake_var[i, j] - 1], j] = room[yearly_variation_variable][rm][[24 * i - [24 - sleep_var[i, j]]]:[24 * i + [wake_var[i, j] - 1]], j]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Calculate presence and activity values for occupancy
        # == == == == == == == == == == == == == == == == == == == == == == == == == ==

        # Number of people per unit area (nominal, minimum, maximum)
        # ----------------------------------------------------------
        room[](rm).area_per_person_nominal = db2024(room(rm).row, 3) # m2 / Person
        room(rm).area_per_person_min = db2024(room(rm).row, 106) # m2 / Person
        room(rm).area_per_person_max = db2024(room(rm).row, 105) # m2 / Person

        # Create triangular distribution
        # ------------------------------
        x0 =[room(rm).area_per_person_min - 1, room(rm).area_per_person_max + 1]
        [x, ~, exitflag] = fsolve( @ (x)my_triang(x, room(rm).area_per_person_min, room(rm).area_per_person_max, room(rm).area_per_person_nominal), x0) # Call solver

        # Sample from triangular distribution
        # -----------------------------------
        pd = makedist('Triangular', 'a', x(1), 'b', room(rm).area_per_person_nominal, 'c', x(2))
        if room(rm).area_per_person_nominal == 0:
            room(rm).area_per_person_variable = zeros(value_number, 1)
        else:
            room(rm).area_per_person_variable = random(pd, value_number, 1)
            room(rm).area_per_person_variable = round(room(rm).area_per_person_variable, 1) # round to 1 decimal digit

        # Occupant activities
        # -----------------------------
        # Calculations are directly made in W / P terms
        # -----------------------------
        room(rm).activity_nominal = db2024(room(rm).row, 5) * room(rm).area_per_person_nominal # W / P
        # If we want uncertain activity, then uncomment the following:
        room(rm).activity_variable = normrnd(activity_nominal, activity_nominal / 20, [value_number 1])
        # If activity uncertainty is not considered, then:
        room(rm).activity_variable = repmat(room(rm).activity_nominal, value_number, 1)

        # Create activity profile \
        # ----------------------- \
        room[rm].yearly_activity_nominal = repmat(room(rm).activity_nominal, 8760, 1)
        room[rm].yearly_activity_variable = repmat(room(rm).activity_variable', 8760, 1)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
      # -------------- \
    area_per_person_nominal = 0
    yearly_occupancy_nominal = 0
    yearly_activity_nominal = 0

    area_per_person_variable = zeros(value_number, 1)

    # Calculation
      # -----------
    for rm = range(0,room_num):
        # Nominal values
        # --------------
        if room(rm).area_per_person_nominal == 0:
            area_per_person_nominal = area_per_person_nominal
        else:
            area_per_person_nominal = area_per_person_nominal + (room(rm).area * 1 / room(rm).area_per_person_nominal) / sum(cat(1, room.area))
    # Variable values
    # ---------------
    if room(rm).area_per_person_nominal == 0:
        area_per_person_variable = area_per_person_variable
    else:
        area_per_person_variable = area_per_person_variable + (
                room(rm).area * 1. / room(rm).area_per_person_variable) / sum(cat(1, room.area))

    if area_per_person_nominal ~ = 0:
        area_per_person_nominal = 1 / area_per_person_nominal
    if area_per_person_variable~ = 0:
    area_per_person_variable = 1. / area_per_person_variable
    else:
        area_per_person_variable = zeros(value_number, 1)
    for rm  in range(0,room_num):
        # Nominal values
        # --------------
    if room(rm).area_per_person_nominal == 0
    yearly_occupancy_nominal = yearly_occupancy_nominal;
    yearly_activity_nominal = yearly_activity_nominal;
    else
    yearly_occupancy_nominal = yearly_occupancy_nominal + (room(rm).area / sum(cat(1, room.area))) * room(
        rm).yearly_occupancy_nominal * (1 / room(rm).area_per_person_nominal) / (1 / area_per_person_nominal);
    yearly_activity_nominal = yearly_activity_nominal + room(rm).area * room(rm).activity_nominal * (
                1 / room(rm).area_per_person_nominal);
    end
    end

    if area_per_person_nominal ~ = 0
    yearly_activity_nominal = yearly_activity_nominal / (1 / area_per_person_nominal) / sum(cat(1, room.area));
    yearly_activity_nominal = repmat(yearly_activity_nominal, 8760, 1); % Creation of activity profile end

    for j = 1:1:prof_number
    yearly_occupancy_variable(:, j) = zeros(8760, 1);
    yearly_activity_variable(j) = 0;
    for rm = 1:1:room_num
    # Variable values
    # ---------------
    if room(rm).area_per_person_nominal == 0
    yearly_occupancy_variable(:, j) = yearly_occupancy_variable(:, j);
    yearly_activity_variable(j) = yearly_activity_variable(j);
    else
    yearly_occupancy_variable(:, j) = yearly_occupancy_variable(:, j) + (room(rm).area / sum(cat(1, room.area))) * room(
        rm).yearly_occupancy_variable(:, j) *(1 / room(rm).area_per_person_variable(j)). / (1 / area_per_person_variable(j));
    yearly_activity_variable(j) = yearly_activity_variable(j) + room(rm).area * room(rm).activity_variable(j) * (1 / room(rm).area_per_person_variable(j));
    end
    end
    end

    yearly_activity_variable = yearly_activity_variable ./ (1./area_per_person_variable) / sum(cat(1, room.area));
    yearly_activity_variable = repelem(yearly_activity_variable, 1, 8760)
    # Creation of activity profile

    # Thermostats
    # == == == == == ==

    for rm = 1:1:room_num

                 # Thermostat values
    # == == == == == == == == =

    # Heating setpoints(nominal, minimum, maximum) \
    # --------------------------------------------- \
    room(rm).therm_h_nominal = db2024(room(rm).row, 2);
    room(rm).therm_h_min = db2024(room(rm).row, 107);
    room(rm).therm_h_max = db2024(room(rm).row, 108);

    # Cooling setpoints(nominal, minimum, maximum) \
    # --------------------------------------------- \
    room(rm).therm_c_nominal = db2024(room(rm).row, 1);
    room(rm).therm_c_min = db2024(room(rm).row, 109);
    room(rm).therm_c_max = db2024(room(rm).row, 110);

    # SAMPLE FROM NORMAL DISTRIBUTIONS
    # == == == == == == == == == == == == == == == ==
    room(rm).therm_h_variable = normrnd(room(rm).therm_h_nominal, 1, [prof_number, 1]);
    room(rm).therm_c_variable = normrnd(room(rm).therm_c_nominal, 1, [prof_number, 1]);

    # Prevent heating setpoint being higher than cooling setpoint \
    # ----------------------------------------------------------- \
        non_compliant_points = find(room(rm).therm_h_variable > room(rm).therm_c_variable);
    if isempty(non_compliant_points) == 0
    for nc = 1:1:max(size(non_compliant_points))
    while room(rm).therm_h_variable(non_compliant_points(nc)) > room(rm).therm_c_variable(non_compliant_points(nc))
        room(rm).therm_h_variable(non_compliant_points(nc)) = normrnd(room(rm).therm_h_nominal, 1, [1, 1]);
        room(rm).therm_c_variable(non_compliant_points(nc)) = normrnd(room(rm).therm_c_nominal, 1, [1, 1]);
    end
    end
    end

    # SAMPLE FROM TRIANGULAR DISTRIBUTIONS
    # == == == == == == == == == == == == == == == == == ==
    # Create triangular distribution
    # ------------------------------
    x0 = [room(rm).therm_h_min - 1, room(rm).therm_h_max + 1]
    [x, ~] = fsolve( @ (x)my_triang(x, room(rm).therm_h_min, room(rm).therm_h_max, room(rm).therm_h_nominal), x0); # Callsolver
    # Sample from triangular distribution
    # -----------------------------------
     pd = makedist('Triangular', 'a', x(1), 'b', room(rm).therm_h_nominal, 'c', x(2));
    # room(rm).therm_h_variable = random(pd, value_number, 1)
    #
    # Create triangular distribution
    # ------------------------------
    # x0 = [room(rm).therm_c_min - 1, room(rm).therm_c_max + 1];
    # [x, ~] = fsolve( @ (x)
    my_triang(x, room(rm).therm_c_min, room(rm).therm_c_max, room(rm).therm_c_nominal), x0)# Call solver
    #
    # Sample from triangular distribution
    # -----------------------------------
    # pd1 = makedist('Triangular', 'a', x(1), 'b', room(rm).therm_c_nominal, 'c', x(2));
    # room(rm).therm_c_variable = random(pd1, value_number, 1);

    # Prevent heating setpoint being higher than cooling setpoint
    # -----------------------------------------------------------
    # non_compliant_points = find(room(rm).therm_h_variable > room(rm).therm_c_variable);
    # if isempty(non_compliant_points) == 0
        # for nc = 1:1:max(size(non_compliant_points))
    # while room(rm).therm_h_variable(non_compliant_points(nc)) > room(rm).therm_c_variable(non_compliant_points(nc))
        # room(rm).therm_h_variable(non_compliant_points(nc)) = random(pd, 1);
    # room(rm).therm_c_variable(non_compliant_points(nc)) = random(pd1, 1);

    room(rm).therm_h_variable = round(room(rm).therm_h_variable, 1)# round to 1 decimal digit
    room(rm).therm_c_variable = round(room(rm).therm_c_variable, 1); # round to 1 decimal digit

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Create thermostat profiles
    # == == == == == == == == == == == == ==
    room(rm).yearly_thermostat_heating_nominal = repmat(room(rm).therm_h_nominal, 8760, 1);
    room(rm).yearly_thermostat_cooling_nominal = repmat(room(rm).therm_c_nominal, 8760, 1);

    room(rm).yearly_thermostat_heating_variable = repmat(room(rm).therm_h_variable', 8760, 1);
    room(rm).yearly_thermostat_cooling_variable = repmat(room(rm).therm_c_variable', 8760, 1);

    # Unoccupied setback
    if room(rm).setback == 1
    room(rm).yearly_thermostat_heating_nominal(room(rm).yearly_occupancy_nominal == 0) = room(rm).yearly_thermostat_heating_nominal(room(rm).yearly_occupancy_nominal == 0) - room(rm).set_back_temp
    room(rm).yearly_thermostat_cooling_nominal(room(rm).yearly_occupancy_nominal == 0) = room(rm).yearly_thermostat_cooling_nominal(room(rm).yearly_occupancy_nominal == 0) + room(rm).set_back_temp

    room(rm).yearly_thermostat_heating_variable(room(rm).yearly_occupancy_variable == 0) = room(rm).yearly_thermostat_heating_variable(room(rm).yearly_occupancy_variable == 0) - room(rm).set_back_temp
    room(rm).yearly_thermostat_cooling_variable(room(rm).yearly_occupancy_variable == 0) = room(rm).yearly_thermostat_cooling_variable(room(rm).yearly_occupancy_variable == 0) + room(rm).set_back_temp

    # Night setback for nominal profile
    if room[night][rm] == 1:
        for i in range(0:365):
            if i == 1:
               # Heating
                room(rm).yearly_thermostat_heating_nominal(i:(wake - 1)) = room(rm).yearly_thermostat_heating_nominal(i:(wake - 1)) - room(rm).set_back_temp;
                room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) - room(rm).set_back_temp;
            # Cooling
                room(rm).yearly_thermostat_cooling_nominal(i:(wake - 1)) = room(rm).yearly_thermostat_cooling_nominal(i:(wake - 1)) + room(rm).set_back_temp;
                room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) + room(rm).set_back_temp;
            elif i == 365:
            # Heating
                room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):end) = room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):end) - room(rm).set_back_temp;
            # Cooling
                room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):end) = room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):end) + room(rm).set_back_temp;
            else:
            # Heating
                room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room(rm).yearly_thermostat_heating_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) - room(rm).set_back_temp;
            # Cooling
                room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room(rm).yearly_thermostat_cooling_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) + room(rm).set_back_temp;
    end
    end
    end

    # Night setback for variable profile
    if room(rm).night == 1
    for j = 1:1:prof_number
    for i = 1:365
    if i == 1
       # Heating
    room(rm).yearly_thermostat_heating_variable(i:(wake_var(i, j) - 1), j) = room(rm).yearly_thermostat_heating_variable(i:(wake_var(i, j) - 1), j) - room(rm).set_back_temp;
    room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) - room(rm).set_back_temp;
    # Cooling
    room(rm).yearly_thermostat_cooling_variable(i:(wake_var(i, j) - 1), j) = room(rm).yearly_thermostat_cooling_variable(i:(wake_var(i, j) - 1), j) + room(rm).set_back_temp;
    room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) + room(rm).set_back_temp;
    elseif
    i == 365
    # Heating
    room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):end, j) = room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):end, j) - room(rm).set_back_temp;
    # Cooling
    room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):end, j) = room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):end, j) + room(rm).set_back_temp;
    else
    # Heating
    room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room(rm).yearly_thermostat_heating_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) - room(rm).set_back_temp;
    # Cooling
    room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room(rm).yearly_thermostat_cooling_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) + room(rm).set_back_temp;
    end
    end
    end
    end

    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    therm_h_nominal = 0
    therm_c_nominal = 0
    yearly_thermostat_heating_nominal = 0
    yearly_thermostat_cooling_nominal = 0

    therm_h_variable = 0
    therm_c_variable = 0
    yearly_thermostat_heating_variable = 0
    yearly_thermostat_cooling_variable = 0

    # Calculation
    # -----------
    for rm in range(0,room_num):
        # Nominal values \
        # -------------- \
        therm_h_nominal = therm_h_nominal + (room(rm).area * room(rm).therm_h_nominal) / sum(cat(1, room.area))
        therm_c_nominal = therm_c_nominal + (room(rm).area * room(rm).therm_c_nominal) / sum(cat(1, room.area))
        yearly_thermostat_heating_nominal = yearly_thermostat_heating_nominal + (room(rm).area * room(rm).yearly_thermostat_heating_nominal) / sum(cat(1, room.area))
        yearly_thermostat_cooling_nominal = yearly_thermostat_cooling_nominal + (room(rm).area * room(rm).yearly_thermostat_cooling_nominal) / sum(cat(1, room.area))
        # Variable values \
    # --------------- \
        therm_h_variable = therm_h_variable + (room(rm).area * room(rm).therm_h_variable) / sum(cat(1, room.area))
        therm_c_variable = therm_c_variable + (room(rm).area * room(rm).therm_c_variable) / sum(cat(1, room.area))
        yearly_thermostat_heating_variable = yearly_thermostat_heating_variable + (room(rm).area * room(rm).yearly_thermostat_heating_variable) / sum(cat(1, room.area))
        yearly_thermostat_cooling_variable = yearly_thermostat_cooling_variable + (room(rm).area * room(rm).yearly_thermostat_cooling_variable) / sum(cat(1, room.area))
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Ventilation
    # == == == == == ==

    for rm in range(0,room_num):

                 # Create ventilation profile \
    # -------------------------- \
        room(rm).yearly_ventilation_nominal = room(rm).yearly_occupancy_nominal
        room(rm).yearly_ventilation_variable = room(rm).yearly_occupancy_variable;

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Ventilation rate
    # == == == == == == == ==
        room[ventilation_nominal][rm] = db2024(room(rm).row, 24) / 3600 # m3 / m2s
        room[rm].ventilation_nominal_per_person = db2024(room(rm).row, 22) # m3 / (Ph)
        room[rm].ventilation_night_nominal_per_person = db2024(room(rm).row, 23) # m3 / (Ph)

    if vent_uncertainty == 1
            # If we consider the ventilation rate per person variable, then:
    #---------------------------------------------------------------
    if room(rm).ventilation_nominal_per_person == 0 # e.g. for a kitchen or a bathroom
    room(rm).ventilation_variable = normrnd(room(rm).ventilation_nominal, room(rm).ventilation_nominal / 10, [value_number 1]); # m3 / (m2s)
    else
    room(rm).ventilation_per_person_variable = normrnd(room(rm).ventilation_nominal_per_person, room(rm).ventilation_nominal_per_person / 10, [value_number 1]); # m3 / (Ph)
    room(rm).ventilation_variable = room(rm).ventilation_per_person_variable./ room(rm).area_per_person_variable / 3600 # m3 / (m2s)
    end
    else
    # If per person ventilation rate uncertainty is not considered, then:
        #------------------------------------------------------------------- \
        room(rm).ventilation_variable = repmat(room(rm).ventilation_nominal, value_number, 1); # m3 / m2s
    end

    # Nominal profiles
    if room(rm).ventilation_night_nominal_per_person
    ~ = 0
    for i = 1:365
    if i == 1
    room(rm).yearly_ventilation_nominal(i:(wake - 1)) = room(rm).yearly_ventilation_nominal(i:(wake - 1)) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
    room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):(24 * i + wake)) = room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):(24 * i + wake)) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;

    elseif i == 365
        room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):end) = room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):end) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
    else
    room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = room(rm).yearly_ventilation_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
    end
    end
    end

    # Variable profiles
    if room(rm).ventilation_night_nominal_per_person
    ~ = 0
    for j = 1:1:prof_number
    for i = 1:365
    if i == 1:
        room(rm).yearly_ventilation_variable(i:(wake_var(i, j) - 1), j) = room(rm).yearly_ventilation_variable(i:(wake_var(i, j) - 1), j) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
        room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + wake_var(i, j)), j) = room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + wake_var(i, j)), j) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
    elif i == 365:
    room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):end, j) = room(
        rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):end, j) *room(
        rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
    else
    room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = room(rm).yearly_ventilation_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) *room(rm).ventilation_night_nominal_per_person / room(rm).ventilation_nominal_per_person;
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
    for rm = 1:1:room_num
                 # Nominal values \
    # -------------- \
        ventilation_nominal = ventilation_nominal + (room(rm).area * room(rm).ventilation_nominal) / sum(cat(1, room.area))

    # Variable values \
    # --------------- \
        ventilation_variable = ventilation_variable + (room(rm).area * room(rm).ventilation_variable) / sum(cat(1, room.area))
    end

    for rm = 1:1:room_num
                 # Nominal values \
    # -------------- \
        yearly_ventilation_nominal = yearly_ventilation_nominal + room(rm).yearly_ventilation_nominal * (room(rm).area / sum(cat(1, room.area))) * room(rm).ventilation_nominal / ventilation_nominal
    end

    for j = 1:1:prof_number
    yearly_ventilation_variable(:, j) = zeros(8760, 1)
    for rm = 1:1:room_num
                 # Variable values
    # ---------------
    yearly_ventilation_variable(:, j) = yearly_ventilation_variable(:, j) + room(rm).yearly_ventilation_variable(:, j) *(room(rm).area / sum(cat(1, room.area))) * room(rm).ventilation_variable(j) / ventilation_variable(j);
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Infiltration profile(new)
    # == == == == == == == == == == == == == =

    for rm = 1:1:room_num

                 # Create profile for infiltration
    # -------------------------------
    room(
        rm).yearly_infiltration_nominal = repmat(ones(1, 1), 8760, 1); # Constant infiltration profile for the whole year
    room(rm).yearly_infiltration_variable = repmat(ones(1, 1), 8760, prof_number); # Constant infiltration profile for the whole year

    # If the building is mechanically ventilated, the infiltration is reduced to 25 percent of its nominal value during occupancy hours
    # -------------------------------------------------------------------------
    if room(rm).mech_vent == 1
    if room(rm).pressurisation == 1
    room(rm).yearly_infiltration_nominal(room(rm).yearly_occupancy_nominal > 0) = 0.25 # Infiltration not considered during occupied hours
    room(rm).yearly_infiltration_variable(room(rm).yearly_occupancy_variable > 0) = 0.25 # Infiltration not considered during occupied hours
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Infiltration value
    # ------------------

    if infilt_uncertainty == 1
    # If we consider the Infiltration rate variable, then:
       #
    ----------------------------------------------------
    room(rm).infiltration_rate_variable = normrnd(room(rm).infiltration_rate_nominal,room(rm).infiltration_rate_nominal / 5, [value_number 1]); # ACH
    else
    # If Infiltration rate uncertainty is not considered, then:
    # --------------------------------------------------------- \
        room(rm).infiltration_rate_variable = repmat(room(rm).infiltration_rate_nominal, value_number, 1); # ACH
    end
    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    infiltration_rate_nominal = 0;
    yearly_infiltration_nominal = 0;

    infiltration_rate_variable = 0;
    yearly_infiltration_variable = 0;

    # Calculation
    # -----------
    for rm = 1:1:room_num
        # Nominal values \
        # -------------- \
        infiltration_rate_nominal = infiltration_rate_nominal + (room(rm).area * room(rm).infiltration_rate_nominal) / sum(cat(1, room.area));
        yearly_infiltration_nominal = yearly_infiltration_nominal + (room(rm).area * room(rm).yearly_infiltration_nominal) / sum(cat(1, room.area));
    # Variable values \
    # --------------- \
        infiltration_rate_variable = infiltration_rate_variable + (room(rm).area * room(rm).infiltration_rate_variable) / sum(cat(1, room.area));
        yearly_infiltration_variable = yearly_infiltration_variable + (room(rm).area * room(rm).yearly_infiltration_variable) / sum(cat(1, room.area));
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # DHW
    # == ==

    for rm = 1:1:room_num

                     # DHW profile
        # == == == == == =

        # DHW profile follows occupancy \
        # ----------------------------- \
        room(rm).yearly_dhw_nominal = room(rm).yearly_occupancy_nominal
        room(rm).yearly_dhw_variable = room(rm).yearly_occupancy_variable

    # DHW profile for rooms that people sleep in, hence occupied at night, must  be zero during nighttime.For an office building, that is not necessary
    # as the occupancy during these times is equal to zero, hence, the DHW  profile will also be zero.
    # -------------------------------------------------------------------------

    # Nominal profiles
    if room(rm).night_dhw == 1
    for i = 1:365
    if i == 1
    room(rm).yearly_dhw_nominal(i:(wake - 1)) = 0;
    room(rm).yearly_dhw_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0;
    elseif
    i == 365
    room(rm).yearly_dhw_nominal((24 * i - (24 - sleep)):end) = 0;
    else
    room(rm).yearly_dhw_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0;
    end
    end
    end

    # Variable profiles
    if room(rm).night_dhw == 1
    for j = 1:prof_number
    for i = 1:365
    if i == 1
    room(rm).yearly_dhw_variable(i:(wake_var(i, j) - 1), j) = 0;
    room(rm).yearly_dhw_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0;
    elseif
    i == 365
    room(rm).yearly_dhw_variable((24 * i - (24 - sleep_var(i, j))):end, j) = 0;
    else
    room(rm).yearly_dhw_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0;
    end
    end
    end
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # DHW values
    # == == == == ==

    # DHW level(nominal, minimum, maximum) \
    # ------------------------------------- \
    room(rm).dhw_nominal = db2024(room(rm).row, 30) # W / m2
    room(rm).dhw_min = db2024(room(rm).row, 111) # W / m2
    room(rm).dhw_max = db2024(room(rm).row, 112)# W / m2

                                                    # Create triangular distribution \
    # ------------------------------ \
    x0 = [room(rm).dhw_min - 1, room(rm).dhw_max + 1]
    [x, fval, flag] = fsolve( @ (x)my_triang(x, room(rm).dhw_min, room(rm).dhw_max, room(rm).dhw_nominal), x0) # Callsolver

    if flag == -2
    x(1) = room(rm).dhw_min;
    x(2) = room(rm).dhw_max;
    end

    # Sample from triangular distribution
    # -----------------------------------
    if x(1) == x(2) & & x(2) == room(rm).dhw_nominal
    room(rm).dhw_variable = zeros(value_number, 1)
    else
    pd = makedist('Triangular', 'a', x(1), 'b', room(rm).dhw_nominal, 'c', x(2))
    room(rm).dhw_variable = random(pd, value_number, 1)
    room(rm).dhw_variable = round(room(rm).dhw_variable, 1)# round to 1 decimal digit
    en
    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization \
    # -------------- \
    dhw_nominal = 0;
    yearly_dhw_nominal = 0;

    dhw_variable = zeros(prof_number, 1);

    # Calculation
    # -----------
    for rm = 1:1:room_num
                 # Nominal values
    # --------------
    if room(rm).dhw_nominal == 0
    dhw_nominal = dhw_nominal;
    else
    dhw_nominal = dhw_nominal + (room(rm).area * room(rm).dhw_nominal) / sum(cat(1, room.area));
    end
    # Variable values
    # ---------------
    if room(rm).dhw_nominal == 0
    dhw_variable = dhw_variable;
    else
    dhw_variable = dhw_variable + (room(rm).area * room(rm).dhw_variable) / sum(cat(1, room.area));
    end
    end

    for rm = 1:1:room_num
    # Nominalvalues
    # --------------
    if dhw_nominal
    ~ = 0
    yearly_dhw_nominal = yearly_dhw_nominal + room(rm).yearly_dhw_nominal * (
                room(rm).area / sum(cat(1, room.area))) * room(rm).dhw_nominal / dhw_nominal;
    end
    end

    for j = 1:1:prof_number
    yearly_dhw_variable(:, j) = zeros(8760, 1);
    for rm = 1:1:room_num
                 # Variable values
    # ---------------
    if dhw_variable(j)~ = 0:
        yearly_dhw_variable(:, j) = yearly_dhw_variable(:, j) + room(rm).yearly_dhw_variable(:, j) *(room(rm).area / sum(cat(1, room.area))) * room(rm).dhw_variable(j) / dhw_variable(j)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Lighting
    # == == == == =

    for rm = 1:1:room_num

    # Lightingprofile
    # == == == == == == == ==

    # Should the lighting profile follow the occupancy profile? (1 = YES, 0 = NO)
    # ---------------------------------------------------------------------------
    room(rm).Follow_occupancy = db2024(room(rm).row, 113)

    # Initialization of lighting profile \
    # ---------------------------------- \
    room(rm).yearly_lighting_nominal = zeros(8760, 1)
    room(rm).yearly_lighting_variable = zeros(8760, prof_number)

    if room(rm).Follow_occupancy == 1:
        room(rm).yearly_lighting_nominal = room(rm).yearly_occupancy_nominal
        room(rm).yearly_lighting_variable = room(rm).yearly_occupancy_variable
    else:
        room(rm).yearly_lighting_nominal(room(rm).yearly_occupancy_nominal > 0) = 1 * room(rm).yearly_variation_nominal(room(rm).yearly_occupancy_nominal > 0)
        room(rm).yearly_lighting_variable(room(rm).yearly_occupancy_variable > 0) = 1 * room(rm).yearly_variation_variable(room(rm).yearly_occupancy_variable > 0)

    # Correct for weekend days
    # ------------------------
    switch room(rm).ruhetage
    case 1
    room(rm).yearly_lighting_nominal(day_for_each_hour_of_year == 7) = 0
    room(rm).yearly_lighting_variable(day_for_each_hour_of_year == 7,:) = 0
    case 2
    room(rm).yearly_lighting_nominal(day_for_each_hour_of_year == 6) = 0
    room(rm).yearly_lighting_nominal(day_for_each_hour_of_year == 7) = 0
    room(rm).yearly_lighting_variable(day_for_each_hour_of_year == 6,:) = 0
    room(rm).yearly_lighting_variable(day_for_each_hour_of_year == 7,:) = 0

    room(rm).yearly_lighting_variable(room(rm).yearly_lighting_variable > 1) = 1

    # Correct for nighttime lighting
    # ------------------------------
    # Building types that will have the lights off during occupied hours are
    # buildings where people are sleeping.These are: residences, hotels, hospitals.

    # Turn of the lights during night for the building types specified
    # ----------------------------------------------------------------

    # Nominal profiles
    if room(rm).night_light == 1:
        for i = 1:365
            if i == 1:
                room(rm).yearly_lighting_nominal(i:(wake - 1)) = 0
                room(rm).yearly_lighting_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0
            elif i == 365:
                room(rm).yearly_lighting_nominal((24 * i - (24 - sleep)):end) = 0
            else:
                room(rm).yearly_lighting_nominal((24 * i - (24 - sleep)):(24 * i + (wake - 1))) = 0

    # Variable profiles
    if room(rm).night_light == 1:
        for j = 1:1:prof_number
            for i = 1:365
                if i == 1:
                    room(rm).yearly_lighting_variable(i:(wake_var(i, j) - 1), j) = 0
                    room(rm).yearly_lighting_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0
                elif i == 365:
                    room(rm).yearly_lighting_variable((24 * i - (24 - sleep_var(i, j))):end, j) = 0
                else:
                room(rm).yearly_lighting_variable((24 * i - (24 - sleep_var(i, j))):(24 * i + (wake_var(i, j) - 1)), j) = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Lighting setpoint
    # == == == == == == == == =
    room(rm).light_stp_nominal = db2024(room(rm).row, 13) # Use for daylighting

    # If we consider the lighting setpoint variable, then:
    # ---------------------------------------------------------------
    room(rm).light_stp_variable = normrnd(room(rm).light_stp_nominal, room(rm).light_stp_nominal / 10,[value_number 1])

    # If lighting setpoint uncertainty is not considered, then:
    # ---------------------------------------------------------------
    room(rm).light_stp_variable = repmat(room(rm).light_stp_nominal, value_number, 1)

    # Lighting density(nominal, minimum, maximum) \
    # -------------------------------------------- \
    room(rm).light_density_nominal = db2024(room(rm).row, 16) + db2024(room(rm).row, 20) #Use for internal gains and energy consumption
    room(rm).light_density_min = db2024(room(rm).row, 17) + db2024(room(rm).row, 21) # Use for internal gains and energy consumption
    room(rm).light_density_max = db2024(room(rm).row, 18) + + db2024(room(rm).row, 20) # Use for internal gains and energy consumption

    # Create triangular distribution
    # ------------------------------
    x0 =[room(rm).light_density_min - 1, room(rm).light_density_max + 1]
    [x, ~] = fsolve( @ (x)my_triang(x, room(rm).light_density_min, room(rm).light_density_max, room(rm).light_density_nominal), x0) # Call solver

    # Sample from triangular distribution
    # -----------------------------------
    pd = makedist('Triangular', 'a', x(1), 'b', room(rm).light_density_nominal, 'c', x(2));
    room(rm).light_density_variable = random(pd, value_number, 1);
    room(rm).light_density_variable = round(room(rm).light_density_variable, 1); # round to 1 decimal digit

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    end

    # Synthesizing among room types
    # == == == == == == == == == == == == == == =

    # Initialization
    # --------------
    light_density_nominal = 0;
    light_stp_nominal = 0;
    yearly_lighting_nominal = 0;

    light_density_variable = 0;
    light_stp_variable = 0;

    # Calculation
    # -----------
    for rm = 1:1:room_num
                 # Nominalvalues
    # --------------
    if room(rm).light_density_nominal == 0:
        light_density_nominal = light_density_nominal
        light_stp_nominal = light_stp_nominal
    else:
        light_density_nominal = light_density_nominal + (room(rm).area * room(rm).light_density_nominal) / sum(cat(1, room.area))
        light_stp_nominal = light_stp_nominal + (room(rm).area * room(rm).light_stp_nominal) / sum(cat(1, room.area))

    # Variable values
    # ---------------
    if room(rm).light_density_nominal == 0:
        light_density_variable = light_density_variable
        light_stp_variable = light_stp_variable
    else:
        light_density_variable = light_density_variable + (room(rm).area * room(rm).light_density_variable) / sum(cat(1, room.area))
        light_stp_variable = light_stp_variable + (room(rm).area * room(rm).light_stp_variable) / sum(cat(1, room.area))

    for rm = 1:1:room_num
        # Nominal values \
        # -------------- \
        yearly_lighting_nominal = yearly_lighting_nominal + room(rm).yearly_lighting_nominal * (room(rm).area / sum(cat(1, room.area))) * room(rm).light_density_nominal / light_density_nominal

    for j = 1:1:prof_number
        yearly_lighting_variable(:, j) = zeros(8760, 1)
    for rm = 1:1:room_num
        # Variablevalues
        # ---------------
        yearly_lighting_variable(:, j) = yearly_lighting_variable(:, j) + room(rm).yearly_lighting_variable(:, j) *(room(rm).area / sum(cat(1, room.area))) * room(rm).light_density_variable(j) / light_density_variable(j);


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Appliances
    # == == == == == =

    for rm = 1:1:room_num

    # Daily appliances profile
    # == == == == == == == == == == == ==

    # Read nominal profile
    # --------------------
    room(rm).daily_appliances_nominal = db2024(room(rm).row, 57:80) # Profile from SIA 2024

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Add vertical variation
    # == == == == == == == == == == ==

    #Initialization of appliances profile \
    # ------------------------------------ \
    room(rm).yearly_appliances_nominal = zeros(8760, 1)
    room(rm).yearly_appliances_variable = zeros(8760, prof_number)

    # Creation of appliances profile according to monthly nominal and variable schedules
    # ----------------------------------------------------------------------------------
    for i = 1:365
    room(rm).yearly_appliances_nominal((i - 1) * 24 + 1:i * 24) = room(rm).daily_appliances_nominal. * room(
        rm).daily_variation_nominal(i);
    for j = 1:prof_number
    room(rm).yearly_appliances_variable((i - 1) * 24 + 1:i * 24, j) = room(rm).daily_appliances_nominal. * room(
        rm).daily_variation_variable(i, j)

    # Create random values in the range[-vert_var, vert_var] for each hour of each variable hourly appliance usage profile
    # ------------------------------------------------------------------------
    X0 = -vert_var + (vert_var - (-vert_var)) * rand(8760, prof_number)

    # Apply vertical variability to hourly profiles
    # -----------------------------------------------
    room(rm).yearly_appliances_variable = room(rm).yearly_appliances_variable.* (1 + X0)

    # Set yearly_appliances profile minimum to 10 percent and maximum 100 percent
    # -------------------------------------------------------------
    room(rm).yearly_appliances_nominal(room(rm).yearly_appliances_nominal < 0.1) = 0.10
    room(rm).yearly_appliances_variable(room(rm).yearly_appliances_variable < 0.1) = 0.10
    room(rm).yearly_appliances_nominal(room(rm).yearly_appliances_nominal > 1) = 1
    room(rm).yearly_appliances_variable(room(rm).yearly_appliances_variable > 1) = 1

    # Check for weekends
    # ------------------
    switch room(rm).ruhetage
    case 1
    room(rm).yearly_appliances_nominal(day_for_each_hour_of_year == 7) = 0.10;
    room(rm).yearly_appliances_variable(day_for_each_hour_of_year == 7) = 0.10;
    case 2
    room(rm).yearly_appliances_nominal(day_for_each_hour_of_year == 6) = 0.10;
    room(rm).yearly_appliances_nominal(day_for_each_hour_of_year == 7) = 0.10;
    room(rm).yearly_appliances_variable(day_for_each_hour_of_year == 6) = 0.10;
    room(rm).yearly_appliances_variable(day_for_each_hour_of_year == 7) = 0.10;
    end

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Add horizontal variability to the appliances profiles
    # == == == == == == == == == == == == == == == == == == == == == == == == == =
    room(rm).yearly_appliances_variable = horizontal_variability(room(rm).yearly_appliances_variable, room(rm).appliance_breaks);

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Appliances level value (nominal, minimum, maximum)
    # --------------------------------------------------
    room(rm).appliances_level_nominal = db2024(room(rm).row, 6) # W / m2  ** ** ** ** ** **
    room(rm).appliances_level_min = db2024(room(rm).row, 7) # W / m2  ** ** ** ** ** **
    room(rm).appliances_level_max = db2024(room(rm).row, 8) # W / m2  ** ** ** ** ** **

    # Create triangular distribution
    # ------------------------------
    x0 =[room(rm).appliances_level_min - 1, room(rm).appliances_level_max + 1];
    [x, ~] = fsolve( @ (x)my_triang(x, room(rm).appliances_level_min, room(rm).appliances_level_max, room(rm).appliances_level_nominal), x0) # Call solver

    # Sample from triangular distribution
    # -----------------------------------
    pd = makedist('Triangular', 'a', x(1), 'b', room(rm).appliances_level_nominal, 'c', x(2));
    room(rm).appliances_level_variable = random(pd, value_number, 1);
    room(rm).appliances_level_variable = round(room(rm).appliances_level_variable, 1) # round to 1 decimal digit

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
    if room(rm).appliances_level_nominal == 0:
        appliances_level_nominal = appliances_level_nominal
    else:
        appliances_level_nominal = appliances_level_nominal + (room(rm).area * room(rm).appliances_level_nominal) / sum(cat(1, room.area))
    # Variable values
    # ---------------
    if room(rm).appliances_level_nominal == 0:
        appliances_level_variable = appliances_level_variable
    else:
        appliances_level_variable = appliances_level_variable + (room(rm).area * room(rm).appliances_level_variable) / sum(cat(1, room.area))

    for rm in range(0,room_num):
        # Nominal values
        # --------------
        if appliances_level_nominal~ = 0:
             yearly_appliances_nominal = yearly_appliances_nominal + room(rm).yearly_appliances_nominal * (room(rm).area / sum(cat(1, room.area))) * room(rm).appliances_level_nominal / appliances_level_nominal

    for j = 1:1:prof_number
    yearly_appliances_variable(:, j) = zeros(8760, 1)
    for rm = 1:1:room_num # Variable values
    # ---------------
    if appliances_level_variable(j)~ = 0:
    yearly_appliances_variable(:, j) = yearly_appliances_variable(:, j) + room(rm).yearly_appliances_variable(:, j) *(room(rm).area / sum(cat(1,room.area))) * room(rm).appliances_level_variable(j) / appliances_level_variable(j);

    # Correction if appliances schedule exceeds 1
    yearly_appliances_variable(yearly_appliances_variable > 1) = 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Final report nominal values
    # == == == == == == == == == == == == == ==

    # Write scalar values
    # == == == == == == == == == =
    if variable_schedules == 'variable': # if only nominal schedules should be generated
        Explanations = {'This factor (m2/person) is used, along with the Zone Floor Area to determine the maximum number of people as described in the Number of People field. The choice from the method field should be Area/Person', ...
        'The heating setpoint temperature in degrees C if constant throughout the year. If the previous field is used this field should be left blank and will be ignored', ...
        'The cooling setpoint temperature in degrees C if constant throughout the year. If the previous field is used this field should be left blank and will be ignored', ...
        'The design outdoor air volume flow rate per person (m3/s/m2). This input is used if Outdoor Air Method is Flow/Area. The default value for this field is 0', ...
        'This factor (ACH) is used to determine the maximum Design Flow Rate as described in the Design Flow Rate field. The choice from the method field should be AirChanges/Hour', ...
        'This factor (watts/m2) is used, along with the Zone Area to determine the maximum equipment level as described in the Design Level field. The choice from the method field should be Watts/Area', ...
        'This factor (watts/m2) is used, along with the Zone Floor Area to determine the maximum lighting level as described in the Lighting Level field. The choice from the method field should be Watts/Area', ...
        'The desired lighting level (in lux) at the First Reference Point. This is the lighting level that would be produced at this reference point at night if the overhead electric lighting were operating at full input power. Recommended values depend on type of activity', ...
        'This factor (watts/m2) is used, along with the Zone Area to determine the maximum equipment level as described in the Design Level field. The choice from the method field should be Watts/Area'};

        C = {area_per_person_nominal 'm2/P' Explanations(1);...
        therm_h_nominal 'degrees C' Explanations(2);...
        therm_c_nominal 'degrees C' Explanations(3);...
        ventilation_nominal 'm3/(m2s)' Explanations(4);...
        infiltration_rate_nominal 'ACH' Explanations(5);...
        dhw_nominal 'W/m2' Explanations(6);...
        light_density_nominal 'W/m2' Explanations(7);...
        light_stp_nominal 'lux' Explanations(8);...
        appliances_level_nominal 'W/m2' Explanations(9)};

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

