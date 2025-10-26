from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):

    return "₨"+str(number)

@register.filter(name='multiply')
def multiply(item,qty):
    total_price=item*qty
    return total_price

@register.filter(name='rembal')
def rembal(item,qty):
    rem_balance=item-qty
    return  rem_balance

@register.filter(name='plus')
def plus(liabilitie,equity):
    rem_balance=liabilitie+equity
    return  rem_balance

@register.filter
def rembalance(balance, subtract_amount, add_increment):
    """Adjusts an account balance by subtracting a specific amount and adding an increment."""
    return balance - subtract_amount + add_increment


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def get_item(dictionary, key):
 
    return dictionary.get(key)

@register.filter
def get_amount(dictionary, key):

    result = dictionary.get(key)
    # Check if the result is a dictionary and contains 'amount__sum'
    if isinstance(result, dict) and 'amount__sum' in result:
        return result['amount__sum']
    return result

@register.filter(name='capitalize_after_space')
def capitalize_after_space(value):
    if not isinstance(value, str):
        value=str(value)
        return ' '.join([word.capitalize() for word in value.split()])
        # return value  # Return the original value if it's not a string
    return ' '.join([word.capitalize() for word in value.split()])