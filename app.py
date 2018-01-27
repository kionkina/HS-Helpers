from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import user
from util import db, scrape2
from lxml import html
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep
from util import productdb
import sys
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(32)
print sys.path

@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session:
        return redirect(url_for("HS_homepage"))
    return render_template("landing.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        print("You're already logged in!")
        return redirect(url_for("HS_homepage"))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if "username" not in session:
        return render_template("signin.html")
    else:
        print("You're already logged in!")
        return redirect(url_for("HS_homepage"))



@app.route('/HS_homepage', methods = ["GET", "POST"])
def HS_homepage():
    if "username" in session:
        username = session["username"]
        return render_template("HS_homepage.html")
    return render_template("landing.html")

@app.route('/auth', methods = ["GET", "POST"])
def auth():
    #user already logged in
    if "username" in session:
        return redirect(url_for("HS_homepage"))
    if request.method == "GET":
        #user went to /auth without logging in
        return redirect("/")
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        print("Please fill out all fields")
        return render_template("signin.html")
    #login authenticated!
    print db.check_credentials(username,password)
    if db.check_credentials(username,password):
        session['username'] = username
        print("Successfully logged in")
        return redirect(url_for('HS_homepage'))
    else:
        print("Failed login")
        return redirect(url_for('signin'))

@app.route('/signauth', methods = ["GET", "POST"])
def signauth():
    try:
        #user filled out everything
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        info = request.form['info']
    except KeyError:
        print("Please fill out all fields")
        return render_template("signup.html")
    if password != password2:
        print("Passwords don't match")
        return render_template("signup.html")
    if username == "" or password == "" or password2 == "":
        print("Fields must not be blank")
        return render_template("signup.html")
    print db.add_company(username,  email, password, info)
    if db.add_company(username,  email, password, info):
        #success! username and password added to database
        print("Successfully created!")
        session['username'] = username
        return redirect(url_for('HS_homepage'))
    else:
        #username couldn't be added to database because it already exists
        print("Username taken")
        return redirect(url_for('signup'))


@app.route('/logout')
def logout():
    if "username" not in session:
        print("You aren't logged in")
        return redirect(url_for('signin'))
    session.pop("username")
    print("You've been logged out")
    return redirect(url_for('index'))



# Passes this variable into every view
@app.context_processor
def logged_in():
    if "username" in session:
        return dict(logged_in=True)
    return dict(logged_in=False)

#@csrf.exempt
@app.route('/ajax_helper', methods=['GET','POST'])
def ajax_helper():
    print "running..."
    url = request.form['link']
    the_username = session['username']
    print the_username
    quantity = request.form['qty']
    print quantity
    company = request.form['company']
    print company
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
#    while True:
    #sleep(3)
    try:
        doc = html.fromstring(page.content)
        XPATH_NAME = '//h1[@id="title"]//text()'
        XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
        XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
        XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
        XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

        RAW_NAME = doc.xpath(XPATH_NAME)
        RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
        RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
        RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

        NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
        CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
        ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

        if not ORIGINAL_PRICE:
            ORIGINAL_PRICE = SALE_PRICE

        if page.status_code!=200:
            raise ValueError('captha')
        data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    }

        extracted_data = []
        url = "https://www.amazon.com/Headphones-Otium-Waterproof-Sweatproof-Cancelling/dp/B018APC4LE/ref=sr_1_5?ie=UTF8&qid=1517035633&sr=8-5&keywords=headphones"
        #print "Processing: "+url
        extracted_data.append(data)
        #sleep(5)
        price = extracted_data[0]['SALE_PRICE']
        print extracted_data
        time = datetime.datetime.now()
        time = (str(time))
        #print price
        #print the_username
        productname = extracted_data[0]['NAME']
        productdb.add_product(price, productdb.get_current_number(), quantity, productname, the_username, company, time)
        productdb.print_table()
        return price

    except Exception as e:
            print e




@app.route('/d_dashboard')
def d_dashboard():
    return render_template('d_dashboard.html')



@app.route('/add_item')
def add_item():
    if "username" in session:
        return render_template("add_item.html")
    else:
        return render_template("landing.html")


if __name__ == '__main__':
    app.run(debug=True)
