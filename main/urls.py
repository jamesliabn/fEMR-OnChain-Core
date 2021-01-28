"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:

https://docs.djangoproject.com/en/3.0/topics/http/urls/

Examples:

Function views

1. Add an import:  `from my_app import views`

2. Add a URL to urlpatterns:  `path('', views.home, name='home')`

Class-based views

1. Add an import:  `from other_app.views import Home`

2. Add a URL to urlpatterns:  `path('', Home.as_view(), name='home')`

Including another URLconf

1. Import the `include()` function: `from django.urls import include, path`

2. Add a URL to urlpatterns:  `path('blog/', include('blog.urls'))`
"""
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as rest_framework_views

from main.admin_views import add_user_to_campaign, add_users_to_campaign, admin_home, create_user_view, cut_user_from_campaign, export_audit_logs_view, export_database_logs_view, \
    filter_audit_logs_view, filter_database_logs_view, filter_users_view, get_audit_logs_view, get_database_logs_view, \
    list_users_view, lock_user_view, unlock_user_view, search_audit_logs_view, search_database_logs_view, \
    search_users_view, update_user_view, update_user_password_view
from .api_views import UserViewSet, GroupViewSet, PatientViewSet, PatientEncounterViewSet, InstanceViewSet, CampaignViewSet
from .auth_views import all_locked, not_logged_in, login_view, logout_view, permission_denied
from .edit_views import patient_edit_form_view, encounter_edit_form_view, patient_export_view
from .form_views import allergy_form_view, health_concern_form_view, immunization_form_view, \
    lab_test_form_view, medication_form_view, patient_form_view, problem_form_view, \
    procedure_form_view, referral_form_view, test_form_view, patient_encounter_form_view
from .list_views import allergy_list_view, health_concern_list_view, immunization_list_view, lab_test_list_view, \
    medication_list_view, patient_csv_export_view, patient_list_view, problem_list_view, procedure_list_view, test_list_view, \
    search_patient_list_view, filter_patient_list_view
from .views import forgot_username, index, home, healthcheck
from .femr_admin_views import edit_contact_view, lock_campaign_view, new_campaign_view, new_contact_view, new_instance_view, edit_campaign_view, edit_instance_view, \
    list_campaign_view, list_instance_view, femr_admin_home, change_campaign, unlock_campaign_view
from main.views import set_timezone
from main import hl7
from main.femr_admin_views import lock_instance_view, unlock_instance_view

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'Groups', GroupViewSet)
router.register(r'Patient', PatientViewSet)
router.register(r'Encounter', PatientEncounterViewSet)
router.register(r'Campaign', CampaignViewSet)
router.register(r'Instance', InstanceViewSet)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^home/$', home, name='home'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'^login_view/$', login_view, name='login_view'),
    url(r'^not_logged_in/$', not_logged_in, name='not_logged_in'),
    url(r'^permissioned_denied/$', permission_denied, name='permission_denied'),
    url(r'^all_locked/$', all_locked, name='all_locked'),
    url(r'^healthcheck/$', healthcheck, name='healthcheck'),

    url(r'^allergy_form_view/$', allergy_form_view, name='allergy_form_view'),
    url(r'^health_concern_form_view/$', health_concern_form_view,
        name='health_concern_form_view'),
    url(r'^immunization_form_view/$', immunization_form_view,
        name='immunization_form_view'),
    url(r'^lab_test_form_view/$', lab_test_form_view, name='lab_test_form_view'),
    url(r'^medication_form_view/$', medication_form_view,
        name='medication_form_view'),
    url(r'^patient_form_view/$', patient_form_view, name='patient_form_view'),
    url(r'^problem_form_view/$', problem_form_view, name='problem_form_view'),
    url(r'^procedure_form_view/$', procedure_form_view, name='procedure_form_view'),
    url(r'^test_form_view/$', test_form_view, name='test_form_view'),

    path(r'patient_edit_form_view/<int:id>',
         patient_edit_form_view, name='patient_edit_form_view'),
    path(r'patient_encounter_form_view/<int:id>',
         patient_encounter_form_view, name='patient_encounter_form_view'),
    path(r'encounter_edit_form_view/<int:patient_id>/<int:encounter_id>',
         encounter_edit_form_view, name='encounter_edit_form_view'),
        
    path(r'referral_form/<int:id>', referral_form_view, name='referral_form_view'),

    url(r'^allergy_list_view/$', allergy_list_view, name='allergy_list_view'),
    url(r'^health_concern_list_view/$', health_concern_list_view,
        name='health_concern_list_view'),
    url(r'^immunization_list_view/$', immunization_list_view,
        name='immunization_list_view'),
    url(r'^lab_test_list_view/$', lab_test_list_view, name='lab_test_list_view'),
    url(r'^medication_list_view/$', medication_list_view,
        name='medication_list_view'),

    url(r'^patient_list_view/$', patient_list_view, name='patient_list_view'),
    url(r'^patient_csv_export_view/$', patient_csv_export_view, name='patient_csv_export_view'),
    url(r'^search_patient_list_view/$', search_patient_list_view,
        name='search_patient_list_view'),
    url(r'^filter_patient_list_view/$', filter_patient_list_view,
        name='filter_patient_list_view'),

    url(r'^problem_list_view/$', problem_list_view, name='problem_list_view'),
    url(r'^procedure_list_view/$', procedure_list_view, name='procedure_list_view'),
    url(r'^test_list_view/$', test_list_view, name='test_list_view'),

    url(r'^superuser_home/$', admin_home, name="superuser_home"),
    url(r'^set_timezone/$', set_timezone, name="set_timezone"),

    # User Management
    url(r'^list_users_view/$', list_users_view, name='list_users_view'),
    url(r'^create_user_view/$', create_user_view, name='create_user_view'),
    path(r'update_user_view/<int:id>',
         update_user_view, name='update_user_view'),
    path(r'update_user_password_view/<int:id>',
         update_user_password_view, name='update_user_password_view'),
    path(r'lock_users_view/<int:id>', lock_user_view, name='lock_user_view'),
    path(r'unlock_users_view/<int:id>',
         unlock_user_view, name='unlock_user_view'),
    url(r'^filter_users_view/$', filter_users_view, name='filter_user_view'),
    url(r'^search_users_view/$', search_users_view, name='search_user_view'),

    path(r'lock_instance_view/<int:id>', lock_instance_view, name='lock_instance_view'),
    path(r'unlock_instance_view/<int:id>', unlock_instance_view, name='unlock_instance_view'),

    path(r'lock_campaign_view/<int:id>', lock_campaign_view, name='lock_campaign_view'),
    path(r'unlock_campaign_view/<int:id>', unlock_campaign_view, name='unlock_campaign_view'),

    # Audit Log Management
    url(r'^get_audit_logs_view/$', get_audit_logs_view, name='get_audit_logs_view'),
    url(r'^export_audit_logs_view/$', export_audit_logs_view,
        name='export_audit_logs_view'),
    url(r'^filter_audit_logs_view/$', filter_audit_logs_view,
        name='filter_audit_logs_view'),
    url(r'^search_audit_logs_view/$', search_audit_logs_view,
        name='search_audit_logs_view'),

    # Database Log Management
    url(r'^get_database_logs_view/$', get_database_logs_view,
        name='get_database_logs_view'),
    url(r'^export_database_logs_view/$', export_database_logs_view,
        name='export_database_logs_view'),
    url(r'^search_database_logs_view/$', search_database_logs_view,
        name='search_database_logs_view'),
    url(r'^filter_database_logs_view/$', filter_database_logs_view,
        name='filter_database_logs_view'),

    # fEMR Environment Management
    url(r'^femr_admin_home/$', femr_admin_home, name='femr_admin_home'),
    url(r'^change_campaign/$', change_campaign, name='change_campaign'),
    url(r'^list_campaign/$', list_campaign_view, name='list_campaign'),
    path(r'edit_campaign/<int:id>', edit_campaign_view, name='edit_campaign'),
    url(r'^new_campaign/$', new_campaign_view, name='new_campaign'),
    url(r'^list_instance/$', list_instance_view, name='list_instance'),
    path(r'edit_instance/<int:id>', edit_instance_view, name='edit_instance'),
    url(r'^new_instance/$', new_instance_view, name='new_instance'),
    path(r'edit_contact/<int:id>', edit_contact_view, name='edit_contact'),
    url(r'^new_contact/$', new_contact_view, name='new_contact'),
    path(r'patient_export/<int:id>', patient_export_view, name='patient_export'),

    path(r'add_users_to_campaign', add_users_to_campaign, name='add_users_to_campaign'),
    path(r'add_user_to_campaign/<int:user_id>', add_user_to_campaign, name='add_user_to_campaign'),
    path(r'cut_user_from_campaign/<int:user_id>', cut_user_from_campaign, name='cut_user_from_campaign'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token,
        name='get_auth_token'),

    url(r'^forgot_username', forgot_username, name='forgot_username'),
]
