from django.urls import resolve
from .models import Round, Hole

def incomplete_rounds(request):
    resolved_view_name = resolve(request.path_info).url_name
    
    # exlude the scorecard view for the context processor
    if resolved_view_name == 'scorecard':
        return {'incomplete_rounds_info': None}
    
    # Add incomplete_rounds for all other views
    if request.user.is_authenticated:

        # Check if the user has started at least one hole in an incomplete round
        incomplete_rounds = Round.objects.filter(user=request.user, round_completed=False)
        if incomplete_rounds.exists():

            for incomplete_round in incomplete_rounds:
                # Get the latest hole of the incomplete round
                latest_hole = incomplete_round.hole_set.last()
                if latest_hole:
                    # Get the hole_id of the latest hole
                    hole_id = latest_hole.id
                    return {'incomplete_rounds_info': {'hole_id': hole_id}}
    
   
    return {'incomplete_rounds_info': None}
