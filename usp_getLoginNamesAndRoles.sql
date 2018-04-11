-- Get login names, Roles, and disabled status for given database
CREATE PROCEDURE usp_getLoginNamesAndRoles
AS
SELECT 
	p.name AS [LOGIN_NAME] , 
	CASE WHEN IS_SRVROLEMEMBER('sysadmin', p.name) = 1 THEN 'Yes' ELSE 'No' END AS [IS_SYSADMIN],
	p.type_desc AS [TYPE_DESC],
	CONVERT(VARCHAR(25),dbp2.name) AS [DB_ROLE], 
	p.is_disabled, 
	CONVERT(VARCHAR(10),p.create_date ,101) AS [CREATED], 
	CONVERT(VARCHAR(10),p.modify_date , 101) AS [UPDATE]
FROM sys.server_principals AS p 
	JOIN sys.syslogins AS s ON p.sid = s.sid
	LEFT JOIN sys.database_principals AS dbp ON p.sid = dbp.sid
	LEFT JOIN sys.database_role_members AS dbrm ON dbp.principal_Id = dbrm.member_principal_Id 
	LEFT JOIN sys.database_principals AS dbp2 ON dbrm.role_principal_id = dbp2.principal_id
WHERE p.name NOT LIKE '##%'

GO
