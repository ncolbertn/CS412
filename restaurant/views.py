from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, time, timedelta


#Key-Value pairs express the item name as a str and
#Item price as an int.
items = {
    'Spaghetti Marinara' : 10,
    'Spaghetti Carbonara' : 12,
    'Fettucini Alfredo' : 12,
    'Margharita Pizza' : 13
         
}
specialItems = {
    'Luigi\'s Special Linguini' : 11,
    'Lobster Alfredo': 11,
    'Gnocchi Marinara' : 11,
    'Chicken Parmigiana' : 11,
}

def main(request):
    
    template_name = 'restaurant/main.html'
    
    context = {
        "isClosed": isClosed(),
    }
    return render(request, template_name, context)

def order(request):

    template_name = 'restaurant/order.html'
    specialotd = random.choice(list(specialItems.items()))
    print(specialotd)
    context = {
        'menuItems' : items,
        'specialotditem' : specialotd[0],
        'specialotdprice' : specialotd[1]
    }
    return render(request, template_name, context)


def confirmation(request):
    ''''''
    print("in confirmation")
    if request.POST:
        template_name = 'restaurant/confirmation.html'
        orderedItems = request.POST.getlist('orderItems')
        print(orderedItems)
        orderItemsDict = {choice: items[choice] for choice in orderedItems}
        print(orderItemsDict)
        total = 0
        for item in orderItemsDict:
            total += orderItemsDict[item]
            print("the total before special is: " + str(total))
        if 'special' in  request.POST:
            total += specialItems[request.POST['special']]
            print("total after special " + str(total))
            # this stupid line is i guess a Pythonic method of appending
            # to the ordered items dict another entry with the key of the
            # special and a lookup to the original dict for the price.
            # practically unreadable? yeah. Functioning? I hope.
            orderItemsDict[request.POST['special']] = specialItems[request.POST['special']]
            print(orderItemsDict) 
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']
        readyTime = datetime.now() + timedelta(minutes=random.randrange(30,60))
        context = {
            'orderedItems' : orderItemsDict,
            'total' : total,
            'name' : name,
            'phone' : phone,
            'email' : email,
            'readyTime' : readyTime,
            'special_instructions' : special_instructions,
        }
        print(context)
        return render(request, template_name, context)
    else:
        return redirect("order")
    
def isClosed():
    currTime = datetime.now().time()
    weekday = datetime.now().weekday()
    if weekday in range(0,4):
        if  time(10,0,0) <= currTime <= time(21,0,0):
            return False
        return True
    elif weekday == 4 or weekday == 5:
        if time(10,0,0) <= currTime <= time(23,0,0):
            return False
        return True
    else:
        return True
    
