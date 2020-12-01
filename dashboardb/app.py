from flask import Flask, render_template,request

import plotly
import plotly.graph_objs as go
import pandas as pd
import json
import numpy as np

import joblib

fixprice = pd.read_csv('./static/fixprice.csv')
app = Flask(__name__)


def category_plot(
    cat_plot = 'histplot',
    cat_x = 'neighbourhood', cat_y = 'bedrooms',
    estimator = 'count', hue = 'room_type'):

    # generate dataframe tips.csv
    # tips = pd.read_csv('./static/tips.csv')

    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in fixprice[hue].unique():
            hist = go.Histogram(
                x=fixprice[fixprice[hue]==val][cat_x],
                y=fixprice[fixprice[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Count Plot'
    elif cat_plot == 'boxplot':
        data = []

        for val in fixprice[hue].unique():
            box = go.Box(
                x=fixprice[fixprice[hue] == val][cat_x], #series
                y=fixprice[fixprice[hue] == val][cat_y],
                name = val
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# 1 home index
@app.route('/')
def index():
    plot = category_plot()
    

    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping

    list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot') ]
    list_x = [('property_type', 'Property type')]
    list_y = [('bedrooms', 'bedrooms')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('room_type','Room Type')]
    # list_hue = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term'), ('emp_length', 'Employment Length'), ('home_ownership', 'Home Ownership'), ('initial_list_status', 'Initial List Status'), ('application_type', 'Application Type')]
  # list_x = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term')]
    # list_y = [('int_rate', 'Interest Rate'), ('loan_amnt', 'Loan Amount'), ('installment', 'Installment'), ('annual_inc', 'Annual Income'), ('dti', 'Debt-to-Income Ratio'), ('pub_rec', 'Derogatory Public Record'), ('revol_bal', 'Revolving Balance'), ('mort_acc', 'Mortgage Account'), ('pub_rec_bankruptcies', 'Public Record of Bankruptcies')]
   
    return render_template('category.html', plot = plot, focus_plot = 'histplot', focus_x = 'property_type', focus_estimator = 'count', focus_hue = 'room_type', drop_plot = list_plot, drop_x = list_x, drop_y = list_y, drop_estimator = list_est, drop_hue = list_hue)


#2
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'property_type'
        cat_y = 'bedrooms'
        estimator = 'count'
        hue = 'room_type'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'count'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'bedrooms'

    # Dropdown menu
    list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot') ]
    list_x = [('property_type', 'Property type'),('neighbourhood_group', 'Neighbourhood Region'),('neighbourhood','neighbourhood'),('room_type','Room type')]
    list_y = [('bedrooms', 'bedrooms'),('price', 'Price'),('bathrooms','bathrooms'),('number_of_reviews','Total Reviews'),('review_scores_rating', 'Review Rating'),('cleaning_fee','cleaning fee'),('beds', 'Total Bed'),('guests_included', 'Total Guests')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('room_type','Room Type'), ('neighbourhood_group', 'Neighbourhood Region', 'instant_bookable','Booking Status'),('host_is_superhost', 'Superhost Status')]
    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    
    return render_template('category.html',plot=plot,focus_plot='histplot',focus_x='loan_status',focus_estimator='count',focus_hue='loan_status',drop_plot=list_plot,drop_x=list_x,drop_y=list_y,drop_estimator=list_est,drop_hue=list_hue)

#3 DATASET + PREDICTING
@app.route('/predict')
def prediction():
    fixprice = pd.read_csv("./static/fixprice.csv").head(100)
    fixprice.index.name = None
    titles = " "
    
    # data.to_html()
    return render_template('prediction.html', tables = [fixprice.to_html(classes = 'data', header = 'true')], titles = titles)

#4 Result
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        input = request.form
        # predicts = pd.DataFrame(data = [['North Region', 'Private room', 20, 20, 30, 12, 't', 'Apartment', 4, 3, 5, 80, 't', 3, 10, 10, 12,1]],
        # columns=['neighbourhood_group','room_type','minimum_nights','reviews_per_month','calculated_host_listings_count','availability_365','host_is_superhost','property_type','bedrooms','beds','guests_included','review_scores_rating','instant_bookable','bathrooms','security_deposit', 'cleaning_fee','len_amenities','budget_dorm'])
        # predicts = pd.DataFrame(data =[['North Region', 'Private room',20, 20, 30, 12, 't','Apartment', 4, 3, 5, 80, 't', 3, 10, 10, 12,1]], 
        # columns=['neighbourhood_group','room_type','minimum_nights','number_of_reviews','calculated_host_listings_count','availability_365','host_is_superhost','property_type','bedrooms','beds','guests_included','review_scores_rating','instant_bookable','bathrooms','security_deposit', 'cleaning_fee','len_amenities','budget_dorm'])
        neighbourhood_group = input['neighbourhood_group']
        room_type = input['room_type']
        minimum_nights = float(input['minimum_nights'])
        number_of_reviews = float(input['number_of_reviews'])
        calculated_host_listings_count = float(input['calculated_host_listings_count'])
        availability_365 = float(input['availability_365'])
        host_is_superhost = input['host_is_superhost']
        property_type = input['property_type']
        bedrooms = int(input['bedrooms'])
        beds = int(input['beds'])
        guests_included = int(input['guests_included'])
        review_scores_rating = int(input['review_scores_rating'])
        instant_bookable = input['instant_bookable']
        bathrooms = float(input['bathrooms'])
        security_deposit = float(input['security_deposit'])
        cleaning_fee = float(input['cleaning_fee'])
        len_amenities = int(input['len_amenities'])
        budget_dorm = int(input['budget_dorm'])

        
        model = joblib.load('AIRBNBMODELFINAL')
        data_pred = pd.DataFrame(data =[[neighbourhood_group,room_type,minimum_nights,number_of_reviews,calculated_host_listings_count,availability_365,host_is_superhost,property_type,bedrooms,beds,guests_included,review_scores_rating,instant_bookable,bathrooms,security_deposit,cleaning_fee,len_amenities,budget_dorm]],
								columns = ['neighbourhood_group','room_type','minimum_nights','number_of_reviews',
                                'calculated_host_listings_count','availability_365','host_is_superhost',
                                'property_type','bedrooms','beds','guests_included','review_scores_rating','instant_bookable','bathrooms','security_deposit','cleaning_fee','len_amenities',
                                'budget_dorm']
								)

		
        pred = model.predict(data_pred)[0]


        return render_template('result.html', 
        neighbourhood_group = neighbourhood_group, 
        room_type = room_type,
        minimum_nights = minimum_nights,
        number_of_reviews = number_of_reviews,
        calculated_host_listings_count = calculated_host_listings_count,
        availability_365 = availability_365,
        host_is_superhost = host_is_superhost,
        property_type = property_type,
        bedrooms = bedrooms,
        beds = beds,
        guests_included = guests_included,
        review_scores_rating = review_scores_rating,
        instant_bookable = instant_bookable,
        bathrooms = bathrooms,
        security_deposit = security_deposit,
        cleaning_fee = cleaning_fee,
        len_amenities = len_amenities,
        budget_dorm = budget_dorm,
        pred = (np.expm1(pred).round(2))
        )

if __name__ == '__main__':
    model = joblib.load('AIRBNBMODELFINAL')
    app.run(debug=True)