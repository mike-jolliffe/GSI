-- Procedure to get MS_Description extended property (metadata description) for a given table and column
CREATE PROCEDURE usp_GetColMetadata
@TableName VARCHAR(50),
@ColName VARCHAR(50)
AS
SELECT S.name as [Schema Name], O.name AS [Object Name], c.name AS [column name], ep.name, ep.value AS [Extended property]
FROM sys.extended_properties EP
INNER JOIN sys.all_objects O ON ep.major_id = O.object_id
INNER JOIN sys.schemas S on O.schema_id = S.schema_id
INNER JOIN sys.columns AS c ON ep.major_id = c.object_id AND ep.minor_id = c.column_id
WHERE O.name = @TableName AND c.name = @ColName

GO
