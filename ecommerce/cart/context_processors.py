from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}
    # context_processors settings are added in settings.py