import json
from unittest import TestCase
from django.test import Client
from django.urls.base import reverse
import pytest
from applications.companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPiTestCase(TestCase):
    def setUp(self) -> None:
        # Creamos un metodo que llevara una variable cliente que sera igual a una clase Cliente con fines de prueba
        # Client() permite obtener solicitudes GET y POST
        # ------------------------------------------
        self.client = Client()
        # creamos una variable llamada companies_url.
        # obtenemos la url del base_name de urls.py(companies) y indicamos que queremos una lista
        # ------------------------------------------
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyAPiTestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:

        # Creamos una variable response, que sera igual al cliente de prueba y obtendremos la solicitud GET
        # de nuestra urls(base_name='companies')
        response = self.client.get(self.companies_url)
        # ------------------------------------------

        # Se hace una funcion para afirmar que el primer argumento es igual al segundo
        # Entonces, le indicamos que devuelva una status 200(Ok)
        self.assertEqual(response.status_code, 200)
        # ------------------------------------------

        # Se hace una funcion para afirmar que el primer argumento es igual al segundo
        #
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        test_company.delete()


class TestPostCompanies(BasicCompanyAPiTestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        assert response.status_code == 400
        assert json.loads(response.content), {"name": ["This field is required."]}

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="pablo")
        response = self.client.post(path=self.companies_url, data={"name": "pablo"})
        assert response.status_code == 400
        assert json.loads(response.content), {
            "name": ["company with this name already exists."]
        }

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company name"}
        )

        assert response.status_code == 201

        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "test company name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "test company name", "status": "Layoffs"},
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "test company name", "status": "WrongStatus"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)
