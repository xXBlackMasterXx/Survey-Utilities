from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np
import pyreadstat

import requests
import time
import wget
import os

import glob

from dotenv import load_dotenv
load_dotenv()

def sign_in_manager(driver : webdriver, email : str, password : str):
    # Go to the SynoInt login page
    driver.get("https://manager.synoint.com/login")
    
    # Enter the credentials and sign in
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
def get_survey_list(driver : webdriver, tracker_id : int):
    # Go to the project
    driver.get(f"https://manager.synoint.com/en/projects/{tracker_id}")

    # Wait until survey list loader is out
    element = WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "td.dataTables_empty")))

    # Read the table with the survey list
    survey_list = pd.read_html( driver.find_element(By.ID, "project-syno__surveys").get_attribute("outerHTML") )[0]
    
    # Return the dataframe with the survey list
    return survey_list

def generate_spss_data(driver : webdriver, survey_id : int):
    # Go to the results section
    driver.get(f"https://manager.synoint.com/en/syno-survey/surveys/{survey_id}/results")
    # Open the report modal
    driver.find_element(By.CSS_SELECTOR, ".file-export-form__button").click()
    driver.implicitly_wait(3)
    # File format: Raw data
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_fileFormat_1']").click()
    time.sleep(0.5)
    # Type: SPSS
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_fileType_3']").click()
    time.sleep(0.5)
    # Waiter until loads exportation options for SPSS
    element = WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".file-export-preloader__holder")))
    # Completes only: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_completesOnly']").click()
    time.sleep(0.5)
    # Include IP: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includeIp']").click()
    time.sleep(0.5)
    # Include panelist Id: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includePanelistId']").click()
    time.sleep(0.5)
    # Include indentity Id: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includeIdentityId']").click()
    time.sleep(2)
    # Click the export button
    driver.find_element(By.CSS_SELECTOR, ".file-export__submit-button").click()

    # Checks if element exists
    token_error = driver.find_elements(By.CSS_SELECTOR, ".export__form > div.pt-2 > span.alert")
    # If there is an error with the token form, resubmit the form again
    if len(token_error) > 0:
        print("Error token found!\t Resubmitting form again")
        driver.find_element(By.CSS_SELECTOR, ".file-export__submit-button").click()
    
    print(f"Report for survey {survey_id} is being generated")
    
def generate_excel_data(driver : webdriver, survey_id : int):
    """
    Generate an export file for the raw data
    """
    # Go to the results section
    driver.get(f"https://manager.synoint.com/en/syno-survey/surveys/{survey_id}/results")
    # Open the report modal
    driver.find_element(By.CSS_SELECTOR, ".file-export-form__button").click()
    driver.implicitly_wait(3)
    # File format: Raw data
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_fileFormat_1']").click()
    time.sleep(0.3)
    # Type: Excel
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_fileType_2']").click()
    time.sleep(0.3)

    # Waiter until loads exportation options
    element = WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".file-export-preloader__holder")))
    
    # Answers: Code (1), Label (2), Code & Label (3)
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_responseDataTemplate_1']").click()
    time.sleep(0.3)
    # Completes only: No
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_completesOnly']").click()
    time.sleep(0.5)
    # Include IP: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includeIp']").click()
    time.sleep(0.5)
    # Include panelist Id: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includePanelistId']").click()
    time.sleep(0.5)
    # Include indentity Id: Yes
    driver.find_element(By.CSS_SELECTOR, "label[for='export_form_includeIdentityId']").click()
    time.sleep(1)
    # Click the export button
    driver.find_element(By.CSS_SELECTOR, ".file-export__submit-button").click()
    
    # Checks if element exists
    token_error = driver.find_elements(By.CSS_SELECTOR, ".export__form > div.pt-2 > span.alert")
    # If there is an error with the token form, resubmit the form again
    if len(token_error) > 0:
        print("Error token found!\t Resubmitting form again")
        driver.find_element(By.CSS_SELECTOR, ".file-export__submit-button").click()
    
    print(f"Report for survey {survey_id} is being generated")
    
    
def download_raw_data(driver : webdriver, survey_id : int):
     # Go to the generated reports section
    driver.get(f"https://manager.synoint.com/en/syno-survey/export/{survey_id}")
    # Waiter until loads exportation files list
    element = WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".file-export-preloader__holder")))
    
    try:
        is_file_exported = WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(9) > i")))
        downloable_file = driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(9) > div").get_attribute("data-content")
        filename = wget.download(downloable_file, os.environ["DATA_DIR"])
        print(f"File {filename} was downloaded")
    except:
        print("Reports is still being generated, trying again...")
        download_raw_data(driver, survey_id)
        
def read_data(directory = os.environ["DATA_DIR"]):
    """
    Read the data from the specified folder
    
    Params: 
        directory
            - Default (data), if not specified. Can be overwritten by another location
    """
    print(f"Reading from directory: {directory}")
    data = pd.DataFrame()

    filenames = glob.glob(directory + '*.sav') # os.listdir(directory)
    for filename in filenames:
        print(f"Reading file: {filename}")
        sav, meta = pyreadstat.read_sav(filename, apply_value_formats=True)
        data = pd.concat([data, sav], axis = 0)
        
    return data

