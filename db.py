import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#This class is soley responsible for reading from and writing to our firebase database.
class Database:

    #the constructor simply authenticates and makes a connection to firebase database and initializes db as a class variables for it to be used in other methods for reading/writing data.
    def __init__(self):
        # Use a service account
        cred = credentials.Certificate('./node_modules/firebase_credentials.json')
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.passwords_collection = self.db.collection('EnhancedPasswords')

    
    #This function lists all the User Enhanced passwords for all the base passwords stored in our database.
    def list_users_enhanced_passwords(self):

        #Get a reference to all the basePassword documents
        docs = self.passwords_collection.stream()

        #Loop through each of these basePasswords documents
        for doc in docs:
            print("\nThese are the user guesses for the base password: " + doc.id)
            #Print all the userEnhancedPasswords inside this basePassword Document
            for password in doc.to_dict()['usersEnhancedPasswords']:
                print(password)

    #This function lists all the User Enhanced passwords the provided base password, if it exists in our database.
    def list_users_enhanced_password_specific(self, basePassword):

        #Get a reference to the basePassword document
        doc_ref = self.passwords_collection.document(basePassword)
        doc = doc_ref.get()

        print("\nThese are the user guesses for the base password: " + doc.id)
        #Print all the userEnhancedPasswords inside this basePassword Document
        for password in doc.to_dict()['usersEnhancedPasswords']:
            print(password)         

    #This function takes in an input dictionary, whose key repesent a base password and the corresponding value represents the User Enhnaced Password. It simply add this User Enhaced Password to the UserEnhancedPasswords list inside the basePassword document on db.
    def add_user_enhanced_passwords(self, base_password_to_enhanced_password_dict):
        for key, value in base_password_to_enhanced_password_dict.items():
            doc_ref = self.passwords_collection.document(key)
            #If the userEnhancedPasswords array exist in our db then simply append the value to it
            if doc_ref.get().exists:
                doc_ref.update({'usersEnhancedPasswords': firestore.ArrayUnion([value])})
            #Otherwise first crate an empty userEnhancedPasswords array and then append the value to it    
            else:
                doc_ref.set({'usersEnhancedPasswords': firestore.ArrayUnion([value])})