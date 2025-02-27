from django.db import IntegrityError
import random
import string
from ..models import UsersTracks


class HelpersService:
    def __init__(self):
        self.UsersTracks = UsersTracks.objects

    def generate_track_id(self):
        characters = string.ascii_lowercase + string.digits
        while True:
            track_id = ''.join(random.choice(characters) for _ in range(6))
            try:
                if not self.UsersTracks.filter(track_id=track_id).exists():
                    return track_id
            except IntegrityError:
                continue
