from django.urls import resolve, reverse
from .models import Round, Shot

def incomplete_rounds(request):
    resolved_view_name = resolve(request.path_info).url_name

    # exclude scorecard view
    if resolved_view_name in ['scorecard', 'hole-details']:
        return {'incomplete_rounds_info': None}

    if request.user.is_authenticated:
        # ✅ Only proceed if incomplete rounds exist
        incomplete_rounds = Round.objects.filter(user=request.user, round_completed=False)

        if incomplete_rounds.exists():
            # Get the last shot from an incomplete round
            last_shot = Shot.objects.filter(
                user=request.user,
                round__in=incomplete_rounds
            ).order_by('-id').first()

            # ✅ CASE 1: last shot finished the hole → go to next-hole
            if last_shot and last_shot.last_shot_of_hole:
                url = reverse('hole-details', kwargs={
                    'course_id': last_shot.course_id,
                    'round_id': last_shot.round_id,
                    
                })
                return {
                    'incomplete_rounds_info': {
                        'redirect_url': url,
                        'type': 'hole-details'
                    }
                }

            # ✅ CASE 2: still inside the latest hole → go to scorecard
            incomplete_round = incomplete_rounds.last()
            latest_hole = incomplete_round.hole_set.last()
            if latest_hole:
                url = reverse('scorecard', kwargs={
                    'hole_id': latest_hole.id,
                })
                return {
                    'incomplete_rounds_info': {
                        'redirect_url': url,
                        'type': 'scorecard'
                    }
                }

    return {'incomplete_rounds_info': None}
