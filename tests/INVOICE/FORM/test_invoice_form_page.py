import json
import copy
import time

from configurations import generic_modules
from pages.io.io_form import DspDashboardIoForm
from pages.io.invoice_form import DspDashboardInvoiceForm
from locators.io.io_form_locator import IoFormLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from utils.user import UserUtils
from selenium.webdriver import Keys


def test_finance_invoice_form_page(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info(
        "[START - RTB-7685] Validate whether the users are able to generate Invoice "
        "after IO is created")
    generic_modules.step_info(
        "[START - RTB-7686] Verify that the relevant fields are automatically filled after "
        "IO is created with mandatory fields filled")
    generic_modules.step_info(
        "[START - RTB-7690] Validate that Invoice has the proper insertion order number "
        "based on created IO")
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    # INVOICE CREATION
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)
    insertion_order_number = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.div_tag, invoice_form_page.id_attribute,
        InvoiceFormLocators.io_number_id)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()
    assert io_number in insertion_order_number in invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.div_tag, invoice_form_page.id_attribute,
        InvoiceFormLocators.io_number_id)

    # DATA VERIFICATION
    pulled_io_data_gui_from_invoice = copy.deepcopy(io_data)
    pulled_io_data_gui_from_invoice['io_main_information']['io_title'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.invoice_title_label)
    pulled_io_data_gui_from_invoice['client_profile'][
        'client'] = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.span_tag, invoice_form_page.id_attribute,
        InvoiceFormLocators.select2_client_container_id)
    pulled_io_data_gui_from_invoice['client_profile'][
        'email'] = invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.email_label)
    pulled_io_data_gui_from_invoice['client_profile']['contact'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.contact_label)
    pulled_io_data_gui_from_invoice['client_profile']['client_company'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_company_id_container_id)
    pulled_io_data_gui_from_invoice['billing_entity']['company_profile'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_company_profile_container_id)
    pulled_io_data_gui_from_invoice['billing_entity']['sales_manager'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_sales_manager_container_id)
    assert io_data == pulled_io_data_gui_from_invoice
    generic_modules.step_info(
        "[END - RTB-7685] Validate whether the users are able to generate Invoice "
        "after IO is created")
    generic_modules.step_info(
        "[END - RTB-7686] Verify that the relevant fields are automatically filled after "
        "IO is created with mandatory fields filled")
    generic_modules.step_info(
        "[END - RTB-7690] Validate that Invoice has the proper insertion order number "
        "based on created IO")

    generic_modules.step_info("[START - RTB-7694] Validate Payment details section is generated with proper data")
    vat = float(invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.vat_label))
    discount = "{:.2f}".format(float(invoice_form_page.get_text_using_tag_attribute(invoice_form_page.input_tag,
                                                                                    invoice_form_page.name_attribute,
                                                                                    InvoiceFormLocators.discount_name)))
    payment_term_days = invoice_form_page.get_value_from_specific_input_field(
        InvoiceFormLocators.payment_term_days_label)
    assert vat == UserUtils.get_user_vat_from_db(
        db_connection,
        company_profile=pulled_io_data_gui_from_invoice['billing_entity']['company_profile'])
    assert discount == str(UserUtils.get_user_discount_from_db(db_connection, user_id=7722))
    assert payment_term_days == UserUtils.get_payment_term_from_db(
        pulled_io_data_gui_from_invoice['client_profile']['client'],
        db_connection)
    generic_modules.step_info("[END - RTB-7694] Validate Payment details section is generated with proper data")


