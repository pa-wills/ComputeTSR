CREATE TABLE ClosingPrices (DateOfClose DATE, SecurityName VARCHAR, Price DECIMAL, PRIMARY KEY (DateOfClose, SecurityName));
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'ANZ.AX', 24.55);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'ARG.AX', 8.68);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'IAF.AX', 113.37);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'MFF.AX', 3.4215);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'NDQ.AX', 21.23);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'PAI.AX', 1.095);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'PMC.AX', 1.6717);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'TGG.AX', 1.37);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'TLS.AX', 3.5502);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'VGS.AX', 81.77);
INSERT INTO ClosingPrices (DateOfClose, SecurityName, Price) VALUES ('2020-01-02', 'WBC.AX', 24.19);

CREATE TABLE Distributions (Date_XD DATE, Date_Payable DATE, Security VARCHAR, Cash_Amount DECIMAL, Tax_Amount DECIMAL);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2017-10-13', '2017-11-10', 'MFF.AX', 0.01, 0.004285714);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2018-04-30', '2018-05-18', 'MFF.AX', 0.015, 0.006428571);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2018-10-12', '2018-11-09', 'MFF.AX', 0.015, 0.006428571);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2019-04-19', '2019-05-17', 'MFF.AX', 0.015, 0.006428571);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2019-10-14', '2019-11-08', 'MFF.AX', 0.02, 0.008571429);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2020-04-27', '2020-05-15', 'MFF.AX', 0.025, 0.010714286);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2020-02-04', '2020-02-19', 'MFF.AX', 0.2, 0.085714286);

CREATE TABLE Performance (PositionDateAcq DATE, PositionSecurityName VARCHAR, RawTSR DECIMAL, AnnTSR DECIMAL, PRIMARY KEY (PositionDateAcq, PositionSecurityName));

CREATE TABLE Positions (Acq_Date DATE, Acq_Transaction VARCHAR, Security VARCHAR, Units NUMERIC, Acq_Unit_Price DECIMAL, Acq_Brokerage DECIMAL, Acq_Total_Cost NUMERIC, Acq_Remarks VARCHAR, Dis_Date DATE, Dis_Transaction VARCHAR, Dis_Unit_Price DECIMAL, Dis_Brokerage DECIMAL, Dis_Total_Cost NUMERIC, Dis_Remarks VARCHAR);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2017-10-10', 'Buy', 'MFF.AX', 10000, 1.91, 0, 19130.07, 'Acquisitions costs need looking at.', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2017-11-10', 'Buy', 'MFF.AX', 50, 1.98, 0, 99.21, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2018-05-18', 'Buy', 'MFF.AX', 64, 2.3664, 0, 151.45, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2018-11-09', 'Buy', 'MFF.AX', 56, 2.6879, 0, 150.52, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2019-05-17', 'Buy', 'MFF.AX', 51, 2.9642, 0, 151.17, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2019-11-08', 'Buy', 'MFF.AX', 64, 3.2127, 0, 205.61, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2020-02-19', 'Buy', 'MFF.AX', 569, 3.6167, 0, 2057.9, 'DRP purchase', NULL, NULL, NULL, NULL, NULL, NULL);
