"""Test suite for the electronics app."""
from datetime import date
from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .admin import NetworkNodeAdmin, clear_debt
from .filters import NetworkNodeFilter
from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer

User = get_user_model()


class NetworkNodeModelTests(TestCase):
    """Tests for model rules and helpers."""

    def setUp(self) -> None:
        """Create a base supplier chain."""
        self.factory = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.FACTORY,
            name='Factory',
            email='factory@example.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1',
            debt=Decimal('0.00'),
        )
        self.retail = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.RETAIL,
            name='Retail',
            email='retail@example.com',
            country='Russia',
            city='Kazan',
            street='Pushkina',
            house_number='2',
            supplier=self.factory,
            debt=Decimal('150.50'),
        )
        self.entrepreneur = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.ENTREPRENEUR,
            name='Entrepreneur',
            email='ip@example.com',
            country='Russia',
            city='Sochi',
            street='Sadovaya',
            house_number='3',
            supplier=self.retail,
            debt=Decimal('90.10'),
        )

    def test_string_representations_and_hierarchy(self) -> None:
        """String conversion and computed hierarchy level should work."""
        product = Product.objects.create(
            node=self.factory,
            name='Phone',
            model='P-1',
            release_date=date(2025, 1, 1),
        )
        self.assertEqual(str(self.factory), 'Factory')
        self.assertEqual(str(product), 'Phone (P-1)')
        self.assertEqual(self.factory.hierarchy_level, 0)
        self.assertEqual(self.retail.hierarchy_level, 1)
        self.assertEqual(self.entrepreneur.hierarchy_level, 2)

    def test_factory_cannot_have_supplier(self) -> None:
        """Factories must stay at level zero."""
        obj = NetworkNode(
            entity_type=NetworkNode.EntityType.FACTORY,
            name='Bad Factory',
            email='bad@example.com',
            country='Russia',
            city='Perm',
            street='Mira',
            house_number='10',
            supplier=self.factory,
            debt=Decimal('0.00'),
        )
        with self.assertRaises(ValidationError):
            obj.full_clean()

    def test_self_reference_is_forbidden(self) -> None:
        """A node cannot point to itself as supplier."""
        self.retail.supplier = self.retail
        with self.assertRaises(ValidationError):
            self.retail.full_clean()

    def test_cycle_is_forbidden(self) -> None:
        """Supplier cycles should be rejected."""
        self.factory.entity_type = NetworkNode.EntityType.RETAIL
        self.factory.supplier = self.entrepreneur
        with self.assertRaises(ValidationError):
            self.factory.full_clean()

    def test_more_than_three_levels_is_forbidden(self) -> None:
        """Only three hierarchy levels are allowed: 0, 1 and 2."""
        obj = NetworkNode(
            entity_type=NetworkNode.EntityType.ENTREPRENEUR,
            name='Too Deep',
            email='deep@example.com',
            country='Russia',
            city='Tomsk',
            street='Main',
            house_number='5',
            supplier=self.entrepreneur,
            debt=Decimal('1.00'),
        )
        with self.assertRaises(ValidationError):
            obj.full_clean()


class AdminTests(TestCase):
    """Tests for admin helpers and actions."""

    def setUp(self) -> None:
        """Create objects needed by admin tests."""
        self.site = AdminSite()
        self.factory = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.FACTORY,
            name='Factory Admin',
            email='fa@example.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1',
            debt=Decimal('0.00'),
        )
        self.retail = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.RETAIL,
            name='Retail Admin',
            email='ra@example.com',
            country='Russia',
            city='Moscow',
            street='Tverskaya',
            house_number='2',
            supplier=self.factory,
            debt=Decimal('10.00'),
        )
        self.admin_obj = NetworkNodeAdmin(NetworkNode, self.site)

    def test_supplier_link_and_level_display(self) -> None:
        """Admin helpers should display supplier link and hierarchy level."""
        html = self.admin_obj.supplier_link(self.retail)
        self.assertIn('Factory Admin', html)
        self.assertIn(str(self.factory.pk), html)
        self.assertEqual(self.admin_obj.supplier_link(self.factory), '-')
        self.assertEqual(self.admin_obj.hierarchy_level_display(self.retail), 1)

    def test_clear_debt_action(self) -> None:
        """Admin action should reset debt to zero."""
        request = RequestFactory().post('/')
        clear_debt(self.admin_obj, request, NetworkNode.objects.filter(pk=self.retail.pk))
        self.retail.refresh_from_db()
        self.assertEqual(self.retail.debt, Decimal('0.00'))