def test_finance_invoice_form_page_two(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info("[START - RTB-7688] Verify that the relevant fields are automatically filled after IO "
                              "is created with all fields filled")
    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)
    second_io = "Glo GH Data December campaign (IO 4453)"
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_data_and_save(io_data)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)

    # INVOICE CREATION
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)
    if io_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        io_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                           'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    pulled_io_data_gui_from_invoice = copy.deepcopy(io_data)
    pulled_io_data_gui_from_invoice['io_main_information']['io_title'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.invoice_title_label)
    pulled_io_data_gui_from_invoice['client_profile'][
        'client'] = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.span_tag, invoice_form_page.id_attribute,
        InvoiceFormLocators.select2_client_container_id)
    pulled_io_data_gui_from_invoice['client_profile'][
        'email'] = invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.email_label)
    pulled_io_data_gui_from_invoice['client_profile']['contact'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.contact_label)
    pulled_io_data_gui_from_invoice['client_profile']['client_company'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_company_id_container_id)
    pulled_io_data_gui_from_invoice['billing_entity']['company_profile'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_company_profile_container_id)
    pulled_io_data_gui_from_invoice['billing_entity']['sales_manager'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_sales_manager_container_id)
    pulled_io_data_gui_from_invoice['io_object'][
        'campaign'] = invoice_form_page.get_selected_value_of_modal_from_field(select_tag_id_or_class="",
                                                                               field_label_or_data_qa=InvoiceFormLocators.campaign_label)
    pulled_io_data_gui_from_invoice['io_object']['media_budget'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.input_tag,
            invoice_form_page.class_attribute,
            InvoiceFormLocators.form_control_media_budget_class)
    pulled_io_data_gui_from_invoice['io_object'][
        'channel_service'] = invoice_form_page.get_element_text(
        InvoiceFormLocators.channel_dropdown_locator)
    pulled_io_data_gui_from_invoice['io_object'][
        'country'] = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.td_tag, invoice_form_page.class_attribute,
        InvoiceFormLocators.country_row_class)
    pulled_io_data_gui_from_invoice['io_object'][
        'campaign_type'] = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.td_tag, invoice_form_page.class_attribute,
        InvoiceFormLocators.campaign_type_class)
    pulled_io_data_gui_from_invoice['total_media_budget'][
        'io_execution_comment'] = \
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag,
            invoice_form_page.id_attribute,
            InvoiceFormLocators.select2_io_execution_comment_id_container_id)
    pulled_io_data_gui_from_invoice['total_media_budget']['notes'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.notes_label, is_textarea=True)
    pulled_io_data_gui_from_invoice['billing_information'][
        'currency'] = invoice_form_page.get_text_using_tag_attribute(
        invoice_form_page.span_tag, invoice_form_page.id_attribute,
        InvoiceFormLocators.select2_currency_container_id)
    pulled_io_data_gui_from_invoice['billing_information']['vat'] = \
        "{:.1f}".format(float(invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.vat_label)))
    pulled_io_data_gui_from_invoice['billing_information'][
        'discount'] = "{:.2f}".format(float(
        invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.input_tag,
            invoice_form_page.name_attribute,
            InvoiceFormLocators.discount_name)))
    pulled_io_data_gui_from_invoice['billing_information'][
        'payment_term_days'] = \
        invoice_form_page.get_value_from_specific_input_field(InvoiceFormLocators.payment_term_days_label)
    if 'http://rtb.local/admin' in driver.current_url:
        del io_data['client_profile']['email']
        del pulled_io_data_gui_from_invoice['client_profile']['email']
    assert io_data == pulled_io_data_gui_from_invoice
    generic_modules.step_info(
        "[END - RTB-7688] Verify that the relevant fields are automatically filled after IO "
        "is created with all fields filled")

    if 'http://rtb.local/admin' not in driver.current_url:
        generic_modules.step_info("[START - RTB-7689] Validate that there is the media budget for each selected IO")
        
        invoice_form_page.select_from_modal(second_io, InvoiceFormLocators.select_io_label, click_uncheck_all=False)
        time.sleep(1)
        media_budget_io_number = invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.span_tag, invoice_form_page.class_attribute,
            InvoiceFormLocators.media_budget_io_number_class)
        second_media_budget_io_number = invoice_form_page.get_element_text(
            InvoiceFormLocators.media_budget_io_number_locator)
        assert media_budget_io_number in io_number
        assert second_media_budget_io_number in second_io
        generic_modules.step_info("[END - RTB-7689] Validate that there is the media budget for each selected IO")

        generic_modules.step_info("[START - RTB-7789] Validate whether the users are able to select multiple IO's")
        first_io = io_data['io_main_information']['io_title']
        ios_list = [f'{first_io} ({"IO " + io_number})', second_io]
        ios_from_gui = invoice_form_page.get_selected_multiple_items_from_modal(InvoiceFormLocators.select_io_label)
        assert ios_list == ios_from_gui
        generic_modules.step_info("[END - RTB-7789] Validate whether the users are able to select multiple IO's")

        generic_modules.step_info("[START - RTB-7691] Validate the media budget is populating with proper information")
        generic_modules.step_info("[START - RTB-7693] Validate whether the Total media budget amount is showing proper "
                                  "data based on the added media budget")
        first_io_media_budget_from_table = float(invoice_form_page.get_text_from_specific_media_budget_table(
            InvoiceFormLocators.tr_serial1_id, InvoiceFormLocators.total_currency_class).replace(',', ''))
        second_io_media_budget_from_table = float(invoice_form_page.get_text_from_specific_media_budget_table(
            InvoiceFormLocators.tr_serial2_id, InvoiceFormLocators.total_currency_class).replace(',', ''))
        if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
            invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                    'Client requested invoice early')
        invoice_form_page.click_on_save_and_generate_invoice_button(
            locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
        io_media_budget_amount_from_table = first_io_media_budget_from_table + second_io_media_budget_from_table
        total_media_budget_amount = float(invoice_form_page.get_text_using_tag_attribute(
            invoice_form_page.div_tag, invoice_form_page.class_attribute,
            InvoiceFormLocators.first_total_media_budget_class))
        media_budget = float(io_data['io_object']['media_budget'])
        assert media_budget == first_io_media_budget_from_table
        assert total_media_budget_amount == io_media_budget_amount_from_table
        generic_modules.step_info("[END - RTB-7691] Validate the media budget is populating with proper information")
        generic_modules.step_info("[END - RTB-7693] Validate whether the Total media budget amount is showing proper "
                                  "data based on the added media budget")

        generic_modules.step_info("[START - RTB-7786] Validate whether Totals & payments table is showing proper data")
        discount_percentage = float(io_data['billing_information']['discount'])
        discount = (total_media_budget_amount * discount_percentage) / 100
        formatted_discount = "₦" + "{:,.2f}".format(discount)
        vat = round(((total_media_budget_amount - discount) * float(io_data['billing_information']['vat']) / 100), 2)
        formatted_vat = "₦" + "{:,.2f}".format(vat)
        total_amount = total_media_budget_amount - discount + vat
        formatted_total_amount = "₦" + "{:,.2f}".format(total_amount)
        formatted_total_media_budget_amount = "₦" + "{:,.2f}".format(total_media_budget_amount)

        assert formatted_total_media_budget_amount == \
               invoice_form_page.get_payment_table_specific_row_and_column_data(1, "Base amount", 1)
        assert formatted_discount == invoice_form_page.get_payment_table_specific_row_and_column_data(1, "Discount", 1)
        assert formatted_vat == invoice_form_page.get_payment_table_specific_row_and_column_data(1, "VAT", 1)
        assert formatted_total_amount == \
               invoice_form_page.get_payment_table_specific_row_and_column_data(1, "Total amount", 1)
        generic_modules.step_info("[END - RTB-7786] Validate whether Totals & payments table is showing proper data")

        generic_modules.step_info("[START - RTB-7791] Verify Comment Field Generation upon Selecting "
                                  "'Other: Comment' in IO-Campaign Execution Comment Dropdown")
        comment = "Testing comment"
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label, "Other: Comment")
        invoice_form_page.wait_for_presence_of_element(InvoiceFormLocators.comment_input_data_qa).send_keys(comment)
        if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
            invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                    'Client requested invoice early')
        invoice_form_page.click_on_save_and_generate_invoice_button(
            locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
        assert comment == invoice_form_page.get_element_text(InvoiceFormLocators.comment_input_data_qa)
        generic_modules.step_info("[END - RTB-7791] Verify Comment Field Generation upon Selecting "
                                  "'Other: Comment' in IO-Campaign Execution Comment Dropdown")

        generic_modules.step_info("[START - RTB-7792] Validate the users are able to change currency")
        currency = "Euro Member Countries (EUR)"
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.currency_label, currency)
        invoice_form_page.wait_alert_is_present()
        invoice_form_page.accept_alert()
        invoice_form_page.click_on_element(InvoiceFormLocators.yes_button_locator, locator_initialization=True)
        time.sleep(invoice_form_page.TWO_SEC_DELAY)
        assert currency == invoice_form_page.get_text_using_tag_attribute(invoice_form_page.span_tag,
                                                                          invoice_form_page.id_attribute,
                                                                          InvoiceFormLocators.select2_currency_container_id)
        generic_modules.step_info("[END - RTB-7792] Validate the users are able to change currency")


