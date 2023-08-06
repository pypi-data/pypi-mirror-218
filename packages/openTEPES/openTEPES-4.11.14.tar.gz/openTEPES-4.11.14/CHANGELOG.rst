Change Log
=============

[4.11.14] - 2023-07-08
----------------------
- [FIXED] simplify input data and fix division by zero in output results
- [FIXED] several fixes in input data, model formulation, problem solving, and output results modules
- [FIXED] fix output of investment results
- [FIXED] reorganize the balance equation to avoid negative dual variables
- [CHANGED] NetworkCommitment file only if needed
- [CHANGED] Computation of problem size
- [FIXED] fixed vMaxCommitment in input data
- [FIXED] fixed vLineOnState and vLineOffState in input data for all the lines
- [CHANGED] add problem size in log file

[4.11.13] - 2023-06-18
----------------------
- [FIXED] fixed error in marginals of adequacy constraints
- [FIXED] fixed error in output results

[4.11.12] - 2023-06-12
----------------------
- [FIXED] fixed error in writing technology emission file of output results

[4.11.11] - 2023-06-08
----------------------
- [CHANGED] performance issues in input data and model formulation

[4.11.10] - 2023-06-06
----------------------
- [CHANGED] performance issues in input data
- [CHANGED] clean up the scaling of the output results

[4.11.9] - 2023-05-30
---------------------
- [CHANGED] avoid the repeated computation of modulo function with n
- [FIXED] fix error in output results
- [FIXED] fix computation of MarginalIncrementalGenerator output file

[4.11.8] - 2023-05-29
---------------------
- [CHANGED] introduce some dictionaries to avoid unnecessary computations
- [CHANGED] change name mTEPES.r to mTEPES.re
- [CHANGED] simplify some set combinations to reduce computation time

[4.11.7] - 2023-05-17
---------------------
- [CHANGED] reorganizing the ifs in model formulation

[4.11.6] - 2023-05-15
---------------------
- [CHANGED] adapt figures to altair 5.0.0

[4.11.5] - 2023-05-13
---------------------
- [CHANGED] fix some typos

[4.11.3] - 2023-04-11
---------------------
- [CHANGED] change boolean to binary parameters
- [CHANGED] get dual variables for each solved problem

[4.11.2] - 2023-04-07
---------------------
- [CHANGED] avoid formulation of period/scenario not solved

[4.11.1] - 2023-03-31
---------------------
- [FIXED] reorganize the problem solving by period
- [FIXED] split formulation by period and scenario

[4.11.0] - 2023-03-28
---------------------
- [CHANGED] if no investment decisions all the scenarios with probability > 0 area solved sequentially
- [CHANGED] new VariableFuelCost input data file

[4.10.6] - 2023-03-21
---------------------
- [FIXED] fix a typo in the generation unit investment file

[4.10.5] - 2023-03-17
---------------------
- [FIXED] fix a typo in the generation unit investment file
- [FIXED] fix a typo in the name of the technology energy plot
- [FIXED] fix a typo in generation operation output results

[4.10.4] - 2023-03-15
---------------------
- [CHANGED] allow negative CO2 emission rate for biomass units

[4.10.3] - 2023-03-10
---------------------
- [CHANGED] introduce incompatibility constraint between charge and outflows use

[4.10.2] - 2023-03-09
---------------------
- [CHANGED] introduce incompatibility constraint between charge and outflows use
- [CHANGED] introduce conditions to avoid doing unnecessary computations in input data
- [CHANGED] introduce indicators to allow selecting output results

[4.10.1] - 2023-02-27
---------------------
- [FIXED] typo in writing ESS operation results
- [FIXED] typo in control of minimum energy infeasibility

[4.10.0] - 2023-02-15
---------------------
- [CHANGED] introduce control of minimum energy infeasibility
- [CHANGED] scale eMaxInventory2Comm, eMinInventory2Comm, and eInflows2Comm constraints
- [FIXED] force time step cycle for ESS inventory scheduling to be integer
- [FIXED] eliminate production and operating reserve variables if there is no pumping capability and no natural inflows
- [FIXED] fix error in determining the storage cycle of every ESS unit (as the minimum value between storage type, outflows type, and energy type) only if values of outflows and energy are provided
- [CHANGED] new VariableMaxEnergy and VariableMinEnergy input data files to determine mandatory max or min energy in time interval defined by EnergyType column in Generation file

[4.9.1] - 2023-01-18
--------------------
- [CHANGED] new TechnologyConsumptionEnergy output file
- [CHANGED] change some column headings in some output files
- [FIXED] fix error in the values of MWkm output results

