
SELECT COUNT(*) FROM stg.posts; -- Количество записей в STG
SELECT COUNT(*) FROM dds.hub_post;-- Уникальных постов в хабе
SELECT COUNT(*) FROM dds.hub_user; --Уникальных пользователей
SELECT COUNT(*) FROM dds.link_post_user;--Связей пост-пользователь
SELECT COUNT(*) FROM dds.sat_post; --Сателлит постов
SELECT * FROM dds.sat_post LIMIT 5; --Пример