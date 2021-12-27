# mssql-django Index Issue

This project was created to reproduce a problem with indexes created by mssql-django 
version 1.1.

Steps to reproduce:

1. Create a model with a char field that allows NULL values.  Make and apply migrations.
  - migration: 0001 in the widgets app.
  - reference commit 4a261e16 in this project.
2. Alter the char field so that it no longer allows NULL values.  Make and apply migrations.
  - migration: 0002 in the widgets app.
  - reference commit 732704a7 in this projejct.
  - This migration created in this step creates the problematic index.

    ```sql
    BEGIN TRANSACTION
    --
    -- Alter field url on widget
    --
    DROP INDEX [widgets_widget_url_98f0535d] ON [widgets_widget];
    ALTER TABLE [widgets_widget] ADD DEFAULT '' FOR [url];
    UPDATE [widgets_widget] SET [url] = '' WHERE [url] IS NULL;
    ALTER TABLE [widgets_widget] ALTER COLUMN [url] nvarchar(255) NOT NULL;
    CREATE INDEX [widgets_widget_url_98f0535d] ON [widgets_widget] ([url]); -- <--- Problematic index
    SELECT d.name FROM sys.default_constraints d INNER JOIN sys.tables t ON d.parent_object_id = t.object_id INNER JOIN sys.columns c ON d.parent_object_id = c.object_id AND d.parent_column_id = c.column_id INNER JOIN sys.schemas s ON t.schema_id = s.schema_id WHERE t.name = 'widgets_widget' AND c.name = 'url';
    ALTER TABLE [widgets_widget] DROP CONSTRAINT [url];
    COMMIT;
    ```

3. Change the char field to a text field.  Make and attempt to apply migrations.
  - migration: 0003 in the widgets app.
  - reference commit 3070df23 in this project.
  - This migration will fail because the index `widgets_widget_url_98f0535d` was not dropped first.

This problem does not occur with mssql-django version 1.0.  Migration 0002 generates the following SQL:
```sql
--
-- Alter field url on widget
--
ALTER TABLE [widgets_widget] ADD DEFAULT '' FOR [url];
UPDATE [widgets_widget] SET [url] = '' WHERE [url] IS NULL;
ALTER TABLE [widgets_widget] ALTER COLUMN [url] nvarchar(255) NOT NULL;
SELECT d.name FROM sys.default_constraints d INNER JOIN sys.tables t ON d.parent_object_id = t.object_id INNER JOIN sys.columns c ON d.parent_object_id = c.object_id AND d.parent_column_id = c.column_id INNER JOIN sys.schemas s ON t.schema_id = s.schema_id WHERE t.name = 'widgets_widget' AND c.name = 'url';
ALTER TABLE [widgets_widget] DROP CONSTRAINT [url];
```

