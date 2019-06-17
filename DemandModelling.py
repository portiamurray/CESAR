import pandas as pd
import numpy as np
import os
from shutil import copyfile
from  UserSettings import SetRunFolder
from RetrofitType import SetRetrofitFiles
from buildings import ProcessCoordinates
from buildings import BuildingsCenter
from buildings import BuildingsNeigh
from buildings import BuildingsAdjacence
from ScheduleGeneration import CESAR_function_Variability_case_multiroom_selection

core_selection=1 # One simulation or two in parallel? either 1 or 2
variable_schedules='variable'# Either 'variable' or 'nominal'
project_directory=r'/Users/portia_murray/Desktop/03_CESAR_Tool_the_15022018_PM/' #Project directory on your computer where the '03_CESAR_Tool_the_15022018' folder is located.  CHECK FOR SPACES LATER
arcgis_simbuildings=r'/Users/portia_murray/Desktop/03_CESAR_Tool_the_15022018_PM/05_TestCase/00_ArcGIS_InputFiles/BuildingInformation.csv' #Path to the age and heating system  building information
arcgis_sitefile=r'/Users/portia_murray/Desktop/03_CESAR_Tool_the_15022018_PM/05_TestCase/00_ArcGIS_InputFiles/SiteVertices.csv' #Path to the building geometry information
RetrofitClass='Tar' # Either target U-values or minimum U-values for retrofits
cixed_classes='F' # Either 'Variable' or 'Fixed' constructions
glratethreshold=100 # Maximum glazing ratio
r=50 # Shading distance from other buildings, default value should be 50
bldtype=['EFH','MFH','Office','Restaurant','Hospital','School','Shop'] # building type
externalinput_path=project_directory+'00_ExternalInput/' #Path to external imput
bldspecglzrate_selection=0 # 0 if building specific glazing ratio is unknown, 1 if known (assigned in building information file by user)
initpath=externalinput_path+'02_RetrofitInputFiles/03_RetrofitConstruction/'#Set path for retrofit constuctions
useExistingSchedule=0
buildtype=0
reret='N' # Do you want the building to be retrofitted? Yes or no?
charproject_name='Offices_wallTar' # Name of folder in which your results will be stored
groundRet='N' # Do you want the ground/basement to be retrofitted? Yes or no?
wallRet='N' # Do you want the facade/wall to be retrofitted? Yes or no?
winRet='N' # Do you want the window to be retrofitted? Yes or no?
roofRet='N' # Do you want the roof to be retrofitted? Yes or no?
eplus_c1=project_directory+'02_EnergyPlusInstallations/EnergyPlusV8-5-c1/'#Path for the first energy plus installation
eplus_c2=project_directory+'02_EnergyPlusInstallations/EnergyPlusV8-5-c2/'#Path for the second energyplus installation
infrate=0.7 # Infiltration rate
r_glaz=15 # Glazing ratio
useExistingSchedules=0 #if 1, use existing schedules. Probably redundant, try to remove later
output_parameters=1 #PROBABLY REDUNDANT, REMOVE LATER
#Create run folder
[arcgispath,geometrypath,eplusinputpath,eplusoutputpath,resultsummarypath,variabilitypath,schedulepath,runepluspath,eplusout_hrznagg,eplusout_hrznspec,eplusout_htmlrep,eplusout_errfiles] = SetRunFolder(project_directory,charproject_name)

[retinputpath,RetType]=SetRetrofitFiles(RetrofitClass,externalinput_path,reret,wallRet,winRet,roofRet,groundRet)

glazingratiopath=externalinput_path +'/00_GeneralData/'
# define the path to the standard infiltration rate
infratepath=externalinput_path + '/00_GeneralData/'
print('--------->   Step 0: Import building coordinate and information files    <---------')
# call input points as building footprint vertices(raw data from ArcGIS)
# for all the buildings at the analysis site (incl. shading objects!)
# with the following information:
# points(Building Number,Original FID, Height, X_Coordinate, Y_Coordinate

# choose file to open (building vertices and information)
points = pd.read_csv(arcgis_sitefile) # read the CSV, starting from row 1 and column 0 (dont read the header of the csv)
copyfile(arcgis_sitefile,arcgispath+'SiteVertices.csv') # copy the file to the Project Folder to keep it for later simulations

