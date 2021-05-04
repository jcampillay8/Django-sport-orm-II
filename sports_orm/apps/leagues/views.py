from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker
from django.db.models import Q, Count


def index(request):

	context = {
		#1 todos los equipos en la Atlantic Soccer Conference
		"ateams": Team.objects.filter(league__name = 'Atlantic Soccer Conference'),
		
        #2 todos los jugadores (actuales) en los Boston Penguins
		"Bplayers": Player.objects.filter(curr_team__team_name = 'Penguins'),

		#3 todos los jugadores (actuales) en la International Collegiate Baseball Conference
		"Iplayers": Player.objects.filter(curr_team__league_id=2),

		#4 todos los jugadores (actuales) en la Conferencia Americana de Fútbol Amateur con el apellido "López"
		"Lplayers": Player.objects.filter(curr_team__league_id=7) & Player.objects.filter(last_name="Lopez"),
		
		#5 todos los jugadores de fútbol
		"fplayers": Player.objects.filter(curr_team__league_id=7) | Player.objects.filter(curr_team__league_id=9),
		
        #6 todos los equipos con un jugador (actual) llamado "Sophia"
		'steams': Team.objects.filter(curr_players__first_name="Sophia"),

		#7 todas las ligas con un jugador (actual) llamado "Sophia"
		'sleague': League.objects.filter(teams__id=25) | League.objects.filter(teams__id=4) | League.objects.filter(teams__id=32),  

		#8 todos con el apellido "Flores" que NO (actualmente) juegan para los Washington Roughriders
		"notfplayers": Player.objects.filter(last_name = 'Flores') & Player.objects.filter(~Q(curr_team_id=10)) ,

		#9 todos los equipos, pasados y presentes, con los que Samuel Evans ha jugado
		'seteams': Team.objects.filter(all_players__id=115),

		#10 todos los jugadores, pasados y presentes, con los gatos tigre de Manitoba
		"maniplayers": Player.objects.filter(all_teams__id=4),

		#11 todos los jugadores que anteriormente estaban (pero que no lo están) con los Wichita Vikings
		"vikiplayers": Player.objects.filter(all_teams__id=40),

		# cada equipo para el que Jacob Gray jugó antes de unirse a los Oregon Colts
		'jacteams': Team.objects.filter(all_players__id=151)[:3],

		#13 todos llamados "Joshua" que alguna vez han jugado en la Federación Atlántica de Jugadores de Béisbol Amateur
		"atplayers": Player.objects.filter(first_name="Joshua") & Player.objects.filter(all_teams__league_id=3),

		# todos los equipos que han tenido 12 o más jugadores, pasados y presentes.
		"playerNums": Team.objects.annotate(nplayer=Count('all_players')).filter(nplayer__gt=12),

		# todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
		"allplayerteam": Team.objects.annotate(nplayer=Count('all_players')).order_by('nplayer')
	
	}
	
	return render(request, "index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
