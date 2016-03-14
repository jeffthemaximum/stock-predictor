import csv
from news_check.models import Company

'''
to seed
1) python3 manage.py shell
2) from news_check.seed import seed, seed_with_details
3) seed()
4) seed_with_details()
5) update_company_names()
5) dance.
'''


def seed():
    with open('news_check/helpers/data/fortune500stocksymbol.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "Symbol":
                # get symbol
                symbol = row[0]
                # get company name
                name = row[1]
                # get industry
                industry = row[2]
                # make company
                company = Company(
                    symbol=symbol,
                    full_name=name,
                    industry=industry
                )
                # save to db
                company.save()


def seed_with_details():
    bricks = 0
    companies = Company.objects.all()
    # gets list of all parts of slug
    companies_slugs = [(company.slug.split('-'), company.full_name) for company in companies]
    with open('news_check/helpers/data/fortune500details.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != "lon":
                # keep track of companies not found
                # get data from csv
                lon = float(row[0])
                lat = float(row[1])
                company = row[2]
                state = row[5]
                city = row[6]
                # check if company exists in db
                try:
                    # look through list of all companies
                    # get slug
                    for tup in companies_slugs:
                        saved = False
                        # convert company to lowercase
                        lc_company = company.lower()
                        # if any part of slug matches comapny.to_lower()
                        if lc_company in tup[0] or company == tup[1]:
                            # get index of company slug
                            idx = companies_slugs.index(tup)
                            # get company object from list of all companies
                            company_object = companies[idx]
                            # update with detail data
                            company_object.lon = lon
                            company_object.lat = lat
                            company_object.state = state
                            company_object.city = city
                            company_object.save()
                            saved = True
                        if saved is True:
                            print (company)
                except:
                    # print company and brick count
                    bricks += 1
                    print(company + " not found. Bricks: " + str(bricks))


def update_company_names():
    stupid = ['inc', 'plc', 'corp', 'co', 'corporation', 'Inc', 'Corp', 'Co']
    companies = Company.objects.all()
    for company in companies:
        # get company name
        name = company.full_name
        # get rid of commans and periods
        name = name.replace(",", "").replace(".", "")
        # split name into list
        name_list = name.split()
        # check if each word in name list in stupid
        for name_word in name_list:
            if name_word in stupid:
                # if so, delete it
                name_list.remove(name_word)
        # join name back together with spaces in between
        name = " ".join(name_list)
        # remove leading and trailing whitespace
        company.full_name = name
        company.save()
