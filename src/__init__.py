from flask import Flask

app = Flask(__name__)

from src import addNewInvoice
from src import getAbnormalContact
from src import getMatchContactInvoice
from src import updateContactDetails
from src import page_error
from src import getInvoice