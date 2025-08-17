def cart_item_count(request):
    cart = request.session.get('cart', {})

    # Ensure cart is a dictionary
    if not isinstance(cart, dict):
        cart = {}

    # Sum only integer quantities
    count = 0
    for value in cart.values():
        if isinstance(value, int):
            count += value
        else:
            # If somehow a dict or other type, ignore or reset
            continue

    return {'cart_count': count}