# Step 1 - Select Simulation Buildings
print('--------->   Step 1: Select Simulation Buildings   <---------')

# call the file containing information about the buildings to be simulated
# Information (in this order):
# Original FID, Building Type, Construction Age, Last
# Retrofit Year, Ground Floor Area, Energy Carrier Heating, Energy Carrier DHW

sim_buildings = pd.read_csv(arcgis_simbuildings) # read the CSV, starting from row 1 and column 0 (dont read the header of the csv)
orig_fid=sim_buildings.loc[:,'ORIG_FID'] # original fid (ArcGIS)
bldng_type=sim_buildings.loc[:,'BuildingType'] # building type: 1 = resi, 2 = office, 3 = Industry
constr_age=sim_buildings.loc[:,'BuildingAge'] # construction age of the building
rtrft_age=sim_buildings.loc[:,'LastRetrofit'] # last retrofit year
grnd_flr_area=sim_buildings.loc[:,'GroundFloorArea'] # gound floor area of each building for postprocessing
energy_sh=sim_buildings.loc[:,'ECarrierHeating'] # energy carrier space heating
energy_dhw=sim_buildings.loc[:,'ECarrierDHW'] # energy carrier dhw

if bldspecglzrate_selection==1: #if building specific glazing rate is selected
    bld_spec_glzrate=sim_buildings.loc[:,'GlazingRatio'] # building specific glazing rate (window to wall ratio)

gmde_weather=sim_buildings.loc[:,'GDE-Number'] # Gemeinde number in order to assign weather file based on location
copyfile(arcgis_simbuildings,arcgispath+'BuildingInformation.csv')

# Step 2 - Create Buildings & Neigbourhood

# Assign the vertexes to the buildings and neighbourhood and create the
# buildings database and neighbourhood database

# Step 2.0 - Create the buildings database
print('--------->   Step 2.0: Create the buildings database   <---------')
[building,n_building,resid_id] = ProcessCoordinates(points,orig_fid)

# Step 2.1 - Create Center Buildings
print('--------->   Step 2.1: Create Center Buildings   <---------')
# set selfcentered coordinates for each center building (simulated building)
[ building_center ] = BuildingsCenter( building,n_building )

# Step 2.2 - Create Neighbourhood of Center buildings
print('--------->   Step 2.2: Create Neighbourhood of Center buildings   <---------')
if r>0: #If the shading radius is larger than zero, do you want neighbour buildings to be considered as shading objects
    # run 'buildings_neigh' function
    [building_neigh, building_neighnum] = BuildingsNeigh(building,n_building,r)
else:
    #set neighbour buildings to empty cells
    building_neigh={} # corresponding neighbour building vertex set from the origin
    building_neighnum={} # corresponding building number
    building_neighnum={} # corresponding building number

# Step 2.4 - Check for Adjacence
print('--------->   Step 2.4: Check for Adjacence   <---------')
adjacence_inf = BuildingsAdjacence( building,n_building)

# Step 3 - Create the idf files

# Loop through all the simulated buildings and create the idf files

# Step 3.1 - Prepare for loop through buildings
print('--------->   Step 3.0: Prepare for loop through buildings   <---------')
n_id=len(resid_id) # number of buildings that are simulated

# Step 3.1 - Output Variables Preparation
print('--------->   Step 3.1: Output Variables Preparation   <---------')
n_floor_all=np.zeros(n_id) # generate a matrix with informations about the number of floors
x_ageclass_all=np.zeros(n_id) # generate a matrix that contains the age class of every building
all_variable_values=np.zeros(n_id) # all variable values that contain information about the used schedules and setpoints, in total 17, for every building
statusquoinf={} #cell(n_id,32) # matrix that will contain the status quo informations

