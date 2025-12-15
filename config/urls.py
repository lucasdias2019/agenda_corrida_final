from django.contrib import admin
from django.urls import path
from app.views import ( # Importa TODAS as views do seu app (CRUD + Listagem)
    listagem_completa, 
    popular_banco_dados, 
    criar_modelo_corrida,
    editar_modelo_corrida,
    excluir_modelo_corrida,
    registrar_historico,
    editar_historico,
    excluir_historico,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota de INFRAESTRUTURA:
    # Mantemos a função 'popular-bd' para uso em teste, mas ela não será acessível pela interface.
    path('popular-bd/', popular_banco_dados, name='popular_banco_dados'), 

    # ROTAS DE MODELO DE CORRIDA (RF01, RF02, RF03)
    path('modelos/novo/', criar_modelo_corrida, name='criar_modelo_corrida'),
    path('modelos/editar/<int:pk>/', editar_modelo_corrida, name='editar_modelo_corrida'),
    path('modelos/excluir/<int:pk>/', excluir_modelo_corrida, name='excluir_modelo_corrida'),

    # ROTAS DE HISTÓRICO DE CORRIDA (RF04, RF02, RF03)
    path('historico/registrar/', registrar_historico, name='registrar_historico'),
    path('historico/editar/<int:pk>/', editar_historico, name='editar_historico'),
    path('historico/excluir/<int:pk>/', excluir_historico, name='excluir_historico'),
    
    # Rota principal (Listagem - READ)
    path('', listagem_completa, name='listagem_completa'), 
]