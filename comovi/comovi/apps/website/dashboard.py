import random
from enum import Enum

from django.db.models import Q
from django.utils.timezone import now

from comovi.apps.core.models import Property, PropertyInterior, CatalogService, PropertyInteriorHasService
from comovi.apps.website.translations import translations


class StatColor(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    PURPLE = 'purple'
    LIGHT_RED = 'light-red'
    LIGHT_BLUE = 'light-blue'
    DARK_BLUE = 'dark-blue'


class DashboardStat:

    def __init__(self):
        self.color = self.make_random_color()

    color: StatColor = StatColor.GREEN
    title: str
    total: float = 0
    total_title: str
    first_value: float = 0
    first_value_title: str
    second_value: float = 0
    second_value_title: str
    percentage_value: float = 0
    percentage_label: str

    # noinspection PyTypeChecker
    @staticmethod
    def make_random_color() -> StatColor:
        return random.choice(list(StatColor))


class Dashboard:

    @staticmethod
    def make_property_interiors_stat(obj: Property) -> DashboardStat:
        property_interiors = obj.interiors.all()
        property_interiors_occupied = property_interiors.filter(status_occupancy=PropertyInterior.OCCUPIED)
        property_interiors_empty = property_interiors.filter(status_occupancy=PropertyInterior.EMPTY)

        total = property_interiors.count()

        stat = DashboardStat()
        stat.color = StatColor.GREEN
        stat.title = translations['property_interiors_stat_title']
        stat.total_title = translations['property_interiors_stat_total']
        stat.first_value_title = translations['property_interiors_stat_first_value']
        stat.second_value_title = translations['property_interiors_stat_second_value']

        percentage = 0 if total == 0 else 100 / total * property_interiors_occupied.count()
        stat.percentage_label = translations['property_interiors_stat_percentage'] % str(percentage)

        stat.total = total
        stat.first_value = property_interiors_occupied.count()
        stat.second_value = property_interiors_empty.count()
        stat.percentage_value = percentage
        return stat

    @staticmethod
    def make_services_to_show(services: [CatalogService]) -> [DashboardStat]:
        stats: [DashboardStat] = []
        this_month = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for service in services:
            interiors_with_service = PropertyInteriorHasService.objects.filter(service=service,
                                                                               due_date__gte=this_month)
            services_pending = interiors_with_service.filter(
                Q(status_payment=PropertyInteriorHasService.PENDING) | Q(
                    status_payment=PropertyInteriorHasService.PENDING_REVIEW)
            )
            services_paid = interiors_with_service.filter(status_payment=PropertyInteriorHasService.PAID)

            stat = DashboardStat()
            stat.title = service.name
            stat.total_title = translations['service_stat_total']
            stat.first_value_title = translations['service_stat_first_value']
            stat.second_value_title = translations['service_stat_second_value']

            total = interiors_with_service.count()
            percentage = 0 if total == 0 else 100 / total * services_paid.count()
            stat.percentage_label = translations['service_stat_percentage'] % str(percentage)

            stat.total = total
            stat.first_value = services_pending.count()
            stat.second_value = services_paid.count()
            stat.percentage_value = percentage
            stats.append(stat)
        return stats
