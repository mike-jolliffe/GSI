USE Armstrong
GO

-- Add Waste Material Sample Matrix Code to appropriate stations and samples
Update smp
Set SampleMatrixCode = 'WM'
FROM Stations stt join Samples smp On (stt.stationNumber = smp.StationNumber)
Where stt.StationName IN ('BRD-1', 'BS-1', 'WS-1')

-- Modify the Soil StationType to include soil and sediment for symbology consistency with prior ArcMap deliverables
Update StationTypes
Set StationTypeCode = 'sdso', StationType = 'Soil or Sediment', FontName = 'ESRI Default Marker', FontIndex = '35'
WHERE StationTypeCode = 'sdso'

-- Create new StationType symbology for Catch Basin Solids
Insert into StationTypes
Values ('CBS', 'Solids', 'ESRI Default Marker', '37', '18', 'Green')

-- Create new Stationtype symbology for Waste Material
Insert into StationTypes
Values ('WM', 'Waste Material', 'ESRI Default Marker', '79', '18', 'Yellow')

