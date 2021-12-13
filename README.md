# About

Simple web app to insert data into mongodb and get result in matching way. 

## Application Logic
1) Find values from mongodb against the input ORGANIZATION_ID and PARTIAL/FULL CONTACT NAME provided in the request body. The response would provide result SCORE and CONTACT NAME, which would be calculated on the basis of historical data for input.
2) Check the Abnormality of the data provided in the request with the historical data and give the result as Boolean. Abnormality is calculated using standard deviation and mean of historical AMOUNT corresponding to the ORGANIZATION_ID and PARTIAL/FULL CONTACT NAME.

## Virtual environments
To create a python virtual environment

### Get virtualenv package
```
$ sudo pip install virtualenv
```

If pip is missing on OSX you get this `easy_install`
```
$ easy_install pip
```

### Get python 3
```
$ brew install python3
```

### Create virtual environment
```
$ virtualenv venv
```

### Activate virtual environment
```
$ source venv/bin/activate
```

#### Installing new packages
```
$ pip install .
```

## Details Regarding Port on which application needs to be run can be set using
```
$ export PORT_VALUE=5000
```

## Every Other property is being set in config.ini
content of config.ini
```
[DEFAULT]
database_name=invoiceDB
collection_name=invoice
mongo_url=mongodb://localhost:27017/
```

## To Test the application
```
python -m unittest discover -s test -p InvoiceTestCases.py
```

## To run Python application
```
python run_invoice_api.py
```

The code in `run_invoice_api.py` is to launch the rest end point and start running on port 5000 if not other port provided

```
if __name__ == '__main__':
    port_number = os.getenv('PORT_VALUE', 5000)
    app.run(debug=False, port=int(port_number))
```

# API

## Add new invoice
```
$ curl -X 'POST' .:5000/addInvoice -d '{"_id":"unique-invoice-id","organization":"organization-id","createdAt":"2021-10-11T09:53:31.339Z","updatedAt":"2021-11-29T13:15:19.500Z","amount":{"currencyCode":"EUR","value":26.3},"contact":{"_id":"unique-contact-id","iban":"DE88100500001310032358","name":"Ani","organization":"organization-id"},"invoiceDate":"2021-10-11T00:00:00.000Z","invoiceId":"VR210230898"}'
```

## Update the contact information
```
$ curl -X 'POST' .:5000/updateContact -d '{"_id":"unique-contact-id","iban":"Hello","name":"Anirudh Sharma","organization":"organization-id"}'
```

## Get Abnoramlity of the data
```
$ curl -X 'POST' .:5000/checkAbnormalContactUri -d '{"organization":"organization-id","contactName":"Ani","amount":26.3}'
```
## Get Suggested invoice from the historical data
```
$ curl -X 'POST' .:5000/suggestContactInvoice -d '{"contactName":"Ani","organization":"organization-id"}'
```

## get invoice detail
```
$ curl  .:5000/invoice/unique-invoice-id
```

## Deactivate the virtual environment
```
$ deactivate
```
