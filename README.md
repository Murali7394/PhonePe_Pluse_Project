# Digital Payments In India
Digital payment transactions have significantly increased as a result of coordinated efforts of the Government as a whole, along with all stake holders concerned, from 2,071 crore transactions in FY 2017-18 to 8,840 crore transactions in FY 2021-22 (Source: RBI, NPCI and banks).

During last five years, various easy and convenient modes of digital payments, including Bharat Interface for Money-Unified Payments Interface (BHIM-UPI), Immediate Payment Service (IMPS), and National Electronic Toll Collection (NETC) have registered substantial growth and have transformed digital payment ecosystem by increasing person-to-person (P2P) as well as person-to-merchant (P2M) payments.

**BHIM UPI** has emerged as the preferred payment mode of the citizens and has recorded 803.6 crore digital payment transactions with the value of ₹ 12.98 lakh crore in January 2023.

Payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-art payments infrastructure built as Public Goods championed by the central bank and the government.

# Phone phe
Phonephe is a strong player in API driven digitisation of payments in India.They have bagged a considerable amount of transactions in the BHIM UPI transactions over all the regions of the country. Phone phe have shared that data for the data and developer community to  work on the data to get valuable insights on digital payments.

Data  [Phoneohe Repository link](https://github.com/PhonePe/pulse.git)
### Data
The Data Set consists of three categories
1. Aggregated
2. Map
3. Top

Each section in the data has transactions and users data for India and states.
## Data Extraction 
1. Data from the git hub repository is cloned using os module.
2. By traversing through the folders in the cloned repository getting the data that fits for analysis for each of the above 
   mentioned categories.
3. After collecting all the data for one category it is stored in a comma separated file(csv) for analysis.
4. Based on the categories we have extracted transactions and users data for India , States, Districts, Pincodes
# Processing of Data and Storing in SQL:
1. The extracted csv files are preprocessed and some formats have been changed and stored in sqlite3 database.
# Streamlit Application
An Interactive streamlit application is created using the extracted data to explore how the digital transactions is growing.
[Phone Phe dashboard](http://192.168.1.5:8501)
## INSIGHTS
1. All the observed insights are in the insights page of the dashboard [Phone Phe dashboard](http://192.168.1.5:8501)







