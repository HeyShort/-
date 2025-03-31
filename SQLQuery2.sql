USE [Курсовая]

--UPDATE [dbo].[Product]
--SET Name_product = 'Пример товара',
--    Price = 100.00,
--    Count_product = 10,
--    Pictury = NULL,  -- или укажите бинарные данные, если есть
--    Description = 'Описание товара'
--WHERE ID = 1;  -- Укажите ID товара, который вы хотите обновить

--INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description) 
--VALUES ('Пример товара', 100.00, 10, NULL, 'Описание товара');

-- Включаем Ad Hoc Distributed Queries



--EXEC sp_configure 'show advanced options', 1;
--RECONFIGURE;
--EXEC sp_configure 'Ad Hoc Distributed Queries', 1;
--RECONFIGURE;

-- Объявляем переменную для хранения бинарных данных
--DECLARE @ImageData VARBINARY(MAX);

-- Загружаем изображение из файла
--SELECT @ImageData = BulkColumn 
--FROM OPENROWSET(BULK 'edu.local\\public\studenthomes\23200778\Desktop\Куровая работа\курс\Резерв\image\1661496275_new_preview_meme-faces10.png', SINGLE_BLOB) AS Image;

-- Вставляем данные в таблицу
--INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description) 
--VALUES ('Пример товара', 100.00, 10, @ImageData, 'Описание товара');

--EXEC sp_configure 'Ad Hoc Distributed Queries';