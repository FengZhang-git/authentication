# Final-Project

Web Programming with Python and JavaScript

## Overview
In this project, I build an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. If the user paid for the food, then I will send an email to the user. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed. I write test program，and every time I submit new changes to Github, Travis CI can run the test programs automatically.

## Milestones
- Complete the User, Authentication, and Registration/Login/Logout steps.
- Complete the Menu, Food, Order and Adding/Deleting Items steps.
- Complete the Viewing Orders and Changing orders' status steps.
- Complete the Shopping Cart and Placing an Order steps.
- Complete the Payment and Sending emails steps.
- Compltet the Testing, Travis-CI steps.
- Complete Scalability and Security Analysis steps

## Methods to start
1. Download the source files from here and then run `python manage.py runserver`
2. Superuser: username:zhangfeng,password:zhangfeng
3. You can register a new account or log in as feng(pw=feng)

## Details
- **Menu:** My web application support all of the available menu items for [Pinnochio’s Pizza & Subs ](http://www.pinocchiospizza.net/menu.html)(a popular pizza place in Cambridge). I add my models to `orders/models.py`, make the necessary migration files, and apply those migrations.
- **Adding Items:** Using Django Admin, site administrators (restaurant owners) are able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into my database using either the Admin UI or by running Python commands in Django’s shell.
- **Registration, Login, Logout:** Site users (customers) are able to register for my web application with a username, password. Customers are able to log in and log out of my website.
- **Shopping Cart:** Once logged in, users will see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping can be saved even if a user closes the window, or logs out and logs back in again.
- **Placing, Deleting an Order:** Once there is at least one item in a user’s shopping cart, they are able to place an order, and the total fee of orders is also in shopping cart. Users can decide to pay for food or delete particular orders before paying.
- **Paying an Order:** Integrate with the [Stripe](https://stripe.com/docs) API to allow users to actually use a credit card to make a purchase during checkout, and support sending users a confirmation email once their purchase is complete.
- **Viewing Orders:** Site administrators have access to a page where they can view any orders that have already been placed.
- **Personal Touch:**  Site administrators can mark orders as complete and allowing users to see the status of their pending or completed orders.
- **Test:**  Configure [Travis](https://travis-ci.org/) and sync my GitHub account. Any repositories that should be tracked by Travis can be selected. After making a push to GitHub, it can be visible on the Travis website as a ‘build’ and will execute the commands as dictated in the configuration file. But Travis is only free for public repositories, so I create the same repository called [`authentication`](https://github.com/FengZhang-git/authentication)

## Source files
```
│  .travis.yml
│  db.sqlite3
│  manage.py
│  requirements.txt
│  result.txt
│  
├─authentication
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │  
│  └─__pycache__
│         ...
│          
├─orders
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  myemail.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│  │    ...
│  │          
│  ├─static
│  │  ├─images
│  │  │      pinocchio_72.gif
│  │  │      
│  │  └─orders
│  │          food.css
│  │          styles.css
│  │          
│  ├─templates
│  │  └─orders
│  │          base.html
│  │          cart.html
│  │          checkout.html
│  │          error.html
│  │          food.html
│  │          menu.html
│  │          success.html
│  │          topping.html
│  │          
│  └─__pycache__
│         ...
│          
└─users
    │  admin.py
    │  apps.py
    │  models.py
    │  tests.py
    │  urls.py
    │  views.py
    │  __init__.py
    │  
    ├─migrations
    │  │  ...
    │          
    ├─templates
    │  └─users
    │          base.html
    │          login.html
    │          register.html
    │          user.html
    │          
    └─__pycache__
            ...
```


## [Stripe: Online payment processing for internrt businesses](https://stripe.com/)
### [Accept a payment](https://stripe.com/docs/payments/accept-a-payment-charges#web-setup)
  Realted source files:

```  
├─orders
│  │  views.py
│  ├─templates
│  │  └─orders
│  │          checkout.html
```

  `orders/views.py`

```python
  import stripe
  def success(request):
      # Set your secret key. Remember to switch to your live secret key in production!
      # See your keys here: https://dashboard.stripe.com/account/apikeys
      stripe.api_key = 'this is my secret key.'

      # Token is created using Stripe Checkout or Elements!
      token = request.POST["stripeToken"]
      charge = stripe.Charge.create(
          amount=int(total),
          currency='usd',
          description='Example charge',
          source=token,
        )
```
Once users paid successfully, they will receive an email, and the server will submit the charge to my account. Then I can find the charge in my account. For example, because this is my test account, so you can just type like the follwing image.![pay example](https://github.com/FengZhang-git/final-project-FengZhang-git/blob/master/images/stripeexample.png)  
![my stripe account](https://github.com/FengZhang-git/final-project-FengZhang-git/blob/master/images/stripe2.png)

### Problem
  `Request req_00QUHrogThCJaw: Invalid integer: 17710.0`: When create a charge, the `amount` must be integer.
  *Solution: `anount=int(total)`*

### Related Learning Material
- YouTube Channel: [Python Tutorial // How to Use Stripe Payments wth Django](https://www.youtube.com/watch?v=6aQanCJZx04)
- Github repository:[A basic shopping cart for digital products. Made with Django](https://github.com/justdjango/Shopping_cart)

## Sending Email
### Here are four basic steps for sending emails using Python:
    1. Set up the SMTP server and log into your account.
    2. Create the `MIMEMultipart` message object and load it with appropriate headers for `From`, `To`, and `Subject` fields.
    3. Add your message body.
    4. Send the message using the SMTP server object.
  The corresponding source file, `orders/myemail.py`  
  *Attention: When you `from email.mime.text import MIMEText`, you don't need install any module, if it has error like this `ModuleNotFoundError: No module named 'email.mime'; 'email' is not a package`, it's just because you named the file 'email.py'. So you can only  rename the file and then you can make it. For example, run `python myemail.py`*
### Related Learning Materials
 - [简单三步，用 Python 发邮件](https://zhuanlan.zhihu.com/p/24180606)

## [Travis-CI](https://travis-ci.org/)
### Overview
  When code is pushed to GitHub, GitHub will notify Travis of those changes. Travis will pull that code and run some tests on it. GitHub will then be notified of the test results.Travis’s configuration file, which lists any tests, installations, etc., is written in the YAML file format.  
  `.travis.yml`:
  ```yml
    language: python
    python:
        - 3.7
    install:
        - pip install -r requirements.txt
    script:
        - python manage.py test
  ```
  Once I push code to Github, Travis will build the corresponding repository automatically. For example, ![travis build result1](https://github.com/FengZhang-git/final-project-FengZhang-git/blob/master/images/travis1.png)![travis build result2](https://github.com/FengZhang-git/final-project-FengZhang-git/blob/master/images/travis2.png)
### Materials
  - YouTube Channel: [Travis CI Tutorial - How to Use Travis CI with Github for Continuous Integration](https://www.youtube.com/watch?v=Uft5KBimzyk)

## Django
### [Making queries](https://docs.djangoproject.com/en/3.0/topics/db/queries/)
- Creating objects
  ```python
    user = User.objects.create_user(username, email, password)
  ```
- Saving changes to objects, always remember save the changes.
  ```python
    order.status = 'M'
    order.save()
  ```
- Retrieving specific objects with filters
  ```python
    currentOrders = user.hasorders.filter(is_paid=False)
    historyOrders = user.hasorders.exclude(is_paid=False)
  ```
- Retrieving a single object with `get()`
  ```python
    Food.objects.filter(type=Type.objects.get(name="Salad"))
  ```
### [Model Field Types](https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types)
- BooleanField
- CharField
- DateTimeField
  - `auto_now`: update timestamp
  - `auto_now_add`: setup timestamp
- FloatField
- IntegerField
- ForeignKey
- ManyToManyField
### [Using the Django authentication system](https://docs.djangoproject.com/en/3.0/topics/auth/default/)
- Creating users
  ```python
  from django.contrib.auth.models import User
  user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  user.save()
  ```
- Creating superusers
  ```
    python manage.py createsuperuser
  ```
### request
- Get current user
  ```python
  def cart(request):
      user = request.user
  ```
- Decide current user whether loged in
  ```python
  def index(request):
      if not request.user.is_authenticated:
          return render(request, "users/register.html", {"message": None})
      else:
          ...
  ```

## Python
  - Float
    ```python
      a = 5.026
      a = float('%.2f' % a)
      Out[]: 5.03
    ```
  - String
    ```python
      astring = 'helloworld'
      if 'world' in astring:
        print 'Exist'
      else:
        print 'Not exist'
    ```
  - `IndentationError: unindent does not match any outer indentation level`  
    *Solution: Check indentation and spaces*
## Problem

  1. `Travis CI can't build`  
    **Reason:** `.travis.yml` must be in the root directory, not can be in the other directory!!!!!

  2. `Travis ModuleNotFoundError: No module named 'orders'`
    **Reason:** `orders` directory was not submitted on the Github!!!

  3. The version of module in python:  
    ```
      import django
      django.__version__
      '2.2.7'
    ```
  4. `tree [path] /f > [outpath]`: Output the structure of directory of path
  5. Import module in python: we want to import `file3.py` in `file4.py`  
      ```
        -- dir
        　　| file1.py
        　　| file2.py
        　　| dir3
        　　　| __init__.py
        　　　| file3.py
        　　| dir4
        　　　| file4.py
      ```
    **Solution:**  

  ```python
    import sys
    sys.path.append("..")
    form dir3 import file3
  ```
