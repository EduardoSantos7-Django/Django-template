import random
import string
from django.db import OperationalError, ProgrammingError

from django.db.models import Model

BASE_64 = '0123456789' + string.ascii_letters + '-_'


def generate_pk_base_64(model: Model, size=11) -> str:
    """Return a unique base 64 id."""
    while True:
        random_pk = ''.join(random.choices(BASE_64, k=size))
        try:
            if not model.objects.filter(pk=random_pk).exists():
                break
        except (OperationalError, ProgrammingError):
            break

    return random_pk