class SerializerAndFilterTests(TestCase):
    """Tests for serializer behavior and filtering."""

    def setUp(self) -> None:
        """Create a factory and product for serializer tests."""
        self.factory = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.FACTORY,
            name='Factory Serializer',
            email='fs@example.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1',
            debt=Decimal('0.00'),
        )
        Product.objects.create(
            node=self.factory,
            name='Laptop',
            model='L-1',
            release_date=date(2025, 2, 1),
        )

    def test_serializer_contains_nested_products(self) -> None:
        """Serializer should expose read-only nested products and hierarchy level."""
        serializer = NetworkNodeSerializer(instance=self.factory)
        self.assertEqual(serializer.data['hierarchy_level'], 0)
        self.assertEqual(serializer.data['products'][0]['model'], 'L-1')

    def test_debt_is_read_only_on_update(self) -> None:
        """Debt should not be editable through serializer updates."""
        request = RequestFactory().patch('/')
        request.user = type(
            'UserObj',
            (),
            {'is_authenticated': True, 'is_active': True, 'is_staff': True},
        )()
        serializer = NetworkNodeSerializer(
            instance=self.factory,
            data={'name': 'Factory Serializer', 'debt': '500.00'},
            partial=True,
            context={'request': request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.debt, Decimal('0.00'))

    def test_country_filter(self) -> None:
        """Filter should return objects from the selected country only."""
        other = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.RETAIL,
            name='Retail EU',
            email='eu@example.com',
            country='Germany',
            city='Berlin',
            street='Unter den Linden',
            house_number='7',
            supplier=self.factory,
            debt=Decimal('1.00'),
        )
        queryset = NetworkNodeFilter(
            {'country': 'germany'},
            queryset=NetworkNode.objects.all(),
        ).qs
        self.assertEqual(list(queryset), [other])


class PermissionTests(TestCase):
    """Tests for custom permissions."""

    def test_active_staff_permission(self) -> None:
        """Permission should allow only active staff users."""
        permission = IsActiveStaff()
        request = RequestFactory().get('/')

        request.user = User(username='ok', is_active=True, is_staff=True)
        self.assertTrue(permission.has_permission(request, None))

        request.user = User(username='inactive', is_active=False, is_staff=True)
        self.assertFalse(permission.has_permission(request, None))

        request.user = User(username='nonstaff', is_active=True, is_staff=False)
        self.assertFalse(permission.has_permission(request, None))


class APITests(APITestCase):
    """Tests for API endpoints and permissions."""

    def setUp(self) -> None:
        """Create users and seed data for API tests."""
        self.staff_user = User.objects.create_user(
            username='staff',
            password='pass12345',
            is_active=True,
            is_staff=True,
        )
        self.inactive_user = User.objects.create_user(
            username='inactive',
            password='pass12345',
            is_active=False,
            is_staff=True,
        )
        self.factory = NetworkNode.objects.create(
            entity_type=NetworkNode.EntityType.FACTORY,
            name='API Factory',
            email='api-factory@example.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1',
            debt=Decimal('0.00'),
        )
        self.client = APIClient()
        self.list_url = reverse('nodes-list')

    def test_api_requires_active_staff(self) -> None:
        """Anonymous and inactive staff users must be rejected."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.inactive_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

    def test_api_crud_and_country_filter(self) -> None:
        """Active staff users should be able to use the CRUD API."""
        self.client.force_authenticate(self.staff_user)

        create_response = self.client.post(
            self.list_url,
            {
                'entity_type': NetworkNode.EntityType.RETAIL,
                'name': 'API Retail',
                'email': 'api-retail@example.com',
                'country': 'Germany',
                'city': 'Berlin',
                'street': 'Street',
                'house_number': '10',
                'supplier': self.factory.pk,
                'debt': '200.25',
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, 201)
        created_id = create_response.data['id']

        filtered = self.client.get(self.list_url, {'country': 'germany'})
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(len(filtered.data), 1)
        self.assertEqual(filtered.data[0]['name'], 'API Retail')

        detail_url = reverse('nodes-detail', args=[created_id])
        patch_response = self.client.patch(
            detail_url,
            {'debt': '999.99', 'city': 'Munich'},
            format='json',
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data['city'], 'Munich')
        self.assertEqual(patch_response.data['debt'], '200.25')

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(NetworkNode.objects.filter(pk=created_id).exists())