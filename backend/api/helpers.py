from django.db.models import Q


def build_or_query(array, field):
    """
    Função para gerar uma query com uma condição OR no campo field com os
    valores passado no array
    """
    query = Q()
    for item in array:
        query |= Q(**{field: item})

    return query