def test_finance_invoice_form_page_edit(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info("[START - RTB-7790] Validate whether the users are able to add multiple media budget")
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    # INVOICE CREATION
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)

    test_data = {'media_budget': '100.00', 'channel': 'DSP display',
                 'country': 'Afghanistan',
                 'campaign_type': 'CPC', 'clicks': '111',
                 'media_rate': "{:.2f}".format((100 / 111))}

    invoice_form_page.click_on_element(
        InvoiceFormLocators.media_budget_plus_button_locator,
        locator_to_be_appeared=IoFormLocators.second_period_field_data_qa)
    invoice_form_page.click_on_element(
        InvoiceFormLocators.media_budget_arrow_xpath.format("2"),
        locator_initialization=True)
    invoice_form_page.set_text_using_tag_attribute(invoice_form_page.input_tag,
                                                   invoice_form_page.class_attribute,
                                                   InvoiceFormLocators.form_control_media_budget_class,
                                                   test_data['media_budget'], index=2)
    invoice_form_page.click_on_element(InvoiceFormLocators.channel_second_dropdown_locator)
    invoice_form_page.set_value_into_element(
        InvoiceFormLocators.channel_text_field_locator,
        test_data['channel'] + Keys.ENTER)
    invoice_form_page.select_dropdown_value(InvoiceFormLocators.country_label, test_data['country'], index=2)
    invoice_form_page.select_dropdown_value(InvoiceFormLocators.campaign_type_label, test_data['campaign_type'],
                                            index=2)
    invoice_form_page.set_value_into_specific_input_field(InvoiceFormLocators.clicks_label, test_data['clicks'],
                                                          tab_out=True)
    test_data_from_gui = copy.deepcopy(test_data)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    test_data_from_gui[
        'media_budget'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id,
        InvoiceFormLocators.total_currency_class, 1)
    test_data_from_gui[
        'channel'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id, InvoiceFormLocators.channel_class, 1)
    test_data_from_gui[
        'country'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id, InvoiceFormLocators.country_row_class,
        1)
    test_data_from_gui[
        'campaign_type'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id,
        InvoiceFormLocators.campaign_type_class, 1)
    test_data_from_gui[
        'clicks'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id, InvoiceFormLocators.impressions_class,
        1)
    test_data_from_gui[
        'media_rate'] = invoice_form_page.get_text_from_specific_media_budget_table(
        InvoiceFormLocators.tr_serial2_id, InvoiceFormLocators.cpm_rate_class, 1)
    assert test_data_from_gui == test_data
    generic_modules.step_info("[END - RTB-7790] Validate whether the users are able to add multiple media budget")

    generic_modules.step_info("[START - RTB-7793] Validate whether the users are able to select multiple Campaigns")
    campaigns_list = ["TTT (110454)", "Test Campaign (115974)"]
    invoice_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=InvoiceFormLocators.campaign_label, option_list_to_select=campaigns_list)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    assert campaigns_list == invoice_form_page.get_selected_multiple_items_from_modal(
        InvoiceFormLocators.campaign_label)
    generic_modules.step_info("[END - RTB-7793] Validate whether the users are able to select multiple Campaigns")

    generic_modules.step_info("[START - RTB-7859] Validate whether the users are able to remove media budget")
    invoice_form_page.click_on_element(InvoiceFormLocators.media_budget_remove_button_xpath.format("2"),
                                       locator_initialization=True)
    assert False is invoice_form_page.is_element_present(
        InvoiceFormLocators.second_media_budget_table_locator, time_out=1)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    assert False is invoice_form_page.is_element_present(
        InvoiceFormLocators.second_media_budget_table_locator, time_out=1)
    generic_modules.step_info("[END - RTB-7859] Validate whether the users are able to remove media budget")

    generic_modules.step_info("[START - RTB-7876] Validate whether the Created/updated by & created/updated date "
                              "information are showing properly")
    created_by_info = invoice_form_page.get_element_text(
        InvoiceFormLocators.created_by_info_locator)
    created_by = created_by_info.split(":")
    assert "AutomationAdminUser" == created_by[1].strip()

    last_updated_by_info = invoice_form_page.get_element_text(
        InvoiceFormLocators.last_updated_by_info_locator)
    last_updated_by = last_updated_by_info.split(":")
    assert "AutomationAdminUser" == last_updated_by[1].strip()

    created_info = invoice_form_page.get_element_text(
        InvoiceFormLocators.created_info_locator)
    created = created_info.split(" ")
    current_date = invoice_form_page.get_current_date_with_specific_format(
        "%Y-%m-%d")
    assert current_date == created[1].strip()
    assert "(GMT+3)" == created[3].strip()

    last_updated_info = invoice_form_page.get_element_text(
        InvoiceFormLocators.last_updated_info_locator)
    last_updated = last_updated_info.split(" ")
    assert current_date == last_updated[2].strip()
    assert "(GMT+3)" == last_updated[4].strip()
    generic_modules.step_info("[END - RTB-7876] Validate whether the Created/updated by & created/updated date "
                              "information are showing properly")
