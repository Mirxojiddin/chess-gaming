import django_filters
from gaming.models import Player, Game


class PlayerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_elo_rating = django_filters.NumberFilter(field_name='elo_rating', lookup_expr='gte')
    max_elo_rating = django_filters.NumberFilter(field_name='elo_rating', lookup_expr='lte')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')

    class Meta:
        model = Player
        fields = ['name', 'min_elo_rating', 'max_elo_rating', 'country']


class GameFilter(django_filters.FilterSet):
    white_player_name = django_filters.CharFilter(field_name='white__name', lookup_expr='icontains')
    black_player_name = django_filters.CharFilter(field_name='black__name', lookup_expr='icontains')
    result = django_filters.CharFilter(lookup_expr='iexact')
    opening = django_filters.CharFilter(field_name='opening__name', lookup_expr='icontains')
    min_date_played = django_filters.DateFilter(field_name='date_played', lookup_expr='gte')
    max_date_played = django_filters.DateFilter(field_name='date_played', lookup_expr='lte')

    class Meta:
        model = Game
        fields = ['white_player_name', 'black_player_name', 'result', 'opening', 'min_date_played', 'max_date_played']
