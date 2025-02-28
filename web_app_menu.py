import mysql.connector
from mysql.connector import Error
from funzioni_utili import esegui_query_parametrizzata, recupera_dati_completi
from datetime import datetime, date

# --- Database Menu ---
while True:
    print("--- INSURANCE DB ---")
    print("1) Add policy")
    print("2) Modify policy")
    print("3) Delete policy")
    print("4) Run query")
    print("0) Exit")

    choice = int(input("Choice: "))

    # --- Add Policy ---
    if choice == 1:
        try:
            # Enter client's personal data
            print("\nEnter the client's personal data.")
            name = input("Name: ")
            surname = input("Surname: ")
            birth_year = int(input("Birth year: "))
            mail = input("Email: ")

            # Add data to a list
            personal_data = [(name, surname, birth_year, mail)]
            print(personal_data)

            # Query to insert data into the database
            query_personal_data = """INSERT INTO Personal_Info (name, surname, birth_year, mail) 
                                     VALUES (%s, %s, %s, %s)"""
            for d in personal_data:
                esegui_query_parametrizzata(query_personal_data, d)

            # Retrieve the last inserted personal ID
            personal_id = recupera_dati_completi("SELECT LAST_INSERT_ID()")[0][0]

            # Enter client's medical data
            print("\nEnter the client's medical data.")
            age = 2025 - birth_year
            sex = input("Sex (Male/Female): ")
            bmi = float(input("Body mass index: "))
            children = int(input("Number of children: "))
            smoker = input("Smoker (Yes/No): ")
            region = input("Region (Northeast/Southeast/Northwest/Southwest): ")

            # Retrieve the region ID
            region_id = recupera_dati_completi(f"""SELECT regional_id FROM Regions WHERE name = '{region}'""")[0][0]

            # Add data to a list
            medical_data = [(age, sex, bmi, children, smoker, region_id)]
            print(medical_data)

            # Query to insert medical data
            query_medical_data = """INSERT INTO Clients (age, sex, bmi, children, smoker, id_region, id_personal) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            for d in medical_data:
                esegui_query_parametrizzata(query_medical_data, (*d, personal_id))  # d: tuple (treated as a single parameter)
                                                                                            # *d: unpacks the tuple 'd' into individual elements to pass them as parameters
                                                                                            # to a query (used when you need to add other parameters)
                                                                                            # The query requires 7 parameters (%) -> *d (6) and id_personal (1)

            # Enter insurance policy data
            print("\nEnter the insurance policy data.")
            charges = float(input("Charges: "))

            # Enter a start date that is not in the future
            while True:
                try:
                    start_date_input = input("Start date (YYYY-MM-DD): ")
                    year, month, day = map(int, start_date_input.split('-'))
                    start_date = date(year, month, day)

                    # Check that the start date is not in the future
                    if start_date > date.today():
                        print("The start date CANNOT be in the future. Enter a valid date.")
                    else:
                        break
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")

            # Calculate the end date of the policy
            try:
                end_date = start_date.replace(year=start_date.year + 1)
            except ValueError:
                # If the end date is invalid (e.g., February 29 in a non-leap year), set a valid date
                print("Error in end date. Setting a valid date.")
                end_date = date(start_date.year + 1, 3, 1)  # Set the end date to March 1 of the next year

            # Set whether the policy is active or expired
            if end_date > date.today():
                status = "active"
            else:
                status = "expired"

            # Add data to a list
            policy_data = [(charges, start_date, end_date, status)]
            print(policy_data)

            # Query to insert policy data
            query_policy_data = """INSERT INTO Policies (charges, start_date, end_date, status) 
                                   VALUES (%s, %s, %s, %s)"""
            for d in policy_data:
                esegui_query_parametrizzata(query_policy_data, d) # d, because the tuple contains all the values required by the query

        except Exception as e:
            print(f"Error while inserting data: {e}")

    # --- Modify Policy ---
    elif choice == 2:
        print("1. Update client's personal data")
        print("2. Update client's medical data")
        print("3. Update client's policy data")
        modify_choice = input("Choice: ")

        try:
            # Update personal data
            if modify_choice == "1":
                personal_id = input("Enter the client's ID to update: ")
                new_name = input("New name: ")
                new_surname = input("New surname: ")
                new_birth_year = int(input("New birth year: "))
                new_mail = input("New email: ")

                query_update_personal = """
                UPDATE Personal_Info 
                SET name = %s, surname = %s, birth_year = %s, mail = %s 
                WHERE personal_id = %s
                """
                esegui_query_parametrizzata(query_update_personal, (new_name, new_surname, new_birth_year, new_mail, personal_id))

            # Update medical data
            elif modify_choice == "2":
                client_id = input("Enter the client's ID to update: ")
                new_bmi = float(input("New BMI: "))
                new_smoker = input("New smoker status (yes/no): ")

                query_update_medical = """
                UPDATE Clients 
                SET bmi = %s, smoker = %s 
                WHERE client_id = %s
                """
                esegui_query_parametrizzata(query_update_medical, (new_bmi, new_smoker, client_id))

            # Update policy data
            elif modify_choice == "3":
                policy_id = input("Enter the policy ID to update: ")
                new_charges = float(input("New charges: "))
                new_status = input("New status (active/expired): ")

                query_update_policy = """
                UPDATE Policies 
                SET charges = %s, status = %s 
                WHERE policy_id = %s
                """
                esegui_query_parametrizzata(query_update_policy, (new_charges, new_status, policy_id))

        except Exception as e:
            print(f"Error while updating data: {e}")

    # --- Delete Policy ---
    elif choice == 3:
        print("1) Delete Personal Data")
        print("2) Delete Clients")
        print("3) Delete Policies")
        delete_choice = input("Choice: ")

        try:
            # Delete personal data
            if delete_choice == "1":
                personal_id = input("Enter the client's ID to delete: ")
                query_delete_personal = "DELETE FROM Personal_Info WHERE personal_id = %s"
                esegui_query_parametrizzata(query_delete_personal, (personal_id,))

            # Delete clients
            elif delete_choice == "2":
                client_id = input("Enter the client's ID to delete: ")
                query_delete_client = "DELETE FROM Clients WHERE client_id = %s"
                esegui_query_parametrizzata(query_delete_client, (client_id,))

            # Delete policies
            elif delete_choice == "3":
                policy_id = input("Enter the policy ID to delete: ")
                query_delete_policy = "DELETE FROM Policies WHERE policy_id = %s"
                esegui_query_parametrizzata(query_delete_policy, (policy_id,))

        except Exception as e:
            print(f"Error while deleting data: {e}")

    # --- Run Query ---
    elif choice == 4:
        print("1. Expired policies")
        print("2. Clients with income > 10000")
        print("3. Average age of smokers")
        print("4. Average clients per region")
        query_choice = input("Choice: ")

        try:
            # Expired policies
            if query_choice == "1":
                query = "SELECT * FROM Policies WHERE status = 'expired'"
                results = recupera_dati_completi(query)
                print("Expired policies:", results)

            # Clients with income > 10000
            elif query_choice == "2":
                query = "SELECT * FROM Clients WHERE charges > 10000"
                results = recupera_dati_completi(query)
                print("Clients with income > 10000:", results)

            # Average age of smokers
            elif query_choice == "3":
                query = "SELECT ROUND(AVG(age)) FROM Clients WHERE smoker = 'yes'"
                results = recupera_dati_completi(query)
                print("Average age of smokers:", results[0][0])

            # Average clients per region
            elif query_choice == "4":
                print("1. Average age of clients per region")
                print("2. Average BMI of clients per region")
                print("3. Average number of children per region")
                average_choice = input("Choice: ")

                # Average age per region
                if average_choice == "1":
                    query = """
                    SELECT Regions.name, ROUND(AVG(Clients.age)) AS average_age
                    FROM Clients
                    JOIN Regions ON Clients.id_region = Regions.regional_id
                    GROUP BY Regions.name
                    """
                    results = recupera_dati_completi(query)
                    print("Average age of clients per region:")
                    for region, average_age in results:
                        print(f"{region}: {average_age:.2f} years")

                # Average BMI per region
                elif average_choice == "2":
                    query = """
                    SELECT Regions.name, AVG(Clients.bmi) AS average_bmi
                    FROM Clients
                    JOIN Regions ON Clients.id_region = Regions.regional_id
                    GROUP BY Regions.name
                    """
                    results = recupera_dati_completi(query)
                    print("Average BMI of clients per region:")
                    for region, average_bmi in results:
                        print(f"{region}: {average_bmi:.2f}")

                # Average number of children per region
                elif average_choice == "3":
                    query = """
                    SELECT Regions.name, ROUND(AVG(Clients.children)) AS average_children
                    FROM Clients
                    JOIN Regions ON Clients.id_region = Regions.regional_id
                    GROUP BY Regions.name
                    """
                    results = recupera_dati_completi(query)
                    print("Average number of children per region:")
                    for region, average_children in results:
                        print(f"{region}: {average_children:.2f} children")

                else:
                    print("Invalid choice.")

        except Exception as e:
            print(f"Error while running the query: {e}")

    # --- Exit ---
    elif choice == 0:
        break