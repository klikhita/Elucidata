from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import xlrd
import os
import xlsxwriter
import numpy as np
import io as io
try:
    from io import BytesIO as IO
except ImportError:
    from io import StringIO as IO

global uploaded_file_url,filename,path
uploaded_file_url=''
filename=''
path = r'C:\Users\Likhita\elucidata\media'

def index(request):
    global uploaded_file_url,filename,path

    if request.method== 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        print('-----------------',uploaded_file_url)
        print('---------------',filename)
        return render(request,'API-1.html')
    return render(request,'index.html')

def api1(request):
    #global uploaded_file_url, filename, path
    if request.method=='POST':
        cs_yes=request.POST.get('childset','yes')
        if(cs_yes=='yes'):
            #print('-------------------------',os.path.join(path,filename))
            #print('--------------',filename)
            df=pd.read_excel(os.path.join(path,filename))
            #print(df)
            dim=df.shape
            rows=dim[0]

            output = IO()

            workbook=xlsxwriter.Workbook(output)
            worksheet1=workbook.add_worksheet('LPC')
            worksheet2 = workbook.add_worksheet('PC')
            worksheet3 = workbook.add_worksheet('plasmologen')
            n1=0
            n2=0
            n3=0

            for i in range(rows):
                name=str(df['Accepted Compound ID'][i])
                if(name[-3:]=='LPC'):
                    worksheet1.write_row(n1, 0, df.iloc[i])

                    n1+=1
                elif name[-2:]=='PC':

                    worksheet2.write_row(n2,0,df.iloc[i])
                    n2+=1
                elif name[-11:]=='plasmalogen':
                    worksheet3.write_row(n3, 0, df.iloc[i])

                    n3+=1
            workbook.close()
            output.seek(0)
            response=HttpResponse(output.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition']='attachment;filename=output.xlsx'

            return response

    return render(request,'API-1.html')


def api2(request):
    if request.method=='POST':
        round_yes=request.POST.get('roundoff','yes')
        if(round_yes=='yes'):
            df = pd.read_excel(os.path.join(path, filename))


            df['Retention time round off (in mins)']=df['Retention time (min)'].apply(np.round)
            df.to_excel(os.path.join(path, filename))


    return render(request,"API-2.html")


def api3(request):
    if request.method=='POST':
        mean_yes=request.POST.get('mean','yes')
        if(mean_yes=='yes'):
            df = pd.read_excel(os.path.join(path, filename))
            print('-------------------------------',type(df))

            df.drop(['m/z','Retention time (min)','Accepted Compound ID'], axis=1)

            #print('After adding-----------',columns)
            result=IO()
            workbook=xlsxwriter.Workbook(result)
            worksheet=workbook.add_worksheet()
            m=df.groupby('Retention time round off (in mins)').agg({'mean'})
            print(m)
            m_dim=m.shape
            m_rows=m_dim[0]
            n=0
            for i in range(m_rows):
                cell=str(m.iloc[i])
                worksheet.write_row(n,0,cell)
                n+=12

            workbook.close()
            result.seek(0)

            response = HttpResponse(result.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment;filename=result.xlsx'

            return response


    return render(request,'API-3.html')


