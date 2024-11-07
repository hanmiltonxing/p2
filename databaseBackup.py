To create a database automatic backup module for the latest version of Odoo:

1. **Schedules automatic backups** at a specified interval.
2. **Saves the backups** to a specified directory.
3. **Allows configuring backup options** through Odoo settings.

This module will create an automatic backup system that will back up the database periodically and store it locally.

### Step 1: Create the Module Structure

1. Create a new directory in your Odoo `addons` folder called `db_backup_auto`.
2. Inside `db_backup_auto`, create the following structure:

```
db_backup_auto/
├── __init__.py
├── __manifest__.py
├── models/
│   └── db_backup.py
├── data/
│   └── backup_cron.xml
└── views/
    └── backup_settings_view.xml
```

### Step 2: Module Manifest (`__manifest__.py`)

Define the module metadata in `__manifest__.py`.

```python
{
    'name': 'Automatic Database Backup',
    'version': '1.0',
    'summary': 'Automatically back up the database at regular intervals',
    'author': 'Your Name',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'data/backup_cron.xml',
        'views/backup_settings_view.xml',
    ],
    'installable': True,
    'application': False,
}
```

### Step 3: Define the Backup Model (`models/db_backup.py`)

In this file, create a model to manage the backup settings and a function to run the backup.

```python
# db_backup_auto/models/db_backup.py

import os
import logging
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, safe_eval

_logger = logging.getLogger(__name__)

class DatabaseBackupSettings(models.Model):
    _name = 'db.backup.settings'
    _description = 'Database Backup Settings'
    _rec_name = 'backup_path'

    backup_path = fields.Char(
        string="Backup Path",
        required=True,
        help="The directory path where backups will be stored.")
    backup_frequency = fields.Integer(
        string="Backup Frequency (hours)",
        default=24,
        help="Frequency in hours to perform automatic backups.")

    def _perform_backup(self):
        """This method performs the database backup."""
        db_name = self.env.cr.dbname
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{db_name}_backup_{timestamp}.zip"
        backup_path = os.path.join(self.backup_path, backup_filename)

        # Ensure backup directory exists
        os.makedirs(self.backup_path, exist_ok=True)

        # Perform the backup
        try:
            self.env['ir.config_parameter'].backup_database(
                db_name=db_name,
                zip_path=backup_path,
            )
            _logger.info(f"Database backup saved to: {backup_path}")
        except Exception as e:
            _logger.error(f"Failed to back up database: {e}")
            raise UserError(f"Failed to back up database: {e}")
```

### Step 4: Define a Cron Job (`data/backup_cron.xml`)

This cron job will call the `_perform_backup` method at the interval specified in the settings.

```xml
<!-- db_backup_auto/data/backup_cron.xml -->

<odoo>
    <record id="ir_cron_db_backup" model="ir.cron">
        <field name="name">Database Backup</field>
        <field name="model_id" ref="model_db_backup_settings"/>
        <field name="state">code</field>
        <field name="code">model._perform_backup()</field>
        <field name="interval_number" eval="24"/> <!-- Default 24 hours -->
        <field name="interval_type">hours</field>
        <field name="numbercall">-1</field>
        <field name="active" eval="True"/>
    </record>
</odoo>
```

### Step 5: Create Settings View (`views/backup_settings_view.xml`)

This view allows the user to configure the backup path and frequency from the Odoo interface.

```xml
<!-- db_backup_auto/views/backup_settings_view.xml -->

<odoo>
    <record id="view_backup_settings_form" model="ir.ui.view">
        <field name="name">db.backup.settings.form</field>
        <field name="model">db.backup.settings</field>
        <field name="arch" type="xml">
            <form string="Database Backup Settings">
                <sheet>
                    <group>
                        <field name="backup_path"/>
                        <field name="backup_frequency"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="backup_settings_action" model="ir.actions.act_window">
        <field name="name">Database Backup Settings</field>
        <field name="res_model">db.backup.settings</field>
        <field name="view_mode">form</field>
        <field name="target">current</field>
    </record>

    <menuitem id="menu_backup_settings" name="Database Backup"
              parent="base.menu_custom" action="backup_settings_action"/>
</odoo>
```

### Step 6: Initialize Module (`__init__.py`)

Include the model in the module’s init file.

```python
# db_backup_auto/__init__.py

from . import models
```

### Step 7: Add Logic to Trigger Database Backup (`backup_database` method)

To handle the actual database backup, we need to add this method (Odoo’s `backup_database` function) that creates a `.zip` file for the database.

Odoo has internal methods for backup, but if you want to call `pg_dump` directly, make sure PostgreSQL tools are available.

### Step 8: Install the Module

1. Restart the Odoo server.
2. Go to **Apps** and update the app list.
3. Install the **Automatic Database Backup** module.
4. Configure the settings under the newly created menu.

### Final Notes

- Ensure that the backup directory has proper permissions for the Odoo user.
- Adjust `backup_frequency` as needed.
- This module can be expanded to support more complex configurations, such as remote storage or notifications.
