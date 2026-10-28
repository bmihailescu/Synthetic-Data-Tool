import csv
import os
import datetime
from datetime import date
import random
import secrets
from random import randint
import string
from faker import Faker
import random
from optparse import OptionParser
from itertools import count
import pandas as pd
import exrex


## Define functions for random generation of data

def csv_array_reader(csv_file):
    """    Read in a single column csv as an array    """
    list_csv = []
    with open(csv_file) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            list_csv.append(row[0])
    return list_csv

def POST_CODE(self):
    """
    Returns a random postcode
    """
    return self.address[-1]

def fake_name(fake_var):
    """
    Generate a fake name and gender
    -Run faker
    -Generate a fake prefix
    -Use the prefix as a driver for name creation from gendered names
    """
    fake_prefix = [fake_var.prefix(), fake_var.prefix_female(), fake_var.prefix_male()]
    fake_prefix = random.choice(fake_prefix)

    if fake_prefix in ['Miss.', 'Mrs.', 'Miss', 'Mrs', 'Ms', 'Ms.']:
        fake_first_name = fake_var.first_name_female()
        GENDER = random.choice(['FEMALE', 'NON BINARY'])

    elif fake_prefix in ['Mr', 'Mr.']:
        fake_first_name = fake_var.first_name_male()
        GENDER = random.choice(['MALE', 'NON BINARY'])

    else:
        fake_first_name = fake_var.first_name()
        GENDER = random.choice(['MALE', 'FEMALE', 'NON BINARY'])

    fake_last_name = fake_var.last_name()

    return [fake_prefix, fake_first_name, fake_last_name, GENDER]

def MOBILE(fake_var):
    """
    Returns a random mobile number
    """
    mobile = fake_var.cellphone_number()
    mobile = ''.join(char for char in mobile if char.isalnum())
    return mobile

def csv_dict_reader(csv_file):
    """
    Read in a 2 columns csv and store as a dictionary
    Use column 1 as the key
    """
    dict_csv = {}
    dict_csv = {}
    with open(csv_file) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            dict_csv[row[0]] = row[1]
    return dict_csv

########################################################################################################################

id_count = 1

