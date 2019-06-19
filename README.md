The CESAR (CombinedEnergySimulationAndRetrofitting) – Tool consists of two main parts, the
Demand Modelling (DM) and the Retrofit Modelling (RM). The DM processes the
building related information (Geometry, Building Usage and Building Envelope Constructions) into
EnergyPlus input-files which are then simulated with the specified weather file. The complete process
is fully automated and requires the Building footprints and certain information about the
building like Energy Systems, Building Age, building geometry, commune/gemeinde number in Switzerland (for weather file assignment) etc., as inputs. Based on this information, and EnergyPlus IDF file is created in order to simulate the loads of the building (Electricity, heating demand, and cooling demand).

When a group of buildings is considered, shading of nearby buildings on each other is considered.

The construction, energy carrier information, and retrofit information as well as the CO2 values are based on the Swiss Building Stock. Although the tool can be used in theory in any location, the constructions and retrofit information and the building schedule information are based on SIA standards.

Building geometry is based on the swisstopo building models in GIS. The coordinates of the vertices (X,Y,Height) buildings of interest can be exported from GIS and imported into the model. The glazing ratio can be user defined, or suggested values are based on building age for typical Swiss buildings.

The RM provides several predefined retrofit strategies that can be applied on a district simulated by
the DM to assess energy and emission saving potentials. Several envelope options can be used to simulate building retrofit improvements. The simulation will first simulate the base case without retrofit, and then the user can select which of the following elements can be retrofitted: facade, ground (basements are currently not considered due to lack of information), windows, and roof. The user can also select whether to choose the SIA target (Zielwerte) U-values or the minimum (Grenzwerte) U-Values for retrofit. In addition, two different retrofit rates are used from the Swiss Energy Strategy: a Business as Usual (BAU) and a New Energy Policy (NEP) with the NEP's rate being approximitly twice that of the BAU.

The simulation will also calculate the total retrofit costs and building material embodied emissions (which can be later used in an optimization model).  The predefined strategies are based on the Swiss Energy Strategy 2050 (Prognos AG, 2012) but the user interface and the modularity of the tool allows for easy setup and assessment of own strategies. The RM takes retrofitting rates, system transformations as well as system developments into account, which are then applied on the selected district.
In addition, the CESAR-Tool allows to account for climate change by running the buildings IDF files
with weather files from different climate change scenarios and GHG concentration pathways.
