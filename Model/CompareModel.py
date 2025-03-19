from Algo import Minimize
from Evaluation import Evaluate
from Analysis import find_fill_and_difference, analyze_csv_files, find_ratio
from FrontEndMapping import Mapping
from scalecsv import scale_third_column
import pandas as pd

def Model(SupplyPath,DemandPath,scalar=1):

    Supply = scale_third_column(SupplyPath,'Model/CSVLib/SupplierData-Scaled.csv', 1)
    Demand = scale_third_column(DemandPath,'Model/CSVLib/CountyData-Scaled.csv', scalar)
    print(Demand)
    Locations = "Model/CSVLib/Locations.csv"

    TranspartResourceDistribution = "Model/CSVResults/TransparentDistribution.csv"
    CompetitiveResourceDistribution = "Model/CSVResults/NonTransparentDistribution.csv"

    UpdatedTransparentDemand = 'Model/CSVResults/TransparentDemand.csv'
    UpdatedCompetitiveDemand = 'Model/CSVResults/NonTransparentDemand.csv'
    TransparentDifference = 'Model/CSVResults/TransparentAnalysisdifference.csv'
    NonTransparentDifference = 'Model/CSVResults/NonTransparentAnalysisdifference.csv'

    costdistribution1,Locations1 =Minimize(Supply,Demand,Locations, TranspartResourceDistribution,trials=50, Mtype="Transparent")
    costdistribution2,Locations2 =Minimize(Supply,Demand,Locations, CompetitiveResourceDistribution,trials=50, Mtype="NonTransparent")

    Evaluate(TranspartResourceDistribution,UpdatedTransparentDemand)
    Evaluate(CompetitiveResourceDistribution,UpdatedCompetitiveDemand)

    find_fill_and_difference(Demand, UpdatedTransparentDemand, 'Model/CSVResults/TransparentAnalysifill.csv',TransparentDifference)
    find_fill_and_difference(Demand, UpdatedCompetitiveDemand, 'Model/CSVResults/NonTransparentAnalysisfill.csv',NonTransparentDifference)

    Mapping(TranspartResourceDistribution,"Model/OutputFiles/Transparent.html")
    Mapping(CompetitiveResourceDistribution,"Model/OutputFiles/NonTransparent.html")

    ratio = find_ratio(Supply,Demand)
    transparentequity, nontransparentequity = analyze_csv_files(UpdatedTransparentDemand,TransparentDifference, UpdatedCompetitiveDemand,NonTransparentDifference, Demand)

    return([ratio, costdistribution1[0], transparentequity[0],transparentequity[1], costdistribution2[0], nontransparentequity[0],nontransparentequity[1]])
