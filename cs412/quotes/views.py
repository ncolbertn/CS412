from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

quotes = ["It's so old-fashioned to work. I'd much rather lounge about the house all day looking fascinting. I'd rather look fascinating than have a permanent income",
        "What would you like to know about America, bucko? Don't tell me you've never been! Every schmuck has been to America (and incidentally only the uneducated say 'America', the hip lingo specialists say 'the States', baby.)",
        "I'm sorry to hear that your friend is going to Australia. He doesn't sound very intelligent. Nobody with any sense goes there.",
        "Since you so politely ask, in my spare time I waltz around sunny Manchester looking sultry, over-educated, and kinda deco (whatever that means.) I consider it my only real purpose in life to look as bored as humanly possible. I'm so old fashioned.",
        "I consider it my puristic duty as self-elected chairman of our National League of Decency, to cultivate your mind at once. My only fear is that it may already be too late."]
images = ["https://consequence.net/wp-content/uploads/2022/12/Morrissey.jpeg?quality=80", 
          "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwOhnmkojPbhpz25wNtWozPCID0wpY_PDAcA&s",
        "https://www.angryyoungandpoor.com/store/pc/catalog/products/misc/fp01420rav.jpg",
        "https://i.guim.co.uk/img/media/fd8a1d46c44e0758750dcda940f76dbf7698191c/0_0_3895_5970/master/3895.jpg?width=465&dpr=1&s=none"]

def quote(request):
    template_name = 'quote.html'
    context = {
        "quote" : random.choice(quotes),
        "image" : random.choice(images),
    }
    return render(request, template_name, context)

def show_all(request):
    template_name = 'show_all.html'
    context = {
        "quotes" : quotes,
        "images" : images,
    }
    return render(request, template_name, context)


def about(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'about.html'

    # delegate rendering work to the template
    return render(request, template_name)