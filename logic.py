from datetime import datetime

def is_adult(age):
    """Zwraca True, jeśli uczestnik jest pełnoletni, w przeciwnym razie False."""
    return age >= 18

def requires_parental_consent(age):
    """Zwraca True, jeśli uczestnik jest niepełnoletni i wymaga zgody rodziców, w przeciwnym razie False."""
    return not is_adult(age)

def can_exit(entry_time, exit_permission, age):
    """Sprawdza, czy uczestnik może opuścić wydarzenie."""
    if age < 18 and not exit_permission:
        return False  # Niepełnoletni bez zgody nie mogą wyjść
    if entry_time is None:
        return False  # Uczestnik musi najpierw wejść
    return True

