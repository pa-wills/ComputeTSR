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
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2007-04-13', '2007-04-13', 'PBL.AX', 0.25, 0.107142);
INSERT INTO Distributions (Date_XD, Date_Payable, Security, Cash_Amount, Tax_Amount) VALUES ('2007-10-15', '2007-10-15', 'PBL.AX', 0.30, 0.128571);

CREATE TABLE Performance (PositionDateAcq DATE, PositionSecurityName VARCHAR, RawTSR DECIMAL, AnnTSR DECIMAL, PRIMARY KEY (PositionDateAcq, PositionSecurityName));

CREATE TABLE Positions (Acq_Date DATE, Acq_Transaction VARCHAR, Security VARCHAR, Units NUMERIC, Acq_Unit_Price DECIMAL, Acq_Brokerage DECIMAL, Acq_Total_Cost NUMERIC, Acq_Remarks VARCHAR, Dis_Date DATE, Dis_Transaction VARCHAR, Dis_Unit_Price DECIMAL, Dis_Brokerage DECIMAL, Dis_Total_Cost NUMERIC, Dis_Remarks VARCHAR);
INSERT INTO Positions (Acq_Date, Acq_Transaction, Security, Units, Acq_Unit_Price, Acq_Brokerage, Acq_Total_Cost, Acq_Remarks, Dis_Date, Dis_Transaction, Dis_Unit_Price, Dis_Brokerage, Dis_Total_Cost, Dis_Remarks) VALUES ('2007-03-16', 'Buy', 'PBL.AX', 700, 19, 29.95, 13329.95, '', '2007-12-03', 'Sell', '20.80', '0', '14560', 'This was the close price on Nov 30, the final day of trading - see my Quicken extracts');
