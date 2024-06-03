import factory
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from ware_home.supplies.models import Category, Product, Supply


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("company")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("company")
    bar_code = Faker("ean")
    description = Faker("words")
    volume = Faker("color")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            self.categories.add(CategoryFactory())
            return

        self.categories.add(*extracted)


class SupplyFactory(DjangoModelFactory):
    class Meta:
        model = Supply

    product = SubFactory(ProductFactory)
    amount = Faker("pyint", min_value=1, max_value=5)
    expiration_date = Faker("date_this_month")