[4.9.0] - 2023-01-12
--------------------
- [FIXED] fix error when writing NetworkInvestment and NetworkInvestment_MWkm output files
- [CHANGED] fix inventory to the lower bound instead of 0 to avoid warnings
- [CHANGED] print infeasibilities to a file
- [CHANGED] if investment/retirement lower and upper bounds are close to 0 or 1, make them 0 or 1
- [CHANGED] add two new network energy flow files per area and total
- [CHANGED] add two new energy balance files per area and technology
- [FIXED] fix ESS inventory constraint to include ESS candidate and existing units
- [FIXED] fix constraint of energy inflows management for the case of candidate ESS units
- [FIXED] add StorageInvestment option in Generation file to link the storage capacity and inflows to the investment decision
- [FIXED] add constraints related to the previous option

[4.8.5] - 2022-12-06
--------------------
- [CHANGED] fix some warning on input data module
- [FIXED] fix relation between generation investment and total charge
- [FIXED] change some future warnings and fix generation investment for ESS

[4.8.4] - 2022-12-01
--------------------
- [CHANGED] scenario probabilities declared as float
- [FIXED] control of inventory at the end of each stage and initial inventory fixed, but only if they are between limits
- [FIXED] error in declaring the parameter scenario probabilities
- [FIXED] avoid writing results for areas with no generation nor demand
- [FIXED] fix some errors in the use of dynamic sets in output results and other modules
- [CHANGED] extensive use of dynamic sets in several modules
- [CHANGED] modify output results to avoid the dynamic activation of the load levels depending on the stage
- [CHANGED] modify input data and output results to clean up the use of aggregated sets
- [CHANGED] modify output results to reduce printing time

[4.8.3] - 2022-11-07
--------------------
- [FIXED] fix typo in assign duration 0 to load levels not being considered
- [CHANGED] added new output files

[4.8.2] - 2022-10-27
--------------------
- [FIXED] fix computation of the demand when there are negative demands
- [CHANGED] avoid a second run of the model if no binary variables are in it
- [CHANGED] improve the computation of some double sets
- [CHANGED] change names of output files from charge to consumption
- [FIXED] protect against division by zero in output results
- [FIXED] fix computation of ESS invested capacity when the unit has no power, but charge
- [CHANGED] change computation of node and line to area sets
- [FIXED] fix an error in balance between output of the ESS and outflows
- [FIXED] fix an error fixing values of storage with outflows
- [CHANGED] fix typo in error message about input data
- [CHANGED] add file for spillage by technology TechnologySpillage
- [FIXED] fix some errors in OutputResults
- [CHANGED] avoid formulation of storage variables and equations with no generation and consumption power
- [FIXED] fix error in output results
- [CHANGED] introduction of a base year in Data_Parameter file for all the economic parameters being affected by the discount rate
- [FIXED] fix error in eTotalTCost constraint
- [FIXED] fix some errors in output results

[4.7.1] - 2022-08-01
--------------------
- [CHANGED] modify the definition of vMaxCommitment
- [CHANGED] add some KPIs, LCOE and net demand in output results
- [FIXED] fix error in operation cost
- [FIXED] fix error in vMaxCommitment
- [FIXED] fix eInstalGenCap and eUninstalGenCap
- [FIXED] fix detection of ESS units with no inflows
- [CHANGED] introduction of lower and upper bounds in investment and retirement decisions for network and generation

[4.6.1] - 2022-06-15
--------------------
- [CHANGED] addition of two new result files for percentage of spillage by generator and technology
- [FIXED] fix error in outflows equation
- [FIXED] fix some typos in input data
- [FIXED] fix error related to initial and final periods
- [CHANGED] addition of two new result files for percentage of energy curtailed by generator and technology
- [FIXED] error in the ramp up equation for the charge onf an ESS (eRampUpCharge)
- [CHANGED] introduce generation/demand balance energy result
- [FIXED] error in the generation/demand balance file

[4.6.0] - 2022-05-19
--------------------
- [CHANGED] introduce generation/demand balance output result
- [CHANGED] allow scenarios defined with 0 probability
- [CHANGED] avoid division by 0 in network utilization
- [CHANGED] avoid values of BigM = 0.0
- [CHANGED] change modeling of negative reactances
- [CHANGED] introduce maximum shifting time for DSM

[4.5.2] - 2022-04-25
--------------------
- [CHANGED] combine load level weight and duration
- [CHANGED] combine period weight and probability
- [CHANGED] fix some typos in cost summary
- [CHANGED] introduce annual discount rate to move money along the time
- [FIXED] control of non-negative values of some input data
- [CHANGED] avoid fixing voltage angle for the reference node with single node option

[4.5.1] - 2022-03-25
--------------------
- [CHANGED] split the objective function and investment constraints in two scripts

