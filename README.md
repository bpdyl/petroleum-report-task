How to run

1. Navigate to the directory where you want to keep this project
2. mkdir yourfolder_name
3. cd yourfolder_name
4. virtualenv venv (you can name whatever you want ,here i named it venv )
5. source venv/bin/activate
6. git clone https://bitbucket.org/bibek_pdyl/challenges-yi/src/main/
7. pip install -r requirements.txt
8. python manage.py runserver

API created for the reports are :
1. Total sales per product : https://petroleumreports.herokuapp.com/api/sales_per_product/

2. Top 3 countries that have the highest and lowest total sales till date: https://petroleumreports.herokuapp.com/api/top_sales_per_country/

3. Average sale of each petroleum product for 4 years of interval: https://petroleumreports.herokuapp.com/api/average_sales/