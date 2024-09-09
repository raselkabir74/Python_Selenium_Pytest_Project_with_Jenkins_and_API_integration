import json
import os
import time

import pytest

from configurations import generic_modules
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.invoice_list_locator import InvoiceListLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from locators.io.proforma_form_locator import ProformaFormLocators
from locators.io.proforma_list_locator import ProformaListLocators
from locators.io.payments_log_locator import PaymentsLogLocators
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.invoice_list import DspDashboardInvoiceList
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.io.payments_log import DspDashboardPaymentsLog
from pages.io.proforma_form import DspDashboardProformaForm
from pages.io.proforma_list import DspDashboardProformaList
from pages.io.credit_note_form import DspDashboardICreditNoteForm
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.compare import CompareUtils as CompareUtil
from utils.io import IoUtils
from utils.page_names_enum import PageNames

global url
debug_mode = "JENKINS_URL" not in os.environ


@pytest.mark.dependency()
def test_regression_add_and_edit_io(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    # PROVIDED IO DATA IN GUI
    global url, debug_mode
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/io_data.json', 'w') as json_file:
        json.dump(io_data, json_file)

    with open('assets/io/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)
    io_edit_data['io_main_information']['io_title'] = \
        io_edit_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/io_edit_data.json', 'w') as json_file:
        json.dump(io_edit_data, json_file)

    with open('assets/io/invoice_data.json') as json_file:
        invoice_data = json.load(json_file)
    invoice_data['invoice_main_information']['invoice_title'] = \
        io_edit_data['io_main_information']['io_title']
    with open('assets/temp/invoice_data.json', 'w') as json_file:
        json.dump(invoice_data, json_file)

    with open('assets/io/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)
    invoice_edit_data['invoice_main_information']['invoice_title'] = \
        invoice_edit_data['invoice_main_information'][
            'invoice_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/invoice_edit_data.json', 'w') as json_file:
        json.dump(invoice_edit_data, json_file)

    with open('assets/io/proforma_data.json') as json_file:
        proforma_data = json.load(json_file)
    proforma_data['proforma_main_information']['proforma_title'] = \
        io_edit_data['io_main_information']['io_title']
    with open('assets/temp/proforma_data.json', 'w') as json_file:
        json.dump(proforma_data, json_file)

    with open('assets/io/proforma_edit_data.json') as json_file:
        proforma_edit_data = json.load(json_file)
    proforma_edit_data['proforma_main_information']['proforma_title'] = \
        proforma_edit_data['proforma_main_information'][
            'proforma_title'] + generic_modules.get_random_string(
            5)
    with open('assets/temp/proforma_edit_data.json', 'w') as json_file:
        json.dump(proforma_edit_data, json_file)

    # IO CREATION
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.navigate_to_add_io()
    url = io_form_page.provide_io_data_and_save(io_data)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # DATA VERIFICATION
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
    pulled_io_data_gui = io_form_page.get_io_information_from_gui(io_data)
    assert generic_modules.ordered(pulled_io_data_gui) == generic_modules.ordered(io_data)

    # EDIT CREATED IO
    io_form_page.provide_io_data_and_save(io_edit_data, edit_io=True)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # DATA VERIFICATION AFTER EDIT
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
    pulled_io_data_gui_after_edit = io_form_page.get_io_information_from_gui(
        io_edit_data)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_io_data_gui_after_edit,
        io_edit_data)


@pytest.mark.dependency(depends=['test_regression_add_and_edit_io'])
def test_regression_add_and_edit_invoice(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_list_page = DspDashboardIoList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    credit_note_page = DspDashboardICreditNoteForm(driver)

    # PROVIDED IO DATA IN GUI
    global url, debug_mode

    with open('assets/temp/invoice_data.json') as json_file:
        invoice_data = json.load(json_file)

    with open('assets/temp/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)

    with open('assets/io/payment_data.json') as json_file:
        payment_data = json.load(json_file)

    with open('assets/io/credit_note_data.json') as json_file:
        credit_note_data = json.load(json_file)

    with open(
            'assets/io/payment_data_after_credit_note.json') as json_file:
        payment_data_after_credit_note = json.load(json_file)

    # INVOICE CREATION
    driver.get(url)
    io_list_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    io_list_page.wait_for_presence_of_element(
        InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    io_list_page.wait_for_visibility_of_element(
        InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    io_list_page.wait_for_element_to_be_clickable(
        InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    invoice_url = driver.current_url
    io_list_page.wait_for_visibility_of_element(
        InvoiceFormLocators.success_message_locator)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

    # DATA VERIFICATION
    driver.get(invoice_url)
    pulled_invoice_data_gui = invoice_form_page.get_invoice_information_from_gui(
        invoice_data)
    print(generic_modules.ordered(pulled_invoice_data_gui))
    print(generic_modules.ordered(invoice_data))
    assert generic_modules.ordered(
        pulled_invoice_data_gui) == generic_modules.ordered(
        invoice_data)

    # EDIT CREATED INVOICE
    invoice_form_page.provide_invoice_data_and_save(invoice_edit_data,
                                                    edit_invoice=True)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

    # DATA VERIFICATION AFTER EDIT
    driver.get(invoice_url)
    pulled_invoice_data_gui_after_edit = invoice_form_page.get_invoice_information_from_gui(
        invoice_edit_data)
    print(generic_modules.ordered(pulled_invoice_data_gui_after_edit))
    print(generic_modules.ordered(invoice_edit_data))
    assert generic_modules.ordered(
        pulled_invoice_data_gui_after_edit) == generic_modules.ordered(
        invoice_edit_data)

    # INVOICE PAYMENT
    assert invoice_form_page.calculate_and_verify_vat_discount_and_total_amount_from_ui(
        invoice_edit_data)
    invoice_form_page.add_payment_into_invoice(payment_data)
    assert "Invoice payment has been added!" in invoice_form_page.get_success_message()
    pulled_payment_data = invoice_form_page.get_payment_data(
        table_number="2",
        row_number="1")
    assert generic_modules.ordered(
        pulled_payment_data) == generic_modules.ordered(payment_data)
    pulled_total_payment_data = invoice_form_page.get_payment_data(
        table_number="2", row_number="2")
    assert generic_modules.ordered(
        pulled_total_payment_data) == generic_modules.ordered(
        payment_data)

    # CREDIT NOTE
    credit_note_page.add_credit_note_into_invoice(credit_note_data)
    credit_invoice_url = driver.current_url
    assert "Credit note saved successfully!" in credit_note_page.get_success_message()

    # DATA VERIFICATION FOR CREDIT NOTE
    driver.get(credit_invoice_url)
    pulled_credit_note_data = credit_note_page.get_credit_invoice_data()
    print(generic_modules.ordered(pulled_credit_note_data))
    print(generic_modules.ordered(credit_note_data))
    assert generic_modules.ordered(pulled_credit_note_data) == generic_modules.ordered(credit_note_data)

    # DATA VERIFICATION FOR CREDIT NOTE FROM INVOICE FORM PAGE
    driver.get(invoice_url)
    pulled_payment_data_after_credit_note = invoice_form_page.get_payment_data_after_credit_note()
    print(generic_modules.ordered(pulled_payment_data_after_credit_note))
    print(generic_modules.ordered(payment_data_after_credit_note))
    assert generic_modules.ordered(
        pulled_payment_data_after_credit_note) == generic_modules.ordered(
        payment_data_after_credit_note)


@pytest.mark.dependency(
    depends=['test_regression_add_and_edit_io',
             'test_regression_add_and_edit_invoice'])
def test_regression_add_and_edit_proforma(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    proforma_form_page = DspDashboardProformaForm(driver)
    proforma_list_page = DspDashboardProformaList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/temp/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)

    with open('assets/temp/proforma_data.json') as json_file:
        proforma_data = json.load(json_file)

    with open('assets/temp/proforma_edit_data.json') as json_file:
        proforma_edit_data = json.load(json_file)

    with open('assets/io/payment_data.json') as json_file:
        payment_data = json.load(json_file)

    # PROFORMA CREATION
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.search_by_title(
        io_edit_data['io_main_information']['io_title'])
    io_list_page.click_on_element(IoListLocators.add_proforma_locator)
    io_list_page.click_on_element(
        ProformaFormLocators.confirmation_yes_button_locator,
        locator_to_be_appeared=ProformaFormLocators.proforma_title_locator)
    proforma_form_page.click_on_save_and_generate_proforma_button(
        locator_to_be_appeared=ProformaFormLocators.success_message_locator)
    io_list_page.wait_for_visibility_of_element(
        ProformaFormLocators.success_message_locator)
    assert "Proforma saved and generated" in proforma_form_page.get_success_message()

    # DATA VERIFICATION
    proforma_list_page.click_on_element(
        ProformaFormLocators.back_to_list_locator, locator_to_be_appeared=ProformaListLocators.search_field_locator)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    proforma_list_page.wait_for_visibility_of_element(
        ProformaListLocators.first_grid_item_locator)
    io_id = IoUtils.pull_io_id("", connection=db_connection, io_title=io_edit_data['io_main_information']['io_title'])
    proforma_list_page.search_and_action(io_title=io_edit_data['io_main_information']['io_title'], io_id=str(io_id))
    io_list_page.wait_for_spinner_load()
    proforma_list_page.click_on_specific_proforma(
        io_edit_data['io_main_information']['io_title'])
    pulled_proforma_data_gui = proforma_form_page.get_proforma_information_from_gui(
        proforma_data)
    print(generic_modules.ordered(pulled_proforma_data_gui))
    print(generic_modules.ordered(proforma_data))
    assert generic_modules.ordered(pulled_proforma_data_gui) == generic_modules.ordered(proforma_data)
    proforma_url = driver.current_url

    # EDIT CREATED PROFORMA
    proforma_form_page.provide_proforma_data_and_save(proforma_edit_data,
                                                      edit_proforma=True)
    assert "Proforma saved and generated" in proforma_form_page.get_success_message()

    # DATA VERIFICATION AFTER PROFORMA EDIT
    driver.get(proforma_url)
    pulled_proforma_data_gui_after_edit = proforma_form_page.get_proforma_information_from_gui(
        proforma_edit_data)
    print(generic_modules.ordered(pulled_proforma_data_gui_after_edit))
    print(generic_modules.ordered(proforma_edit_data))
    assert generic_modules.ordered(pulled_proforma_data_gui_after_edit) == generic_modules.ordered(proforma_edit_data)

    # PROFORMA PAYMENT
    invoice_form_page.click_on_element(InvoiceFormLocators.buttons_group_locator)
    invoice_form_page.add_payment_into_invoice(payment_data)
    time.sleep(3)
    status = proforma_form_page.get_element_text(
        ProformaFormLocators.status_locator)
    assert str(status).strip() == "Paid"


@pytest.mark.dependency(
    depends=['test_regression_add_and_edit_io',
             'test_regression_add_and_edit_invoice',
             'test_regression_add_and_edit_proforma'])
def test_regression_delete_io_and_invoice(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    invoice_list_page = DspDashboardInvoiceList(driver)
    payments_log_page = DspDashboardPaymentsLog(driver)

    with open('assets/temp/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)

    with open('assets/temp/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)

    folder_path = 'assets/temp'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(
                    file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (
                file_path, e))

    if "JENKINS_URL" not in os.environ:
        # PAYMENT DELETE
        sidebar_navigation.navigate_to_page(PageNames.IO)
        io_list_page.click_on_element(
            IoListLocators.logs_dropdown_icon_data_qa)
        io_list_page.click_on_element(
            IoListLocators.payment_actions_data_qa)
        if io_list_page.is_element_present(
                PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(
                PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(
                PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()
        if io_list_page.is_element_present(
                PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(
                PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(
                PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()
        if io_list_page.is_element_present(
                PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(
                PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(
                PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()

        # INVOICE CLEAN UP
        sidebar_navigation.navigate_to_page(PageNames.INVOICE)
        invoice_list_page.wait_for_visibility_of_element(
            InvoiceListLocators.first_grid_item_locator)
        time.sleep(2)
        invoice_list_page.click_on_specific_invoice(
            invoice_edit_data['invoice_main_information'][
                'invoice_title'])
        io_list_page.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form_page.get_success_message()

        # IO CLEAN UP
        sidebar_navigation.navigate_to_page(PageNames.IO)
        io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(
            IoListLocators.first_grid_item_locator)
        io_list_page.search_by_title(
            io_edit_data['io_main_information']['io_title'])
        io_list_page.click_on_element(IoListLocators.edit_io_locator)
        io_list_page.click_on_specific_button(IoFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()
        assert "IO has been deleted!" in io_form_page.get_success_message()
    else:
        pass


def test_regression_invoice_creation_delete_and_io_download(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    download_dir = os.path.join(os.getcwd(), "downloads")

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info("[START] IO creation")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io_url = driver.current_url

    generic_modules.step_info("[END] IO creation")

    generic_modules.step_info(
        "[START - RTB-6949]  Validate whether the Download IO button is working properly")

    driver.get(io_url)
    current_date = io_form_page.get_current_date_with_specific_format(
        "%Y_%m_%d")
    file_name = "LT_IO_" + io_number + "_Test_Automation_Company_" + current_date + ".pdf"
    io_form_page.click_on_element(
        IoFormLocators.download_button_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.download_io_button_data_qa)
    io_form_page.wait_for_spinner_load()
    assert io_form_page.is_a_specific_file_available_into_a_folder(
        download_dir, file_name)

    generic_modules.step_info(
        "[END - RTB-6949]  Validate whether the Download IO button is working properly")

    generic_modules.step_info(
        "[START - RTB-6951]  Validate whether the Back button is working properly")
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator)
    assert True is io_list_page.is_element_present(
        IoListLocators.create_io_button_data_qa)
    generic_modules.step_info(
        "[END - RTB-6951]  Validate whether the Back button is working properly")

    generic_modules.step_info(
        "[START - RTB-6950]  Validate whether the Create invoice button is working properly")
    io_list_page.click_on_element(IoListLocators.create_io_button_data_qa)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)
    assert True is io_form_page.is_element_present(
        InvoiceFormLocators.invoice_page_title_locator)
    generic_modules.step_info(
        "[END - RTB-6950]  Validate whether the Create invoice button is working properly")
