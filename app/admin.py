from django.contrib import admin
from .models import ModeloDeCorrida, HistoricoCorrida

# modelos para que sejam visíveis e editáveis no /admin/
admin.site.register(ModeloDeCorrida)
admin.site.register(HistoricoCorrida)
