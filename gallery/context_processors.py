from .models import Style


def styles(request):
    """
    Retrieves all styles from the database and returns them in a dictionary.
    """
    styles = Style.objects.all()
    return {'styles': styles}
