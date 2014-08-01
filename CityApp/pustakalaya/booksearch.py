__author__ = 'Pravesh'

from django.http import *
from django.shortcuts import *
from pustakalaya.models import *
import math

def search(request):
    if request.method == 'GET':
        user = request.GET.get('user')
        query = request.GET.get('search_query')
        books = []
        books += Book.objects.filter(author__regex =r'(.*%s.*)'%query).order_by('-published_date')
        books += Book.objects.filter(name__regex = r'(.*%s.*)'%query).order_by('-published_date')
        booklist = list(set(books))
        if len(request.GET) == 2:
            for i in request.GET:
                if i != 'search_query':
                    field = Interest.objects.filter(topic = str(i))
                    if field:
                        field = field[0]
                    break

            if not field:
                booklist = []
            else:
                booklist = [i for i in booklist if field in i.interest.all()]

        length = int(math.ceil(len(booklist)/4.))
        booklist2 = []
        for i in range(length):
            if 4*(i+1)<len(booklist):
                booklist2.append(booklist[4*i:4*(i+1)])
            else:
                booklist2.append(booklist[4*i:])

        booklist = booklist2
        action = 'search_query=%s'%request.GET['search_query']
        path = '/booksearch/'
        showpagination = True
        return render(request, "dashboard.html", {'user':user, 'booklist':booklist, 'show_pagination':showpagination,'action':action, 'path':path})

#    elif request.method == 'GET':
#        # if request.session.get('user','') == '':
#        #     return HttpResponse('You must log in first !!')
#        return render(request, 'booksearch.html')


def get_interest_vector(obj, interest_map):
    interest_vector = []
    for interests in interest_map:
        if interests in obj.interest.all():
            interest_vector.append(1)
        else:
            interest_vector.append(0)
    return interest_vector


def interest_dot(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        sum += vec1[i]*vec2[i]
    return sum

def recommended(request):
    all_interests = tuple(Interest.objects.all())
    interest_count = len(all_interests)
    user = request.session['user']
    user_interest_vector = get_interest_vector(user, all_interests)
    all_books = Book.objects.all()

    interest_data = []
    #   create an interest vector
    for books in all_books:
        interest_vector = get_interest_vector(books, all_interests)
        interest_data.append((interest_dot(interest_vector, user_interest_vector), books))

    interest_data = sorted(interest_data, reverse=True)

    #return the list of names.
    book_list = [i[1] for i in interest_data if user not in i[1].waiting_list.all() and user != i[1].lend and user != i[1].borrow]
    return book_list[:20]

