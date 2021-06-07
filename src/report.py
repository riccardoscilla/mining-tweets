from html_reports import Report
import pandas as pd
import matplotlib.pyplot as plt

class report:
    def __init__(self):
        self.rep = Report()

    def add_title(self, title, level=1):
        self.rep.add_title(title, level)

    def add_text(self, text):
        self.rep.add_markdown(text)

    def add_parameters(self, trans, sup, tsup):
        self.single_param("Transactions",trans)
        self.single_param("Support Threshold",sup)
        self.single_param("Temporal Support Threshold",tsup)

    def single_param(self, tipo, lista):
        if len(lista)>1:
            text = tipo+": ["
        else:
            text = tipo+": "

        for i in range(len(lista)):
            text += str(lista[i])
            if i < len(lista) - 1:
                text += ", "
        if len(lista)>1:
            text += "]"  
        self.add_title(text,4)
        

    def add_plot(self):
        self.rep.add_figure()

    def add_table(self,table):
        CSS = 'table border 0px solid black'
        table = table.to_html(classes=CSS)
        self.rep.body.append(table)


    def write(self, name):
        self.rep.write_report(filename=name)