class Data_Types():

    _ids=count(0)

    def __init__(self,fake_var):
        """
        Initialises selected variables before 
        / outside the main function calls
        """
        self.Id = ""
        self._cached_credit_card = {}
        self._cached_name = {}
        self._cached_currency = {}
        self._cached_address = {}
        self._cached_bank_account = {}
        self._cached_salutation = None
        self._generated_passwords = set()
        self.mc_column_tracker = {}                                                      # dictionary for each multiple choice column

    def _clear_caches(self):
        """
        Clears all cached data to ensure new values are generated for a new row.
        """
        self._cached_credit_card = {}
        self._cached_name = {}
        self._cached_currency = {}
        self._cached_address = {}
        self._cached_bank_account = {}
        self._cached_salutation = None

    def Multiple_Choice(self,fake_var,format,col):
        """
        User provides possible options via the frontend,
        this method returns items from the user's inputted
        options at random. Additionally, ensures that for each
        Multiple_Choice column, all options are used at least once
        before any repetition. When the standard salutation list is
        used, the chosen value is cached for use by Title().
        """

        # Initialise tracking for this column if needed
        if col not in self.mc_column_tracker:
            mc_string = format
            all_mc_options = [option.strip() for option in mc_string.split(',')]
            self.mc_column_tracker[col] = {
                'all_options': all_mc_options,
                'remaining_mc_options_required': random.sample(all_mc_options, len(all_mc_options)),
            }

        tracker = self.mc_column_tracker[col]

        # Use each option at least once before repeating
        if tracker['remaining_mc_options_required']:
            value = tracker['remaining_mc_options_required'].pop(0)
        else:
            value = random.choice(tracker['all_options'])

        # Cache salutation when using the standard salutation list
        # so that downstream fields (e.g. Title) can derive values.
        if format == "Mr.,Ms.,Mrs.,Dr.,Prof.,Mx.":
            self._cached_salutation = value

        return value

    def String(self,fake_var,format):
        """
        Join letters together for a
        random string of defined length
        """
        letters = string.ascii_letters
        return ''.join(random.choices(letters, k=int(format)))
    
    def Phone_Number(self, fake_var, format):
        """
        Generates mobile numbers, phone numbers and area codes
        """
        if format == "Mobile Number": return MOBILE(fake_var)
        if format == "areaCode": return  fake_var.country_calling_code()
        if format == "Phone Number": return  fake_var.phone_number()

    def Website(self,fake_var):
        """
        Returns a random website generated by faker
        """
        return fake_var.url()

    def Number(self,fake_var,format):
        """
        Randomly generates a number based on
        a minimum and maximum integer
        """
        min = int(format.split(",")[0])
        max = int(format.split(",")[1])
        return randint(min,max)

    def Company(self,fake_var):
        """
        Returns a random company name generated by faker
        """
        return fake_var.company()

    def Password(self,fake_var):
        """
        Returns a unique password meeting common password rules.
        """
        special_characters = "!@#$%^&*()-_=+[]{};:,.<>?"
        all_characters = string.ascii_letters + string.digits + special_characters

        while True:
            password_characters = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(special_characters),
            ]
            password_characters.extend(secrets.choice(all_characters) for _ in range(8))
            random.shuffle(password_characters)
            password = ''.join(password_characters)

            if password not in self._generated_passwords:
                self._generated_passwords.add(password)
                return password

    def Title(self, fake_var):
        """
        Derive a lead Title from the cached salutation.
        - If salutation is 'Dr.'  -> 'Doctor'
        - If salutation is 'Prof.' -> 'Professor'
        - Otherwise               -> 'N/A'
        """
        sal = self._cached_salutation or ""
        if sal == "Dr.":
            return "Doctor"
        if sal == "Prof.":
            return "Professor"
        return "N/A"

    def Email(self,fake_var):
        """
        Returns a random email generated by faker.
        If a name has already been generated and cached via Name(),
        reuse that name in the local-part (before the "@") in either
        firstName+lastName or lastName+firstName order (no spaces),
        converted to lowercase and followed by a 1–4 digit number.
        """
        base_email = fake_var.email()

        # If we don't have a cached name yet, just return the faker email
        if not self._cached_name:
            return base_email

        # Split the faker email into local-part and domain
        _local, sep, domain = base_email.partition("@")
        if not sep:  # safety: malformed email from faker
            return base_email

        first = self._cached_name.get("firstName", "") or ""
        last = self._cached_name.get("lastName", "") or ""

        if not first and not last:
            return base_email

        # Randomly choose name order: firstName lastName OR lastName firstName
        if random.choice([True, False]):
            name_part = f"{first}{last}"
        else:
            name_part = f"{last}{first}"

        # normalise to lowercase for email local-part
        name_part = name_part.replace(" ", "").lower()

        # Append a 1–4 digit random number
        digits_len = random.randint(1, 4)
        digits = "".join(random.choice(string.digits) for _ in range(digits_len))

        # Use the constructed local-part with the original domain (no spaces)
        new_local = f"{name_part}{digits}"
        return f"{new_local}@{domain}"

    def Address(self,fake_var,format):
        """
        Prerequisites:Instantiate Faker for UK addresses and names
        Generates full addresses, address lines and postcodes
        """
        if "-new" in format:
            self._cached_address = {}
            format = format.replace("-new","")
        if not self._cached_address:
            full_address = fake_var.address()
            address_array = full_address.split('\n')
            postcode = address_array[-1]

            self._cached_address["fullAddress"] = f"{address_array[0]} {address_array[1]} {postcode}"
            self._cached_address["addressLine1"] = address_array[0]
            self._cached_address["addressLine2"] = address_array[1] if len(address_array) > 2 else ""
            self._cached_address["postcode"] = postcode

        return self._cached_address.get(format, self._cached_address["fullAddress"])
    
    def City(self,fake_var):
        """
        Returns a random UK city generated by faker
        """
        return fake_var.city()
    
    def County(self,fake_var):
        """
        Returns a random UK county generated by faker
        """
        return fake_var.county()
    
    def Country(self,fake_var):
        """
        Returns a random country generated by faker
        """
        return fake_var.country()

    def Banking(self, fake_var, format):
        """
        Generates a consistent SWIFT, sort code, account number and IBAN.
        Details can be requested entirely or separately via format input.
        """
        if not self._cached_bank_account:
            country_code = "GB"
            check_digits = f"{fake_var.random_int(min=2, max=98):02d}"

            bank_code = fake_var.lexify(text='????').upper()
            location_code = fake_var.lexify(text='??').upper()
            swift = f"{bank_code}{country_code}{location_code}"

            sort_code = ''.join([str(fake_var.random_digit()) for _ in range(6)])
            sort_code_display = f"{sort_code[:2]}-{sort_code[2:4]}-{sort_code[4:]}"
            account_number = ''.join([str(fake_var.random_digit()) for _ in range(8)])

            iban = f"{country_code}{check_digits}{sort_code}{account_number}"

            self._cached_bank_account["iban"] = iban
            self._cached_bank_account["swift"] = swift
            self._cached_bank_account["sort_code"] = sort_code_display
            self._cached_bank_account["account_number"] = account_number

        return self._cached_bank_account.get(format, self._cached_bank_account["iban"])

    def Date(self, fake_var, format):
        """
        Get a date at a proportion of a range of two formatted dates.
        start and end should be strings specifying dates formatted in the
        given format, giving an interval [start, end].
        The returned date will be in the specified format.
        """
        date_format = format.split(",")[0]

        start = datetime.datetime.strptime(format.split(",")[1],'%Y-%m-%d')
        end = datetime.datetime.strptime(format.split(",")[2],'%Y-%m-%d')
        date = fake_var.date_time_between( start_date = start,end_date = end,tzinfo=None)
        date = datetime.datetime.strftime(date, date_format)
        return date

    def Name(self,fake_var,format):
        """
        Return a random name from faker
        """
        if not self._cached_name:
            first = fake_var.first_name()
            last = fake_var.last_name()
            full = f"{first} {last}"
            self._cached_name = {
                "firstName": first,
                "lastName": last,
                "fullName": full
            }

        return self._cached_name.get(format, "")

    def Job(self,fake_var):
        """
        Return a random job from faker
        """
        return fake_var.job()

    def Text(self,fake_var,format):
        """
        Return a random word from faker
        """
        words = fake_var.text()
        if format == "": return words
        else: return ' '.join(words.split()[:int(format)])
    
    def NINO(self,fake_var):
        """
        Return a realistic UK NINO
        """
        prefixes = ['AB', 'CD', 'EF', 'GH', 'JK', 'LM', 'MN', 'NP', 'PQ', 'QQ', 'RT', 'WX', 'YZ']
        suffixes = ['A', 'B', 'C', 'D']

        return (
            random.choice(prefixes) +
            f"{random.randint(0, 99):02}" +
            f"{random.randint(0, 99):02}" +
            f"{random.randint(0, 99):02}" +
            random.choice(suffixes)
        )

    def Number_Plate(self,fake_var):
        """
        Return a random licence plate
        """
        return fake_var.license_plate()
    
    def Credit_Card(self,fake_var,format):
        """
        Return random credit card data from faker
        The initally empty cached credit card is
        populated in segments via the relevant faker calls
        """
        if not self._cached_credit_card:
            number = fake_var.credit_card_number()
            provider = fake_var.credit_card_provider()
            cvc = fake_var.credit_card_security_code()
            expiry = fake_var.credit_card_expire()
            fullDetails = f"{provider}\n{number} {expiry}\nCVC: {cvc}"

            self._cached_credit_card = {
                "fullDetails": fullDetails,
                "cardNumber": number,
                "cardProvider": provider,
                "securityCode": cvc,
                "expiryDate": expiry
            }

        return self._cached_credit_card.get(format)

    def Currency(self,fake_var,format):
        """
        Return random currency data from faker
        The initally empty cached currency is
        populated in segments via the relevant faker calls
        for uniformity
        """
        if not self._cached_currency:
            ccy_tuple = fake_var.currency()
            print(ccy_tuple)
            ccy_code, ccy_name = ccy_tuple
            self._cached_currency = {
                "ccyCodeAndName": f"{ccy_code}\n {ccy_name}",
                "ccyCode": ccy_code,
                "ccyName": ccy_name,
            }
        
        return self._cached_currency.get(format, "")

      

