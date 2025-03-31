USE [Курсовая_100]


--ALTER TABLE Users ADD is_deleted BIT DEFAULT 0;

--CREATE TABLE [dbo].[Users] (
--    ID INT IDENTITY(1,1) PRIMARY KEY,
--    login VARCHAR(50) NOT NULL,
--    password VARCHAR(50) NOT NULL,
--    role VARCHAR(50) NOT NULL,
--    is_deleted BIT DEFAULT 0
--);


--DROP TABLE Product
--CREATE TABLE [dbo].[Product] (
--    ID INT IDENTITY(1,1) PRIMARY KEY,
--	Name_product varchar(50) NULL,
--	Price int NULL,
--	Count_product int NULL,
--	Pictury VARBINARY(MAX) NULL,
--	Description varchar(MAX) NULL,
--	Time_in_a_account time(7) NULL,
--	Date date NULL
--);


--DROP TABLE Account_in_a_game 

CREATE TABLE [dbo].[Account_in_a_game] (
    ID int IDENTITY(1,1) PRIMARY KEY, 
	ID_login int null,
	Email varchar(255) null,
	Password varchar(255) null
);

CREATE TABLE [dbo].[Customers] (
    ID INT IDENTITY(1,1) PRIMARY KEY,
	login varchar(50) null,
	password varchar(50) null,
	role varchar(50) null,
	email varchar(255) null
);



--CREATE TABLE #TempProduct (
--    ID INT IDENTITY(1,1) PRIMARY KEY,
--    Name_product NVARCHAR(255),
--    Price INT,
--    Count_product INT,
--    Pictury VARBINARY(MAX),
--    Description NVARCHAR(255)
--);

--ALTER TABLE Account_in_a_game
--ALTER COLUMN ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL;

















--ALTER TABLE [dbo].[Account_in_a_game]
--DROP COLUMN Time_in_a_account, Date;


--ALTER TABLE [dbo].[Product]
--ADD Time_in_a_account time(7),
--    Date date;





































--SELECT Name_product, Price, Count_product, Pictury, Description, is_deleted FROM [dbo].[Products]

--ALTER TABLE [dbo].[Products]
--ALTER COLUMN Pictury VARBINARY(MAX);

--ALTER TABLE Products
--ALTER COLUMN Pictury VARBINARY(MAX);

--SELECT COLUMN_NAME, DATA_TYPE 
--FROM INFORMATION_SCHEMA.COLUMNS 
--WHERE TABLE_NAME = 'Product' AND COLUMN_NAME = 'Pictury';

--EXEC sp_help 'Product';

--INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description, Time_in_a_account, Date)
--VALUES ('Test Product', 10.00, 5, NULL, 'Test Description', '12:00:00', '2023-10-01');

--ALTER TABLE [dbo].[Product]
--ALTER COLUMN Pictury VARBINARY(MAX);



--CREATE TABLE [dbo].[Customers] (
--    ID INT IDENTITY(1,1) PRIMARY KEY,
--	login varchar(50) null,
--	password varchar(50) null,
--	role varchar(50) null,
--	email varchar(255) null
--);