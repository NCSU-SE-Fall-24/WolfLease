def test_create_owner_with_invalid_data(self):
        """
        Ensure that creating an Owner with invalid data returns a bad request.
        """
        url = '/owners'
        data = {
            'contact_number': 'invalid-phone',  # Invalid phone format
            'contact_email': 'not-an-email',    # Invalid email format
            'password': ''                      # Empty password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_update_nonexistent_owner(self):
        """
        Attempt to update an Owner that does not exist.
        """
        url = '/owners/99999'  # Assuming this ID does not exist
        data = {'contact_email': 'nonexistent@testing.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
def test_create_interested_with_invalid_flat(self):
        """
        Ensure that we cannot create an interested entry with an invalid flat ID.
        """
        url = '/interests'
        data = {
            'user_id': str(User.objects.get().id),
            'flat_id': '99999',  # Invalid flat ID
            'apartment_id': str(Apartment.objects.get().id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_get_nonexistent_interest(self):
        """
        Attempt to fetch an Interested object that does not exist.
        """
        url = '/interests/99999'  # Assuming this ID does not exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
def test_create_flat_with_high_rent(self):
        """
        Ensure we can create a Flat with high rent to check boundary limits.
        """
        url = '/flats'
        data = {
            'availability': 'True',
            'associated_apt_id': str(Apartment.objects.get().id),
            'lease_id': str(Lease.objects.get().id),
            'floor_number': '1',
            'rent_per_room': '10000'  # High rent value for boundary testing
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flat.objects.count(), 2)

def test_update_flat_with_invalid_availability(self):
        """
        Attempt to update a flat's availability with an invalid value.
        """
        url = '/flats/' + str(Flat.objects.get().id)
        data = {'availability': 'NotValid'}  # Invalid availability value
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
def test_create_apartment_missing_fields(self):
        """
        Ensure that creating an Apartment with missing fields returns an error.
        """
        url = '/apartments'
        data = {
            'address': '',  # Missing address field
            'owner_id': str(Owner.objects.get().id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_search_apartment_no_results(self):
        """
        Ensure that searching for an Apartment with no results returns an empty response.
        """
        url = '/apartments?search=nonexistentaddress'
        response = self.client.get(url)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 0)

def test_create_owner_duplicate_email(self):
        """
        Ensure that creating an Owner with a duplicate email is handled properly.
        """
        Owner.objects.create(contact_number='1112223333', contact_email='test@testing.com', password='test')
        url = '/owners'
        data = {
            'contact_number': '9998887777',
            'contact_email': 'test@testing.com',  # Duplicate email
            'password': 'newtest'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_show_owner_without_authentication(self):
        """
        Ensure that fetching an Owner object without authentication fails.
        """
        self.client.credentials()  # Remove the token
        url = '/owners'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_create_interested_duplicate_entry(self):
        """
        Ensure that duplicate interested entries for the same user and flat are handled.
        """
        url = '/interests'
        data = {
            'user_id': str(User.objects.get().id),
            'flat_id': str(Flat.objects.get().id),
            'apartment_id': str(Apartment.objects.get().id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Attempt to create a duplicate
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_update_interested_with_invalid_user(self):
        """
        Ensure we cannot update an interested object with an invalid user ID.
        """
        url = '/interests/' + str(Interested.objects.get().id)
        data = {'user_id': '99999'}  # Invalid user ID
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_flat_missing_fields(self):
        """
        Ensure creating a Flat with missing required fields returns an error.
        """
        url = '/flats'
        data = {
            'availability': 'True',
            'associated_apt_id': str(Apartment.objects.get().id)
            # Missing 'lease_id', 'floor_number', 'rent_per_room'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_delete_flat_with_existing_user(self):
        """
        Ensure that deleting a Flat associated with a user fails or handles it gracefully.
        """
        flat = Flat.objects.get()
        url = f'/flats/{flat.id}'
        response = self.client.delete(url)
        # This assumes that you cannot delete a flat with associated users
        # Adjust according to your app's logic.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
def test_create_apartment_with_long_address(self):
        """
        Ensure that creating an Apartment with an excessively long address fails.
        """
        url = '/apartments'
        data = {
            'address': 'a' * 256,  # Assuming max length is 255
            'facilities': 'Gym, Pool',
            'owner_id': str(Owner.objects.get().id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_update_apartment_invalid_owner(self):
        """
        Attempt to update an Apartment with an invalid owner ID.
        """
        url = '/apartments/' + str(Apartment.objects.get().id)
        data = {'owner_id': '99999'}  # Nonexistent owner
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def test_create_owner_with_short_password(self):
    """
    Ensure that creating an Owner with a password that is too short returns an error.
    """
    url = '/owners'
    data = {
        'contact_number': '1234567890',
        'contact_email': 'valid@example.com',
        'password': 'short' 
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('password', response.data) 

def test_update_owner_with_invalid_email_format(self):
    """
    Attempt to update an Owner's email with an invalid format.
    """
    url = '/owners/' + str(Owner.objects.get().id)
    data = {'contact_email': 'invalid-email-format'}
    response = self.client.patch(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('contact_email', response.data)

def test_delete_nonexistent_flat(self):
    """
    Attempt to delete a Flat that does not exist.
    """
    url = '/flats/99999' 
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_create_apartment_with_invalid_facilities_format(self):
    """
    Ensure that creating an Apartment with an invalid facilities format returns an error.
    """
    url = '/apartments'
    data = {
        'address': '123 Valid St',
        'facilities': 'Not a list',
        'owner_id': str(Owner.objects.get().id)
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('facilities', response.data)