########################################################################################################################

def generate_data(num_of_entries,column_name_array,data_type_array,format_list,blank_perc_list,bad_data_list,file_type):
    """
    Facilitates the return of the given data type
    as a given file type as input by the user
    """
    fake_var = Faker('en_GB')

    listoflists = []
    dummy_fields = Data_Types(fake_var)

    for i in range(num_of_entries+1):   #iterate over rows
        if i == 0:  #column name row
            print(column_name_array)
        else:   #data rows                 
            SETL_info =[]
            num_of_m_choice = 0
            dummy_fields._clear_caches()

            # iterate over every data type selected
            for col in range(len(data_type_array)):
                attr = data_type_array[col]

                #blank values
                blank_perc = blank_perc_list[col]
                blank_perc = max(min(100, blank_perc), 0)  #restrict percent 0-100
                is_cell_blank = random.choices([True, False],[blank_perc,100-blank_perc],k=1)[0]

                value = "" # Initialize value to blank, will be overwritten if not blank
    
                # --- Conditional Data Generation ---
                if not is_cell_blank: # Only generate data if the cell is NOT blank
                # This list defines ALL data types that consume an entry from format_list
                    if attr in ["Date", "Address", "Name", "Number", "String", "Text", "Regex", "Credit_Card", "Currency", "Phone_Number", "Banking"]:
                        method = getattr(dummy_fields,attr)
                        value = method(fake_var,format_list[num_of_m_choice])
                    elif attr == "Multiple_Choice":
                        method = getattr(dummy_fields,attr)
                        value = method(fake_var,format_list[num_of_m_choice],col)
                    elif attr == "Id":
                        value = i
                    else:
                        method = getattr(dummy_fields,attr)
                        if isinstance(method,str):
                            value = method
                        else:
                            value = method(fake_var)
                num_of_m_choice+=1

                # Bad Data
                
                bad_data_level = bad_data_list[col]
                if (attr == "Id" or attr == "Number" or attr == "Password") or bad_data_level == "0": pass
                elif bad_data_level == "1": 
                    bad_char = [""," "]
                    value = random.choice(bad_char) + random.choice(bad_char) + value + random.choice(bad_char) + random.choice(bad_char)
                elif bad_data_level == "2": 
                    bad_char = [""," ",",","."]
                    value = random.choice(bad_char) + random.choice(bad_char) + value + random.choice(bad_char) + random.choice(bad_char)
                elif bad_data_level == "3": 
                    bad_char = [""," ",",","."";",":","@"]
                    value = random.choice(bad_char) + random.choice(bad_char) + value + random.choice(bad_char) + random.choice(bad_char)
                elif bad_data_level == "4": 
                    bad_char = [""," ",",","."";",":","@",chr(10),chr(160)]
                    value = ''.join('%s%s' % (x, random.choice(bad_char) if random.random() > 0.5 else '') for x in value)

                SETL_info.append(value)

            listoflists.append(SETL_info)

    df = pd.DataFrame(data=listoflists)
    df.columns=column_name_array

    #ensuring no account_names/company names are repeated
    for column_name in column_name_array:
        if column_name == "Account Name" or column_name == "Company": 

            suffixes = ["ltd", "plc", "llc", "inc"]                    # salesforce recognises same company names with an extra suffix as the same company
            df[column_name].str.lower                                  # making them all lowercase so we can use the duplicate function properly
            for suffix in suffixes:
                df[column_name].str.removesuffix(suffix).str.strip()   # replacing the company suffixes with nothing so that we have a uniform set of names

            while not df[column_name].is_unique:                       # checks that the column is unique, and if its NOT unique then the loop is triggered
                duplicated_array = df[column_name].duplicated()        # gives an array of true or false values
                duplicated_values = df.index[duplicated_array]        # gives the index/position of the true or false values
                for dup in duplicated_values:                         
                    df.loc[dup, column_name] = fake_var.company()      # locates the index in the column_name of a duplicated value and then replaces it with a new company
 
    if file_type == 'csv':
        file_name = 'SyntheticData.csv'
        df.to_csv(file_name,index=False)
    elif file_type == 'excel':
        file_name = 'SyntheticData.xlsx'
        df.to_excel(file_name,index=False)
    elif file_type == 'json':
        file_name = 'SyntheticData.json'
        df.to_json(file_name,'records')
    elif file_type == 'xml':
        file_name = 'SyntheticData.xml'
        df.to_xml(file_name)

    return file_name

# return csvfile
if __name__ == "__main__":
    x = generate_data(num_of_entries= 5,
                column_name_array=['Number_Plate','NINO'],
                data_type_array=["Number_Plate","NINO"],
                format_list=[],
                blank_perc_list=[0,0],
                bad_data_list=[0,0],
                file_type = 'json'
                )

    print(x)
