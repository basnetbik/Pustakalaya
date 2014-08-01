# Create your views here.
from django.http import *
from django.shortcuts import render, render_to_response
from validation import *
import math
from booksearch import *

def home(request):
    user = request.session.get('user', '')
    showpagination = False
    action = ''
    if user:
        booklist = []
        if request.method=='GET':
            if 'allbooks' in request.GET:
                booklist = list(Book.objects.all().order_by('-published_date'))
                length = int(math.ceil(len(booklist)/4.))
                booklist2 = []
                for i in range(length):
                    if 4*(i+1)<len(booklist):
                        booklist2.append(booklist[4*i:4*(i+1)])
                    else:
                        booklist2.append(booklist[4*i:])
                booklist = booklist2
                showpagination = True
                action = 'allbooks'

            elif 'contributed' in request.GET:
                booklist = list(Book.objects.filter(lend=request.session['user']).order_by('-published_date'))
                length = int(math.ceil(len(booklist)/4.))
                booklist2 = []
                for i in range(length):
                    if 4*(i+1)<len(booklist):
                        booklist2.append(booklist[4*i:4*(i+1)])
                    else:
                        booklist2.append(booklist[4*i:])
                booklist = booklist2
                action = 'contributed'

            elif 'wishlist' in request.GET:
                booklist = list(Book.objects.filter(waiting_list=request.session['user']).order_by('-published_date'))
                length = int(math.ceil(len(booklist)/4.))
                booklist2 = []
                for i in range(length):
                    if 4*(i+1)<len(booklist):
                        booklist2.append(booklist[4*i:4*(i+1)])
                    else:
                        booklist2.append(booklist[4*i:])
                booklist = booklist2
                action = 'wishlist'

            elif 'borrowed' in request.GET:
                booklist = list(Book.objects.filter(borrow=request.session['user']).order_by('-published_date'))
                length = int(math.ceil(len(booklist)/4.))
                booklist2 = []
                for i in range(length):
                    if 4*(i+1)<len(booklist):
                        booklist2.append(booklist[4*i:4*(i+1)])
                    else:
                        booklist2.append(booklist[4*i:])
                booklist = booklist2
                action = 'borrowed'
            elif 'recommended' in request.GET:

                booklist = recommended(request)

                if len(request.GET) == 2:
                    for i in request.GET:
                        if i != 'recommended':
                            field = Interest.objects.filter(topic = str(i))[0]
                            break

                    booklist = [i for i in booklist if field in i.interest.all()]

                length = int(math.ceil(len(booklist)/4.))
                booklist2 = []
                for i in range(length):
                    if 4*(i+1)<len(booklist):
                        booklist2.append(booklist[4*i:4*(i+1)])
                    else:
                        booklist2.append(booklist[4*i:])

                booklist = booklist2
                action = 'recommended'
                showpagination = True



        return render(request, "dashboard.html", {'user':user, 'booklist':booklist, 'show_pagination':showpagination,'action':action})
    else:
        return render(request, "index.html",{'error':''})


def add_to_wishlist(request):
    if request.method=='POST':
        if not 'user' in request.session or 'book' not in request.POST:
            return HttpResponseRedirect('/')
        user = request.session['user']
        book = Book.objects.filter(id=int(request.POST['book']))[0]
        book.waiting_list.add(user)
        book.save()
        return HttpResponseRedirect('/?wishlist')


def signup(request):
    if request.method == 'POST':

        error = ''

        # get all the fields
        fname = request.POST.get('fname', '')   # first name
        lname = request.POST.get('lname', '')   # last name
        uname = request.POST.get('uname', '')   # user name
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        lat = request.POST.get('lat', '')   # latitude
        lon = request.POST.get('lon', '')   # longitude
        interests = request.POST.get('interests', '')   # the interests vector of a person, separated by ;

        # Basic validation
        if not fname or not lname or not uname or not password or not address or not email or \
                        not phone or not interests or not cpassword:
            # generate error
            error = "Fields marked by asterik are compulsory"

        interest_list = interests.split(';')
        interest_obj_list = []

        # Check if the username/email exists on the system
        if UserExists(uname):
            error = "Username already exists"

        elif EmailExists(email):
            error = "Email already exists"

        elif password != cpassword:
            error = "Passwords do not match"

        else:
            try:
                for interest in interest_list:
                    interest_obj_list.append(Interest.objects.get(topic=interest))
            except:
                error = "Invalid Interest request"

        if error:
            # generate some error message here
            return HttpResponse(error)
        else:
            # Create the User
            a = User(username=uname, first_name = fname, last_name=lname, password=password, address=address, \
                 email = email, phone_number=phone,lat=lat, lon=lon)#, interest=[Interest(topic = i) for i in interests.split(';')])

            a.save()
            [a.interest.add(i) for i in interest_obj_list]

            # Show the Dashbord

            return HttpResponse("User Created")

    elif request.method=='GET':
        return render(request,"test.html")


def login(request):
    if request.method=='POST':
        error = ''
        username = request.POST.get('uname')
        password = request.POST.get('password')

        if not username or not password:
            error = 'Both fields must be filled'
        if error:
            return render(request,"landing.html",{'error':error})

        user = Validate(username, password)
        if user:
            request.session['user'] = user
            return HttpResponseRedirect('/?allbooks')
        else:
            error = 'Username/Password do not match'
        if error:
            return render(request,"landing.html",{'error':error})

        #return HttpResponse("Login Successful!!")

    elif request.method == 'GET':
        return render(request, "login.html")



def test(request):
    user = request.session.get('user')
    if not user:
        return HttpResponse("No user logged in")
    else:
        return HttpResponse('Hello %s' % user.username)

def logout(request):
    del request.session['user']
    return HttpResponseRedirect('/')