# Generated by Django 4.1.9 on 2023-06-12 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dcim", "0171_cabletermination_change_logging"),
        ("netbox_cisco_support_plugin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CiscoDeviceSupport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("serial", models.CharField(blank=True, max_length=100, null=True)),
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("coverage_end_date", models.DateField(blank=True, null=True)),
                ("service_contract_number", models.CharField(blank=True, max_length=100, null=True)),
                ("service_line_descr", models.CharField(blank=True, max_length=100, null=True)),
                ("warranty_type", models.CharField(blank=True, max_length=100, null=True)),
                ("warranty_end_date", models.DateField(blank=True, null=True)),
                ("is_covered", models.BooleanField(default=False)),
                ("sr_no_owner", models.BooleanField(default=False)),
                ("contract_supplier", models.CharField(blank=True, max_length=100, null=True)),
                ("api_status", models.CharField(blank=True, max_length=100, null=True)),
                ("recommended_release", models.CharField(blank=True, max_length=100, null=True)),
                ("desired_release", models.CharField(blank=True, max_length=100, null=True)),
                ("current_release", models.CharField(blank=True, max_length=100, null=True)),
                ("desired_release_status", models.BooleanField(default=False)),
                ("current_release_status", models.BooleanField(default=False)),
                ("eox_has_error", models.BooleanField(default=False)),
                ("eox_error", models.CharField(blank=True, max_length=100, null=True)),
                ("eox_announcement_date", models.DateField(blank=True, null=True)),
                ("end_of_sale_date", models.DateField(blank=True, null=True)),
                ("end_of_sw_maintenance_releases", models.DateField(blank=True, null=True)),
                ("end_of_security_vul_support_date", models.DateField(blank=True, null=True)),
                ("end_of_routine_failure_analysis_date", models.DateField(blank=True, null=True)),
                ("end_of_service_contract_renewal", models.DateField(blank=True, null=True)),
                ("last_date_of_support", models.DateField(blank=True, null=True)),
                ("end_of_svc_attach_date", models.DateField(blank=True, null=True)),
                (
                    "device",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="dcim.device"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="ciscodevicetypesupport",
            name="eox_error",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name="CiscoSupport",
        ),
    ]