[4.5.0] - 2022-03-20
--------------------
- [CHANGED] introduce initial and final period for each generator/line. The periods must be non-negative integers
- [CHANGED] define the scenario probability of each period.
- [CHANGED] introduce changes to allow multiperiod cases.
- [CHANGED] introduce some infeasibility detection.
- [CHANGED] additional control on definition of ESS units.
- [CHANGED] exchange the order of scenario and period to do dynamic expansion planning.

[4.4.0] - 2022-03-11
--------------------
- [CHANGED] introduce options for deactivating the up/down ramp constraints and the minimum up/down time constraints.
- [CHANGED] introduce a single-node option for running a case study as a single node (no network constraints).
- [CHANGED] new option value 2 for IndBinGenInvest, IndBinGenRetirement, IndBinNetInvest for ignoring the investment/retirement decisions.
- [CHANGED] re-group the generation operation constraints by topics in separate functions.
- [CHANGED] change some names of output results to organize them by topics.

[4.3.7] - 2022-02-28
--------------------
- [CHANGED] saving new results about incremental generator 'oT_Result_IncrementalGenerator_'+CaseName+'.csv'.
- [CHANGED] saving new results about incremental emission of generators with surplus 'oT_Result_GenerationIncrementalEmission_'+CaseName+'.csv'.
- [CHANGED] saving new results about generation ramp surplus in 'oT_Result_GenerationRampUpSurplus_'+CaseName+'.csv' and 'oT_Result_GenerationRampDwSurplus_'+CaseName+'.csv'.
- [CHANGED] saving new results about generation surplus in 'oT_Result_GenerationSurplus_'+CaseName+'.csv'.
- [CHANGED] saving new results about incremental variable cost of generators with surplus in 'oT_Result_GenerationIncrementalVariableCost_'+CaseName+'.csv'.

[4.3.6] - 2022-02-09
--------------------
- [CHANGED] change of domain of some p.u. parameters to UnitInterval and others to Reals
- [CHANGED] change output of units not contributing to operating reserves
- [CHANGED] change on the assessment of the termination condition

[4.3.5] - 2022-01-29
--------------------
- [FIXED] detect ESS that only pump/charge
- [FIXED] exclude contribution to operating reserves of units with NoOperatingReserves=yes
- [FIXED] fix computation of dual variables of operating reserves

[4.3.4] - 2022-01-27
--------------------
- [FIXED] fix computation of log console option

[4.3.3] - 2022-01-25
--------------------
- [CHANGED] Permanent presence of the solver log file
- [CHANGED] LP-file writing depends of the pIndLogConsole

[4.3.2] - 2022-01-24
--------------------
- [FIXED] Append function updated to cumulate all stages before plotting the LSRMC
- [CHANGED] Condition updated in ProblemSolving to use Gurobi or Mosek 

[4.3.2] - 2022-01-24 - release candidate
--------------------
- [FIXED] Legend in nodes in the network map
- [CHANGED] Use of the CBC as a recommended solver instead of GLPK
- [CHANGED] Adding pIndLogConsole in openTEPES_ProblemSolving.py

[4.3.1] - 2022-01-19
--------------------
- [CHANGED] improved network map representation in html
- [CHANGED] console log as option in input data

[4.3.0] - 2021-12-31
--------------------
- [CHANGED] improved representation of operating reserves

[4.2.4] - 2021-12-30
--------------------
- [FIXED] inertia constraints
- [FIXED] typos in output results
- [CHANGED] introduce html plots based on Altair

[4.2.3] - 2021-12-17
--------------------
- [FIXED] plots associated to ESS technologies

[4.2.2] - 2021-12-08
--------------------
- [FIXED] assessment of the locational short-run marginal costs

[4.2.1] - 2021-12-01
--------------------
- [FIXED] assessment of the locational short-run marginal costs

[4.2.0] - 2021-11-11
--------------------
- [CHANGED] introduction of a retirement cost to allow retirement decisions
- [CHANGED] elimination of line switching states

[4.1.3] - 2021-10-31
--------------------
- [FIXED] Generalization of the maximum commitment and mutually exclusive constraints

[4.1.2] - 2021-10-28
--------------------
- [FIXED] Removing option when the solver is called in ProblemSolving

[4.1.1] - 2021-10-27
--------------------
- [FIXED] adding mutually exclusive formulation for ESS, add output results of reserve margin

[4.1.0] - 2021-10-22
--------------------
- [CHANGED] introduction of mutually exclusive generator in generation file
- [CHANGED] Using TimeStep of 4 instead of 2 in Cases 9n and sSEP to speed-up the packaging tests

[3.1.5] - 2021-10-15
--------------------
- [FIXED] fix magnitude of the emission output