# Step 3.2 - GENERATING THE VARIABLE / Non-Variable SCHEDULES & Save them
print('--------->   Step 3.2: Generate the variable or non-nariable schedules and save them  <---------')
bldg=bldtype[buildtype]
if useExistingSchedules == 0:
    if variable_schedules == 1: # if variable schedules should be used
        if n_id<=100: # if the number of simulated buildings is smaller than 100, generate only as many variants as buildings exist
            prof_nr=n_id # number of profiles that should be generated
            value_nr=n_id # number of values that should be generated
            CESAR_function_Variability_case_multiroom_selection(prof_nr,value_nr,variable_schedules,schedulepath,bldg) # Call schedule generation function
        else:
            # generate 100 variants and assign them randomly to the buildings
            prof_nr=100 # number of profiles that should be generated
            value_nr=100 # number of values that should be generated
            CESAR_function_Variability_case_multiroom_selection(prof_nr,value_nr,variable_schedules,schedulepath,bldg) # Call schedule generation function

        # -------------------- READ THE GENERATED PARAMETER FILES -------------------------
        # reading all the variable value files --> later used for variable schedules and variability
        appliances_value = pd.read_csv(schedulepath + bldtype[buildtype] + '_appliances_level_variable.csv') # read the appliances setpoint values
        dhw_demand = pd.read_csv(schedulepath + bldtype[buildtype] +'_dhw_variable.csv') # read the domestic hot water demand values
        light_density = pd.read_csv(schedulepath,bldtype[buildtype] + '_light_density_variable.csv') # read the light density values
        outside_airflow = pd.read_csv(schedulepath,bldtype[buildtype] +'_ventilation_rate_variable.csv') # read the outside airflow values
        area_pperson = pd.read_csv(schedulepath,bldtype[buildtype]+ '_area_per_person_variable.csv') # read the area per person values
        # generate the indicator that this is variable case
        variable_case='variable' # is used in idf_writer5_schedules
    else:    # if no variable values are required
        prof_nr=1 # number of profiles that should be generated
        value_nr=1 # number of values that should be generated
        CESAR_function_Variability_case_multiroom_selection(prof_nr,value_nr,variable_schedules,schedulepath,bldg)
         # -------------------- READ THE GENERATED PARAMETER FILES -------------------------
        # reading all the variable value files --> later used for variable schedules and variability
        variable_values=pd.read_excel(schedulepath + bldtype[buildtype] + '_summary.xlsx','Sheet1',usecols='B')
        appliances_value = variable_values.loc[8,'Value'] # read the nominal appliances setpoint values
        dhw_demand = variable_values.loc[5,'Value'] # read the domestic hot water demand values
        light_density = variable_values.loc[6,'Value']  # read the light density values
        outside_airflow =  variable_values.loc[3,'Value'] # read the outside airflow values
        area_pperson = variable_values.loc[0,'Value'] # read the area per person values
        variable_case='nominal' # is used in idf_writer5_schedules
else:
    baseCaseSchedulePath = project_directory +'/' + charproject_name + '/06_Schedule_Parameter_Files/'
    if variable_schedules == 'variable': # if variable schedules should be used
        appliances_value = pd.read_csv(schedulepath + bldtype[buildtype] + '_appliances_level_variable.csv') # read the appliances setpoint values
        dhw_demand = pd.read_csv(schedulepath + bldtype[buildtype] +'_dhw_variable.csv') # read the domestic hot water demand values
        light_density = pd.read_csv(schedulepath,bldtype[buildtype] + '_light_density_variable.csv') # read the light density values
        outside_airflow = pd.read_csv(schedulepath,bldtype[buildtype] +'_ventilation_rate_variable.csv') # read the outside airflow values
        area_pperson = pd.read_csv(schedulepath,bldtype[buildtype]+ '_area_per_person_variable.csv') # read the area per person values
        # generate the indicator that this is variable case
        variable_case='variable' # is used in idf_writer5_schedules
    else:
        variable_values=pd.read_excel(schedulepath + bldtype[buildtype] + '_summary.xlsx','Sheet1',usecols='B')
        appliances_value = variable_values.loc[8,'Value'] # read the nominal appliances setpoint values
        dhw_demand = variable_values.loc[5,'Value'] # read the domestic hot water demand values
        light_density = variable_values.loc[6,'Value']  # read the light density values
        outside_airflow =  variable_values.loc[3,'Value'] # read the outside airflow values
        area_pperson = variable_values.loc[0,'Value'] # read the area per person values
        variable_case='nominal' # is used in idf_writer5_schedules