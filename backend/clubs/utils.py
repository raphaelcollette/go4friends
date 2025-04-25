from direct_messages.models import ThreadParticipant

def add_user_to_club_chat(club, user):
    if club.thread and not ThreadParticipant.objects.filter(thread=club.thread, user=user).exists():
        ThreadParticipant.objects.create(thread=club.thread, user=user)