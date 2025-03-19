from Algo import Minimize
from Evaluation import Evaluate
from Analysis import find_difference, analyze_csv_files, find_ratio
from FrontEndMapping import Mapping
from scalecsv import scale_third_column
import pandas as pd

def Model(scalar=1):
    OriginalCountyDemand = 'Model/CSVLib/CountyData.csv' 
    OriginalCountySupply = 'Model/CSVLib/SupplierData.csv'

    Demand = scale_third_column(OriginalCountyDemand,'Model/CSVLib/CountyData-Scaled.csv', scalar)
    Supply = scale_third_column(OriginalCountySupply,'Model/CSVLib/SupplierData-Scaled.csv', 1)

    Locations = "Model/CSVLib/Locations.csv"

    TranspartResourceDistribution = "Model/CSVResults/TransparentDistribution.csv"
    CompetitiveResourceDistribution = "Model/CSVResults/NonTransparentDistribution.csv"

    UpdatedTransparentDemand = 'Model/CSVResults/TransparentDemand.csv'
    UpdatedCompetitiveDemand = 'Model/CSVResults/NonTransparentDemand.csv'


    costdistribution1,Locations1 =Minimize(Supply,Demand,Locations, TranspartResourceDistribution,trials=50, Mtype="Transparent")
    costdistribution2,Locations2 =Minimize(Supply,Demand,Locations, CompetitiveResourceDistribution,trials=50, Mtype="NonTransparent")

    Evaluate(TranspartResourceDistribution,UpdatedTransparentDemand)
    Evaluate(CompetitiveResourceDistribution,UpdatedCompetitiveDemand)

    find_difference(Demand, UpdatedTransparentDemand, 'Model/CSVResults/TransparentAnalysifill.csv')
    find_difference(Demand, UpdatedCompetitiveDemand, 'Model/CSVResults/NonTransparentAnalysisfill.csv')

    Mapping(TranspartResourceDistribution,"Model/OutputFiles/Transparent.html")
    Mapping(CompetitiveResourceDistribution,"Model/OutputFiles/NonTransparent.html")

    ratio = find_ratio(Supply,Demand)
    transparentequity, nontransparentequity = analyze_csv_files(UpdatedTransparentDemand, UpdatedCompetitiveDemand, Demand)

    return([ratio, costdistribution1[0], transparentequity, costdistribution2[0], nontransparentequity])
