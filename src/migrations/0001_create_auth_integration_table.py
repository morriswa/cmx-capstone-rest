from django.db import migrations

'''
Django migration for auth_integration tables
'''
class Migration(migrations.Migration):
    """
        Django migration for auth_integration tables
        :author William Morris """
    dependencies = [] #dependencies for the migration
    operations = [ #List of operations that will be performe during the migration
        migrations.RunSQL(
            #SQL statement to creat auth integration table to generat uuid and email
            sql=""" 
                create table auth_integration(
                    user_id uuid primary key default gen_random_uuid(),
                    email varchar(256) not null unique
                );
            """,
            #SQL statement to drop the auth integration table
            reverse_sql="""
                drop table if exists auth_integration;
            """
        )
    ]
