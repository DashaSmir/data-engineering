# data-engineering
# Решение тестового задания.

## Описание

В этом репозитории представлены решения задачи: реализовать загрузку данных в корпоративное хранилище в слой DDS, для моделирования слоя DDS.
использовать методологию Data Vault 2.0.

## Стек технологий
- Python 3.12 – скрипты ETL.

- PostgreSQL – хранилище данных.

- Docker – контейнеризация БД.

- Data Vault 2.0 – методология моделирования DDS.

- REST API – источник данных.
- 
## Как запустить
   ```bash
1. Установите PostgreSQL
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d postgres
```
2. Проверка работы docker
   ```bash
   docker ps
   ```
3. Установить зависимости
   ```bash
   pip install requests psycopg2-binary
   ```
4. Запустить python-скрипты
   Запуск ELT1 и ELT2
   ```bash
   python elt1_load_stg.py
   python elt2_to_dds.py
   ```
5. В качестве проверки, необходимо выполнить следующие SQL-запросы.
   ```sql
    SELECT COUNT(*) FROM dds.sat_post;
    SELECT COUNT(*) FROM dds.link_post_user;
    SELECT COUNT(*) FROM stg.posts;
    SELECT COUNT(*) FROM dds.hub_post;
    SELECT COUNT(*) FROM dds.hub_user;
    SELECT * FROM dds.sat_post LIMIT 5;
   ```
Далее выполнено подключени к БД через DBeaver, результат выполнения прикреплен ниже:

<img width="239" height="103" alt="Снимок экрана 2026-06-04 223339" src="https://github.com/user-attachments/assets/c7a8b5d9-ebab-42b4-bc57-c493bc3cf470" />

<img width="1700" height="246" alt="Снимок экрана 2026-06-04 223429" src="https://github.com/user-attachments/assets/72c7c517-7a22-44a9-a6cb-9a39d1af9d79" />

<img width="896" height="213" alt="Снимок экрана 2026-06-04 223403" src="https://github.com/user-attachments/assets/49e0a52f-46a4-4c6d-b26d-0c0837ec0736" />

<img width="820" height="166" alt="Снимок экрана 2026-06-04 223356" src="https://github.com/user-attachments/assets/17b78a41-3d87-4255-9b06-5e35b4175131" />

<img width="751" height="192" alt="Снимок экрана 2026-06-04 223351" src="https://github.com/user-attachments/assets/0aa1b01a-2ce5-45db-b0e2-47c2b4853bd4" />

<img width="336" height="82" alt="Снимок экрана 2026-06-04 223344" src="https://github.com/user-attachments/assets/3b4f0729-dced-4c3c-b44b-e8e74dd05fcf" />

## Потоки данных
### ELT1 – Загрузка в STG

   - HTTP GET запрос к https://jsonplaceholder.typicode.com/posts.

   - Для каждого поста вычисляется hash_diff (MD5 от id+userId+title+body).

   - Запись в таблицу stg.posts с меткой времени load_ts.


### ELT2 – Трансформация STG в DDS

    - Читаются все записи из stg.posts.

    Для каждой записи:

       - Вычисляются хэши

       - Происходит вставка в hub_post (если ещё нет такого post_hk).

       - Происходит вставка в hub_user (если ещё нет такого user_hk).

       - Происходит вставка в link_post_user (если ещё нет такой связи).

       - Происходит вставка в sat_post.

