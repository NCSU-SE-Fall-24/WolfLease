from django.test import TestCase
from housing.models import Owner, Apartment, Lease, Flat, UserPreference, User, Interested

class OwnerModelTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            contact_number="1234567890",
            contact_email="owner@example.com",
            password="ownerpassword"
        )

    def test_owner_creation(self):
        self.assertIsInstance(self.owner, Owner)
        self.assertEqual(self.owner.contact_email, "owner@example.com")


class ApartmentModelTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            contact_number="1234567890",
            contact_email="owner@example.com",
            password="ownerpassword"
        )
        self.apartment = Apartment.objects.create(
            address="123 Main St",
            facilities="Gym, Pool",
            owner_id=self.owner
        )

    def test_apartment_creation(self):
        self.assertIsInstance(self.apartment, Apartment)
        self.assertEqual(self.apartment.address, "123 Main St")


class LeaseModelTest(TestCase):
    def setUp(self):
        self.lease = Lease.objects.create(
            lease_start_date="2024-01-01",
            lease_end_date="2025-01-01"
        )

    def test_lease_creation(self):
        self.assertIsInstance(self.lease, Lease)
        self.assertEqual(self.lease.lease_start_date, "2024-01-01")


class FlatModelTest(TestCase):
    def setUp(self):
        self.apartment = Apartment.objects.create(
            address="123 Main St",
            facilities="Gym, Pool",
            owner_id=None
        )
        self.lease = Lease.objects.create(
            lease_start_date="2024-01-01",
            lease_end_date="2025-01-01"
        )
        self.flat = Flat.objects.create(
            availability=True,
            associated_apt_id=self.apartment,
            lease_id=self.lease,
            rent_per_room=1000,
            floor_number=2
        )

    def test_flat_creation(self):
        self.assertIsInstance(self.flat, Flat)
        self.assertEqual(self.flat.rent_per_room, 1000)


class UserPreferenceModelTest(TestCase):
    def setUp(self):
        self.preference = UserPreference.objects.create(preference_type="veg")

    def test_preference_creation(self):
        self.assertIsInstance(self.preference, UserPreference)
        self.assertEqual(str(self.preference), "veg")


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            contact_number="9876543210",
            contact_email="user@example.com",
            password="userpassword",
            dob="1995-01-01",
            gender="M"
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.contact_email, "user@example.com")


class InterestedModelTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            contact_number="1234567890",
            contact_email="owner@example.com",
            password="ownerpassword"
        )
        self.apartment = Apartment.objects.create(
            address="123 Main St",
            facilities="Gym, Pool",
            owner_id=self.owner
        )
        self.flat = Flat.objects.create(
            associated_apt_id=self.apartment,
            lease_id=None,
            rent_per_room=1000,
            floor_number=1
        )
        self.user = User.objects.create(
            contact_number="9876543210",
            contact_email="user@example.com",
            password="userpassword",
            dob="1995-01-01",
            gender="M"
        )
        self.interested = Interested.objects.create(
            apartment_id=self.apartment,
            flat_id=self.flat,
            user_id=self.user
        )

    def test_interested_creation(self):
        self.assertIsInstance(self.interested, Interested)
        self.assertEqual(self.interested.apartment_id, self.apartment)
