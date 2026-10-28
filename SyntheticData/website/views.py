from django.shortcuts import render, HttpResponse
import json
from .SyntheticApp import Data_Types
from .SyntheticApp import generate_data
from faker import Faker
import inspect

# Data Type List
a = Data_Types(Faker('en_GB'))
attr_list = []

for name, func in inspect.getmembers(Data_Types, predicate=inspect.isfunction):
    if not name.startswith("_"):
        attr_list.append(name)

# Manually include Id as the only non-function
attr_list.append("Id")

# Create your views here.
def home(request):
    """
    This view connects the front end Javascript
    to the back end python by structuring the logic
    for POST (user requests synthetic data) and 
    GET (user loads the home page) requests.
    """
    var = {'node': 'yes'}
    
    if request.method == "POST":    # Submit Synthetic dataset request
        # Converting Data into list arguments
        column_name_array = request.POST.getlist("column_name")
        data_type_array = [w.replace(' ', '_') for w in request.POST.getlist('data_type')]
        num_of_entries = int(request.POST['num_of_entries'])
        format_list = request.POST.getlist("format_option")
        blank_perc_list = [int(w) for w in request.POST.getlist('blankPercent')]
        bad_data_list = request.POST.getlist("badData")
        file_type = str(request.POST['file_type'])

        print(data_type_array)
        
        # Generate Data
        file_name = generate_data(num_of_entries,column_name_array,data_type_array,format_list,blank_perc_list,bad_data_list,file_type)
       
        if file_type == 'csv':
            content_type = 'document'
            mode = "rt"
        elif file_type == 'excel':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            mode = "rb"
        elif file_type == 'json':
            content_type = 'application/json'
            mode = "rt"
        elif file_type == 'xml':
            content_type = 'application/xml'
            mode = "rb"

        with open(file_name, mode =mode) as file:
            #TODO: Configure content type to each specific file type
            try:
                response = HttpResponse(file,content_type=content_type)
            except Exception as e:
                print(e)
            response['Content-Disposition'] = f'''attachment; filename="{file_name}"'''

            return response

    else:   # Home page - get request
        # Data Type List
        with open('static/website/js/attr_list.js', 'w') as out_file:
            out_file.write('var attr_list = %s;' % json.dumps(attr_list))

        return render(request, 'home.html', {"my_data": var, "active_page": "home"})


def about(request):
    """
    Loads the about page
    """
    return render(request, "about.html",{"active_page": "about"})