def read_distribution(directory = os.environ["DISTRIBUTION_DIR"]):
    """
    Reads a csv file from a specified directory
    
    Params: 
        directory
            - By default the directory `data` is read. It can be overwritten by another location
    """
    print(f"Reading from directory: {directory}")

    # Concat all distribution files
    distribution_bg = pd.DataFrame()

    for distribution_file in glob.glob(directory + '*.csv'): # os.listdir(directory):
        print(f"Reading file: {distribution_file}")
        # Read the current filename 
        df = pd.read_csv(distribution_file)
        # Filter out columns of interesst
        df.drop("Unnamed: 8", axis = "columns", inplace=True)
        df.rename(columns={"GUID" : "guid", "Target group" : "Target group (Distribution)"}, inplace=True)
        # Concat dataframes by rows
        distribution_bg = pd.concat([distribution_bg, df], axis = "index")

    return distribution_bg

def read_purespectrum(directory = os.environ["PURESPECTRUM_DIR"]):
    print(f"Reading from directory: {directory}")
    
    # Concat all closed files
    purespectrum_bg = pd.DataFrame()

    for purespectrum_file in glob.glob(directory + '*.csv'): # os.listdir(directory):
        print(f"Reading file: {purespectrum_file}")
        # Read the current filename 
        df = pd.read_csv(purespectrum_file)
        # Filter out columns of interest
        df = df[["Survey ID", "Project Name", "PSID", "Transaction ID", "Survey Country", "Survey Language", "Respondent Status Description", "IP", "UserAgent"]].reset_index(drop=True)
        df.rename(columns={"Transaction ID" : "guid", "Project Name" : "Project Name (PureSpectrum)"}, inplace=True)
        # Concat dataframes by rows
        purespectrum_bg = pd.concat([purespectrum_bg, df], axis = "index")

    return purespectrum_bg

def read_lucid(directory = os.environ["LUCID_DIR"]):
    print(f"Reading from directory: {directory}")

    # Concat all files from Lucid
    lucid_bg = pd.DataFrame()
    
    for lucid_file in glob.glob(directory + '*.csv'): # os.listdir(directory):
        print(f"Reading file: {lucid_file}")
        # Read the current filename
        df = pd.read_csv(lucid_file)
        # Filter out columns of interest
        df = df[["Response ID", "PID", "SurveyName",  "SupplierName", "IsLive", "EntryDate", "LastDate", "FulcrumStatus", "ClientStatus", "ResponseStatus", "SupplierLinkTypeName", "RedirectURL"]].reset_index(drop=True)
        df.rename(columns={"Response ID" : "guid", "SurveyName" : "SurveyName (Lucid)"}, inplace=True)

        # lowercase all Response IDs
        df["guid"] = df["guid"].str.lower()

        # Concat dataframes by rows
        lucid_bg = pd.concat([lucid_bg, df], axis = "index")

    return lucid_bg

def lucidRemoves(lucid, data):
    # Complete that we must have as complete in Lucid
    lucid_match = lucid[lucid["guid"].isin( data[ (data["source"] == "Lucid") & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]
    # Respondents to remove in Lucid
    lucid_removes = lucid[
        (~lucid["guid"].isin( lucid_match["guid"])) & # Filter non matched Survey completes
        (lucid["ResponseStatus"] == "Complete") # Filter only completes in Lucid that di not matched in Surveys
    ]

    return lucid_removes

def lucidAdds(lucid, data):
    # Completes that we must have as complete in Lucid
    lucid_match = lucid[lucid["guid"].isin( data[ (data["source"] == "Lucid") & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]
    # Respondents to add in Lucid
    lucid_add = lucid_match[lucid_match["ResponseStatus"] != "Complete"]
    
    return lucid_add

def pureRemoves(pure, data):
    # Completes that we must have as complete in PureSpectrum
    pure_match = pure[pure["guid"].isin( data[ (data["source"] == "Pure Spectrum") & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]
    # Respondents to remove in PureSpectrum
    pure_removes = pure[
        (~pure["guid"].isin( pure_match["guid"])) &  # Filter non matched Survey completes
        (pure["Respondent Status Description"] == "Complete") # Filter only completes in Pure that did not matched in Surveys
    ]

    return pure_removes

def pureAdds(pure, data):
    # Completes that we must have as complete in PureSpectrum
    pure_match = pure[pure["guid"].isin( data[ (data["source"] == "Pure Spectrum") & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]
    # Respondents to add in PureSpectrum
    pure_add = pure_match[pure_match["Respondent Status Description"] != "Complete"]
    # pure_add.to_excel("pure_add.xlsx", index = False)
    
    return pure_add

def distributionRemoves(distribution, data):
    # Completes that we must have as completes in Distribution
    distribution_match = distribution[distribution["guid"].isin( data[ (data["source"].isin(["Cint", "Syno"])) & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]

    # Respondents to remove in Distribution
    distribution_removes = distribution[
        (~distribution["guid"].isin( distribution_match["guid"] )) &
        (distribution["Status"] == "Complete")
    ]

    return distribution_removes

def distributionAdds(distribution, data):
    # Completes that we must have as completes in Distribution
    distribution_match = distribution[distribution["guid"].isin( data[ (data["source"].isin(["Cint", "Syno"])) & (data["status"] == "complete") & (data["mode"] == "live") ]["guid"] )]

    # Respondents to add in Distribution
    distribution_add = distribution_match[distribution_match["Status"] != "Complete"]
    
    return distribution_add

def format_sheet(writer, sheet_name, data):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 9})  # This line is correct, assuming the engine is 'xlsxwriter'
    print(f"This operation will affect {data.shape[0] * data.shape[1]} cells, please be patient")
    for col_num, value in enumerate(data.columns.values):
        worksheet.set_column(col_num, col_num, 12.5, cell_format)  # Example of setting column width and format