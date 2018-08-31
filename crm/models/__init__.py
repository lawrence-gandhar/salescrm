from __future__ import unicode_literals
from django.db import models

from crm.models.users import User_usertype, Usertype
from crm.models.leads import Leads_tbl, Lead_type, Lead_line_of_business, Lead_payment_type, Lead_probability
from crm.models.leads import Lead_status, Lead_program_requirement, Lead_call_purpose, Lead_pricing_model, Lead_questionnaire_model