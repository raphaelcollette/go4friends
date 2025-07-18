from direct_messages.models import ThreadParticipant

def add_user_to_club_chat(club, user):
    """
    Adds a user to the club's associated thread (chat) if:
    - The club has a thread.
    - The user is not already a participant in the thread.
    """
    if club.thread and not ThreadParticipant.objects.filter(thread=club.thread, user=user).exists():
        ThreadParticipant.objects.create(thread=club.thread, user=user)