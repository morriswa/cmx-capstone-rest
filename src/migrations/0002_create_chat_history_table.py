from django.db import migrations

'''
Django migration for auth_integration tables
'''
class Migration(migrations.Migration):
    """
        Django migration for auth_integration tables
        :author Timothy Holmes """
    dependencies = [("core", "0001_create_auth_integration_table")] #dependencies for the migration
    operations = [ #List of operations that will be performe during the migration
        migrations.RunSQL(
            #SQL statement to creat auth integration table to generat uuid and email
            sql="""
                create table chat_history(
                    pair_id uuid primary key default gen_random_uuid(),
                    chat_id uuid not null default gen_random_uuid(),
                    user_id uuid not null references auth_integration(user_id),
                    created timestamp not null default current_timestamp,
                    q varchar(256) not null,
                    a json not null
                );
            """,
            #SQL statement to drop the auth integration table
            reverse_sql="""
                drop table if exists chat_history;
            """
        )
    ]