def salesforce(request):
    """
    Loads the salesforce page
    Generates account data for the poc
    """
    # Preview lists shown in the UI so users can see
    # which columns are generated for each option
    business_mandatory_fields = [
        "Account Name",
    ]

    business_all_fields = business_mandatory_fields + [
        "Phone",
        "Fax",
        "Type",
        "Industry",
        "Website",
        "Description",
        "Employees",
        "Annual Revenue",
        "Billing Street",
        "Billing City",
        "Billing State/Province",
        "Billing Zip/Postal Code",
        "Billing Country",
        "Shipping Street",
        "Shipping City",
        "Shipping State/Province",
        "Shipping Zip/Postal Code",
        "Shipping Country",
    ]

    person_mandatory_fields = [
        "Last Name",
    ]

    person_all_fields = [
        "Salutation",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Fax",
        "Website",
        "Type",
        "Industry",
        "Employees",
        "Annual Revenue",
        "Description",
        "Billing Street",
        "Billing City",
        "Billing State/Province",
        "Billing Zip/Postal Code",
        "Billing Country",
        "Shipping Street",
        "Shipping City",
        "Shipping State/Province",
        "Shipping Zip/Postal Code",
        "Shipping Country",
    ]

    # Shared metadata for account-style fields (used by Account and
    # Contact variants) so we can generate consistent data types and
    # formats across objects.
    account_field_meta = {
        "Salutation": ("Multiple_Choice", "Mr.,Ms.,Mrs.,Dr.,Prof.,Mx."),
        "First Name": ("Name", "firstName"),
        "Email": ("Email", ""),
        "Phone": ("Phone_Number", "Phone Number"),
        "Fax": ("Phone_Number", "Phone Number"),
        "Website": ("Website", ""),
        "Type": (
            "Multiple_Choice",
            "Analyst,Competitor,Customer,Integrator,Investor,Partner,Press,Prospect,Reseller,Other",
        ),
        "Industry": (
            "Multiple_Choice",
            "Agriculture,Apparel,Banking,Biotechnology,Chemicals,Communications,Construction,Consulting,Education,Electronics,Energy,Engineering,Entertainment,Environmental,Finance,Food & Beverage,Government,Healthcare,Hospitality,Insurance,Machinery,Manufacturing,Media,Not For Profit,Other,Recreation,Retail,Shipping,Technology,Telecommunications,Transportation,Utilities",
        ),
        "Employees": ("Number", "0,1000"),
        "Annual Revenue": ("Number", "0,100000000"),
        "Description": ("Text", ""),
        "Billing Street": ("Address", "addressLine1"),
        "Billing City": ("City", ""),
        "Billing State/Province": ("City", ""),
        "Billing Zip/Postal Code": ("Address", "postcode"),
        "Billing Country": ("Country", ""),
        "Shipping Street": ("Address", "addressLine1-new"),
        "Shipping City": ("City", ""),
        "Shipping State/Province": ("City", ""),
        "Shipping Zip/Postal Code": ("Address", "postcode"),
        "Shipping Country": ("Country", ""),
    }

    lead_mandatory_fields = [
        "Last Name",
        "Company",
        "Lead Status",
    ]

    lead_all_fields = [
        "Salutation",
        "First Name",
        "Last Name",
        "Company",
        "Title",
        "Phone",
        "Email",
        "Rating",
        "Lead Status",
        "Street",
        "City",
        "State/Province",
        "Zip/Postal Code",
        "Country",
        "Website",
        "No. of Employees",
        "Annual Revenue",
        "Lead Source",
        "Industry",
        "Description",
    ]

    contact_mandatory_fields = [
        "Last Name",
        "Account Name",
    ]

    # Contact "all fields" variants build on the account field sets.
    person_all_without_last = [f for f in person_all_fields if f != "Last Name"]
    business_rest_fields = business_all_fields[1:]  # drop Account Name (already mandatory)

    # Contact - Person: mandatory contact fields + all Person Account fields
    # except Last Name (which is already included as the contact Last Name).
    contact_all_person_fields = contact_mandatory_fields + person_all_without_last

    # Contact - Business: mandatory contact fields + all Business Account
    # fields except Account Name (already included as the contact Account Name).
    contact_all_business_fields = contact_mandatory_fields + business_rest_fields

    # Contact - Both: mandatory contact fields + union of all Person and
    # Business Account fields (excluding Parent/Active and de-duplicated
    # while preserving order).
    seen = set()
    contact_all_both_fields = []
    for name in contact_mandatory_fields + person_all_fields + business_all_fields:
        if name in ("Parent Account", "Active"):
            continue
        if name not in seen:
            seen.add(name)
            contact_all_both_fields.append(name)

    # Default previews (business account)
    mandatory_fields_preview = business_mandatory_fields
    all_fields_preview = business_all_fields

    field_previews = json.dumps({
        "business": {
            "mandatory": business_mandatory_fields,
            "all": business_all_fields,
        },
        "person": {
            "mandatory": person_mandatory_fields,
            "all": person_all_fields,
        },
        "lead": {
            "mandatory": lead_mandatory_fields,
            "all": lead_all_fields,
        },
        "contact": {
            "mandatory": contact_mandatory_fields,
            "all_person": contact_all_person_fields,
            "all_business": contact_all_business_fields,
            "all_both": contact_all_both_fields,
        },
    })

    if request.method == "POST":
        num_of_entries = int(request.POST['num_of_entries'])
        mode = request.POST['mode']
        parent_account = (request.POST.get('parent_account') or "").strip()
        active_flag = request.POST.get('active')
        sf_object = request.POST.get('sf_object', '')

        # Base arrays vary by selected object
        if sf_object == "Account - Person":
            # Person Account - Mandatory vs All Standard
            if mode == "all_fields":
                column_name_array = person_all_fields.copy()

                data_type_array = [
                    "Multiple_Choice",  # Salutation
                    "Name",             # First Name
                    "Name",             # Last Name
                    "Email",
                    "Phone_Number",
                    "Phone_Number",
                    "Website",
                    "Multiple_Choice",  # Type
                    "Multiple_Choice",  # Industry
                    "Number",
                    "Number",
                    "Text",
                    "Address",
                    "City",
                    "City",
                    "Address",
                    "Country",
                    "Address",
                    "City",
                    "City",
                    "Address",
                    "Country",
                ]

                format_list = [
                    "Mr.,Ms.,Mrs.,Dr.,Prof.,Mx.",
                    "firstName",
                    "lastName",
                    "",
                    "Phone Number",
                    "Phone Number",
                    "",
                    "Analyst,Competitor,Customer,Integrator,Investor,Partner,Press,Prospect,Reseller,Other",
                    "Agriculture,Apparel,Banking,Biotechnology,Chemicals,Communications,Construction,Consulting,Education,Electronics,Energy,Engineering,Entertainment,Environmental,Finance,Food & Beverage,Government,Healthcare,Hospitality,Insurance,Machinery,Manufacturing,Media,Not For Profit,Other,Recreation,Retail,Shipping,Technology,Telecommunications,Transportation,Utilities",
                    "0,1000",
                    "0,100000000",
                    "",
                    "addressLine1",
                    "",
                    "",
                    "postcode",
                    "",
                    "addressLine1-new",
                    "",
                    "",
                    "postcode",
                    "",
                ]
            else:
                # Mandatory only: Last Name using existing Name logic
                column_name_array = ["Last Name"]
                data_type_array = ["Name"]
                format_list = ["lastName"]

        elif sf_object == "Contact":
            contact_all_type = request.POST.get("contact_all_type")

            if mode == "all_fields" and contact_all_type in ("person", "business", "both"):
                # Choose the appropriate Contact all-fields variant
                if contact_all_type == "person":
                    column_name_array = contact_all_person_fields.copy()
                elif contact_all_type == "business":
                    column_name_array = contact_all_business_fields.copy()
                else:
                    column_name_array = contact_all_both_fields.copy()

                data_type_array = []
                format_list = []

                for name in column_name_array:
                    if name == "Last Name":
                        data_type_array.append("Name")
                        format_list.append("lastName")
                    elif name == "Account Name":
                        data_type_array.append("Company")
                        format_list.append("")
                    else:
                        dtype, fmt = account_field_meta.get(name, ("Text", ""))
                        data_type_array.append(dtype)
                        format_list.append(fmt)
            else:
                # Contact – mandatory only: Last Name + Account Name
                column_name_array = contact_mandatory_fields.copy()
                data_type_array = [
                    "Name",     # Last Name
                    "Company",  # Account Name
                ]
                format_list = [
                    "lastName",
                    "",
                ]

        elif sf_object == "Lead":
            # Lead behaviour based on New Lead layout
            if mode == "all_fields":
                column_name_array = lead_all_fields.copy()

                data_type_array = [
                    "Multiple_Choice",  # Salutation
                    "Name",             # First Name
                    "Name",             # Last Name
                    "Company",          # Company
                    "Title",            # Title (derived from salutation)
                    "Phone_Number",     # Phone
                    "Email",            # Email
                    "Multiple_Choice",  # Rating
                    "Multiple_Choice",  # Lead Status
                    "Address",          # Street
                    "City",             # City
                    "City",             # State/Province
                    "Address",          # Zip/Postal Code
                    "Country",          # Country
                    "Website",          # Website
                    "Number",           # No. of Employees
                    "Number",           # Annual Revenue
                    "Multiple_Choice",  # Lead Source
                    "Multiple_Choice",  # Industry
                    "Text",             # Description
                ]

                format_list = [
                    "Mr.,Ms.,Mrs.,Dr.,Prof.,Mx.",
                    "firstName",
                    "lastName",
                    "",
                    "",
                    "Phone Number",
                    "",
                    "Hot,Warm,Cold",
                    "New,Contacted,Nurturing,Qualified,Unqualified",
                    "addressLine1",
                    "",
                    "",
                    "postcode",
                    "",
                    "",
                    "0,1000",
                    "0,100000000",
                    "Advertisement,Employee Referral,External Referral,Partner,Public Relations,Seminar - Internal,Seminar - Partner,Trade Show,Web,Word of mouth,Other",
                    "Agriculture,Apparel,Banking,Biotechnology,Chemicals,Communications,Construction,Consulting,Education,Electronics,Energy,Engineering,Entertainment,Environmental,Finance,Food & Beverage,Government,Healthcare,Hospitality,Insurance,Machinery,Manufacturing,Media,Not For Profit,Other,Recreation,Retail,Shipping,Technology,Telecommunications,Transportation,Utilities",
                    "",
                ]
            else:
                # Mandatory only: Last Name, Company, Lead Status
                column_name_array = lead_mandatory_fields.copy()
                data_type_array = [
                    "Name",            # Last Name
                    "Company",         # Company
                    "Multiple_Choice", # Lead Status
                ]
                format_list = [
                    "lastName",
                    "",
                    "New,Contacted,Nurturing,Qualified,Unqualified",
                ]

        else:
            # Business Account behaviour (existing logic)
            column_name_array = business_mandatory_fields.copy()
            data_type_array = ["Company"]
            format_list = [""]

            # parent account (optional)
            if parent_account != "":
                column_name_array.append("Parent Account")
                data_type_array.append("Multiple_Choice")
                format_list.append(parent_account)

            # if 'all' selected, arrays are extended
            if mode == "all_fields":
                column_name_array += business_all_fields[1:]  # exclude Account Name already included

                data_type_array += [
                    "Phone_Number",
                    "Phone_Number",
                    "Multiple_Choice",
                    "Multiple_Choice",
                    "Website",
                    "Text",
                    "Number",
                    "Number",
                    "Address",
                    "City",
                    "City",
                    "Address",
                    "Country",
                    "Address",
                    "City",
                    "City",
                    "Address",
                    "Country",
                ]

                format_list += [
                    "Phone Number",
                    "Phone Number",
                    "Analyst,Competitor,Customer,Integrator,Investor,Partner,Press,Prospect,Reseller,Other",
                    "Agriculture,Apparel,Banking,Biotechnology,Chemicals,Communications,Construction,Consulting,Education,Electronics,Energy,Engineering,Entertainment,Environmental,Finance,Food & Beverage,Government,Healthcare,Hospitality,Insurance,Machinery,Manufacturing,Media,Not For Profit,Other,Recreation,Retail,Shipping,Technology,Telecommunications,Transportation,Utilities",
                    "",
                    "",
                    "0,1000",
                    "0,100000000",
                    "addressLine1",
                    "",
                    "",
                    "postcode",
                    "",
                    "addressLine1-new",
                    "",
                    "",
                    "postcode",
                    "",
                ]

            # Active column (optional via checkbox) – business accounts only
            if active_flag:
                column_name_array.append("Active")
                data_type_array.append("Multiple_Choice")
                format_list.append("TRUE")

        # Add custom fields if provided
        custom_field_labels = request.POST.getlist("custom_field_label")
        custom_data_types = request.POST.getlist("custom_data_type")
        custom_format_options = request.POST.getlist("custom_format_option")

        if custom_field_labels:  # if any custom fields were added
            column_name_array.extend(custom_field_labels)
            data_type_array.extend([w.replace(' ', '_') for w in custom_data_types])
            format_list.extend(custom_format_options)

        blank_perc_list = [0]*len(column_name_array)
        bad_data_list = ['no']*len(column_name_array)

        file_name = generate_data(
            num_of_entries,
            column_name_array,
            data_type_array,
            format_list,
            blank_perc_list,
            bad_data_list,
            "csv"
        )

        with open(file_name, mode = "rt") as file:
            try:
                response = HttpResponse(file,content_type="document")
            except Exception as e:
                print(e)
            response['Content-Disposition'] = f'''attachment; filename="{file_name}"'''
            return response
        
    return render(
        request,
        "salesforce.html",
        {
            "active_page": "salesforce",
            "mandatory_fields_preview": mandatory_fields_preview,
            "all_fields_preview": all_fields_preview,
            "field_previews": field_previews,
        },
    )