pause
pause
pause

goto skip
DO $$ DECLARE
    tabname RECORD;
BEGIN
    FOR tabname IN (SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = current_schema()) 
LOOP
    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(tabname.tablename) || ' CASCADE';
END LOOP;
END $$;
:skip

# del db.sqlite3
call m flush
del games\migrations\0*.py
del core\migrations\0*.py
call m makemigrations games
call m makemigrations core
call m migrate
call m initifdb
call m createsuperuser --email "ersatzplut+bot@gmail.com" --username "бездушный робот" --noinput
call m createsuperuser --email "mooskagh@gmail.com" --username "crem"