USE [��������]

--UPDATE [dbo].[Product]
--SET Name_product = '������ ������',
--    Price = 100.00,
--    Count_product = 10,
--    Pictury = NULL,  -- ��� ������� �������� ������, ���� ����
--    Description = '�������� ������'
--WHERE ID = 1;  -- ������� ID ������, ������� �� ������ ��������

--INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description) 
--VALUES ('������ ������', 100.00, 10, NULL, '�������� ������');

-- �������� Ad Hoc Distributed Queries



--EXEC sp_configure 'show advanced options', 1;
--RECONFIGURE;
--EXEC sp_configure 'Ad Hoc Distributed Queries', 1;
--RECONFIGURE;

-- ��������� ���������� ��� �������� �������� ������
--DECLARE @ImageData VARBINARY(MAX);

-- ��������� ����������� �� �����
--SELECT @ImageData = BulkColumn 
--FROM OPENROWSET(BULK 'edu.local\\public\studenthomes\23200778\Desktop\������� ������\����\������\image\1661496275_new_preview_meme-faces10.png', SINGLE_BLOB) AS Image;

-- ��������� ������ � �������
--INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description) 
--VALUES ('������ ������', 100.00, 10, @ImageData, '�������� ������');

--EXEC sp_configure 'Ad Hoc Distributed Queries';