[3.1.4] - 2021-09-30
--------------------
- [FIXED] fix initialization of synchronous condenser and shunt candidate

[3.1.3] - 2021-09-10
--------------------
- [FIXED] fix in some equations the activation of the operating reserves

[3.1.2] - 2021-07-12
--------------------
- [FIXED] fix typo in network investment constraint to include candidate lines

[3.1.1] - 2021-07-08
--------------------
- [FIXED] change location of lea and lca computation

[3.1.0] - 2021-07-07
--------------------
- [CHANGED] definition of switching stages with dict and data files to allow less granularity in switching decisions

[2.6.5] - 2021-07-04
--------------------
- [FIXED] typos in line switching equations and redefinition of lea and lca sets

[2.6.4] - 2021-06-23
--------------------
- [FIXED] typo in equation formulating the total output of a unit
- [CHANGED] introduce binary commitment option for each unit
- [CHANGED] introduce adequacy reserve margin for each area
- [CHANGED] introduce availability for each unit

[2.6.3] - 2021-06-20
--------------------
- [FIXED] typo in investment constraint in model formulation

[2.6.2] - 2021-06-18
--------------------
- [CHANGED] updated for pyomo 6.0
- [CHANGED] if not defined length computed as geographical distance

[2.6.1] - 2021-06-14
--------------------
- [CHANGED] line length added in network input file
- [FIXED] error in output results due to stage weight

[2.6.0] - 2021-05-27
--------------------
- [CHANGED] new inertia constraint for each area
- [FIXED] change column BinarySwitching by Switching in network data meaning that line is able to switch or not

[2.5.3] - 2021-05-14
--------------------
- [FIXED] fix output results of storage utilization

[2.5.2] - 2021-05-11
--------------------
- [CHANGED] new ESS inventory utilization result file
- [FIXED] protection against stage with no load levels

[2.5.1] - 2021-05-07
--------------------
- [FIXED] introduction of stage weight in the operation variable cost

[2.5.0] - 2021-04-29
--------------------
- [CHANGED] generalize the definition of stages to allow using representative stages (weeks, days, etc.)

[2.4.2] - 2021-04-29
--------------------
- [CHANGED] initialize shutdown variable
- [FIXED] fix error in conditions to formulate the relationship between UC, startup and shutdown

[2.4.1] - 2021-04-28
--------------------
- [CHANGED] very small parameters -> 0 depending on the area
- [CHANGED] avoid use of list if not needed

[2.4.0] - 2021-04-24
--------------------
- [CHANGED] new input files VariableMaxConsumption and VariableMinConsumption and MininmumCharge column in Generation file
- [CHANGED] change names of MaximumStorage (MinimumStorage) files to VariableMaxStorage (VariableMinStorage)

[2.3.1] - 2021-04-23
--------------------
- [CHANGED] avoid superfluous equations

[2.3.0] - 2021-04-20
--------------------
- [CHANGED] separate model data and optimization model

[2.2.5] - 2021-04-18
--------------------
- [FIXED] fix commitment, startup and shutdown decisions of hydro units
- [FIXED] output results of storage units
- [FIXED] detection of storage units

[2.2.4] - 2021-04-10
--------------------
- [FIXED] fix line switch off constraint

[2.2.3] - 2021-04-07
--------------------
- [FIXED] determine the commitment and output of generating units at the beginning of each stage

[2.2.2] - 2021-04-05
--------------------
- [CHANGED] remove a warning in InputData

[2.2.1] - 2021-04-03
--------------------
- [CHANGED] added three new output files for line commitment, switch on and off
- [CHANGED] added three four output files for ESS energy outflows
- [FIXED]   fix writing flexibility files for ESS

[2.2.0] - 2021-03-31
--------------------
- [CHANGED] introduction of Power-to-X in ESS. Modifies the Generation file and introduces a new EnergyOutflows file
- [CHANGED] introduction of switching decision for transmission lines. Modifies the Option file and introduces a new column BinarySwitching in Network file

[2.1.0] - 2021-03-18
--------------------
- [CHANGED] using README.rst instead of README.md
- [CHANGED] split openTEPES_ModelFormulation.py in multiple functions related to investment and operating constraints
- [CHANGED] split openTEPES_OutputResults.py in multiple functions related to investment and operating variables

[2.0.24] - 2021-03-08
---------------------

- [FIXED] changed location of the shell openTEPES to sub folder openTEPES with all modules
- [FIXED] updated _init_.py

[2.0.23] - 2021-03-08
---------------------

- [CHANGED] included metadata in pyproject.toml and also requirements  (only pyomo, matplotlib, numpy, pandas, and psutil.)
- [CHANGED] created a README.md file
