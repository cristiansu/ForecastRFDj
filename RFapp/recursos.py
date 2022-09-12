from import_export import resources
from .models import ForecastTablaManu

class ManualResource(resources.ModelResource):
    class Meta:
        model = ForecastTablaManu
        exclude = ('id',)