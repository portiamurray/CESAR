def SetRunFolder(project_directory,charproject_name):
    import os
    os.mkdir(project_directory+charproject_name)
    projectpath=project_directory+charproject_name
    #Create project directories
    os.mkdir(projectpath + '/01_EnergyPlus_Input')  # EnergyPlus Input Textfiles
    os.mkdir(projectpath + '/02_EnergyPlus_Output')  # EnergyPlus Output Textfiles
    os.mkdir(projectpath + '/03_Results')  # EnergyPlus Summary Output Textfiles
    os.mkdir(projectpath + '/04_Variability_Information')  # Variability information database
    os.mkdir(projectpath + '/05_SimulationSetup')  # Run EnergyPlus Setup Storage
    os.mkdir(projectpath + '/06_Schedule_Parameter_Files') # Schedule & Parameter files
    os.mkdir(projectpath + '/07_arcGIS_Input') #GIS Input files
    os.mkdir(projectpath + '/08_BuildingGeometry')  # Building geometry textfiles
    #Create Paths for Data Handling
    arcgispath=projectpath +'/07_arcGIS_Input/' # path to geometry files
    geometrypath=projectpath + '/' + '08_BuildingGeometry/' # path to geometry files
    eplusinputpath=projectpath + '/' + '01_EnergyPlus_Input/' # path to energy plus input (job files, idf)
    eplusoutputpath=projectpath + '/' + '02_EnergyPlus_Output/' # path to energy plus output files
    resultsummarypath=projectpath + '/' + '03_Results/' # path to energy plus output files
    variabilitypath=projectpath + '/' + '04_Variability_Information/' # path to energy plus output files
    schedulepath=projectpath + '/' + '06_Schedule_Parameter_Files/' # path to schedule files
    runepluspath=projectpath + '/' + '05_SimulationSetup/' # path to energy plus run files

    # Create SubPaths for EnergyPlus Output Files
    #result_basepath=eplusoutputpath; repetative, removed
    os.mkdir(eplusoutputpath +'01_HourlyZnAgg')
    os.mkdir(eplusoutputpath +'02_HourlyZnSpec')
    os.mkdir(eplusoutputpath +'03_HtmlReport')
    os.mkdir(eplusoutputpath +'04_ErrorFiles')
    eplusout_hrznagg=eplusoutputpath + '01_HourlyZnAgg/'
    eplusout_hrznspec=eplusoutputpath + '02_HourlyZnSpec/'
    eplusout_htmlrep=eplusoutputpath + '03_HtmlReport/'
    eplusout_errfiles=eplusoutputpath +'04_ErrorFiles/'
    return [arcgispath,geometrypath,eplusinputpath,eplusoutputpath,resultsummarypath,variabilitypath,schedulepath,runepluspath,eplusout_hrznagg,eplusout_hrznspec,eplusout_htmlrep,eplusout_errfiles]