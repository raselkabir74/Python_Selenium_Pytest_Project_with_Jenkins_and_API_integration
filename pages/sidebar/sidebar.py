from locators.sidebar.sidebar_locators import SidebarLocators
from pages.base_page import BasePage
from utils.page_names_enum import PageNames, PageCategories


class DashboardSidebarPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    @staticmethod
    def get_category(page_name: PageNames):
        for category in PageCategories:
            if page_name in category.value:
                return category
        return None

    def navigate_to_page(self, page_name: PageNames):
        category = self.get_category(page_name)
        if category == PageCategories.ADOPS_TOOLS:
            self.click_on_sidebar_menu(SidebarLocators.adops_tools_menu_data_qa)
            if page_name == PageNames.BRANDING:
                self.click_on_sidebar_menu(SidebarLocators.branding_data_qa)
            elif page_name == PageNames.CAMPAIGNS_EMAILS:
                self.click_on_sidebar_menu(SidebarLocators.campaigns_emails_data_qa)
            elif page_name == PageNames.CLIENTS_COMPANIES:
                self.click_on_sidebar_menu(SidebarLocators.clients_companies_data_qa)
            elif page_name == PageNames.GLOBAL_AUDIENCES:
                self.click_on_sidebar_menu(SidebarLocators.global_audiences_data_qa)
            elif page_name == PageNames.GLOBAL_PACKAGES:
                self.click_on_sidebar_menu(SidebarLocators.global_packages_data_qa)
        elif category == PageCategories.ADMIN_TOOLS:
            self.click_on_sidebar_menu(SidebarLocators.admin_tools_menu_data_qa)
            if page_name == PageNames.AD_EXCHANGES:
                self.click_on_sidebar_menu(SidebarLocators.ad_exchanges_data_qa)
            elif page_name == PageNames.BIDDER_SETTINGS:
                self.click_on_sidebar_menu(SidebarLocators.bidder_settings_data_qa)
            elif page_name == PageNames.BLACKLISTS:
                self.click_on_sidebar_menu(SidebarLocators.blacklist_data_qa)
            elif page_name == PageNames.COLLECTION_TARGET:
                self.click_on_sidebar_menu(SidebarLocators.collection_target_data_qa)
            elif page_name == PageNames.COMPANIES_GROUPS:
                self.click_on_sidebar_menu(SidebarLocators.companies_groups_data_qa)
            elif page_name == PageNames.COUNTRY_SETTINGS:
                self.click_on_sidebar_menu(SidebarLocators.country_settings_data_qa)
            elif page_name == PageNames.DEVICES:
                self.click_on_sidebar_menu(SidebarLocators.devices_data_qa)
            elif page_name == PageNames.DEVICES_MISSING:
                self.click_on_sidebar_menu(SidebarLocators.devices_missing_data_qa)
            elif page_name == PageNames.DMP_PROFILES:
                self.click_on_sidebar_menu(SidebarLocators.dmp_profiles_data_qa)
            elif page_name == PageNames.ESKIMI_BILLING_ENTITIES:
                self.click_on_sidebar_menu(SidebarLocators.eskimi_billing_entities_data_qa)
            elif page_name == PageNames.OPERATORS:
                self.click_on_sidebar_menu(SidebarLocators.operators_data_qa)
            elif page_name == PageNames.PAYMENT_SETTINGS:
                self.click_on_sidebar_menu(SidebarLocators.payment_settings_data_qa)
            elif page_name == PageNames.PLATFORMS_STATS:
                self.click_on_sidebar_menu(SidebarLocators.platforms_stats_data_qa)
            elif page_name == PageNames.PREDICTIVE:
                self.click_on_sidebar_menu(SidebarLocators.predictive_data_qa)
            elif page_name == PageNames.SCREENSHOTS:
                self.click_on_sidebar_menu(SidebarLocators.screenshots_data_qa)
            elif page_name == PageNames.SIDEBAR_LAYOUTS:
                self.click_on_sidebar_menu(SidebarLocators.sidebar_layouts_data_qa)
            elif page_name == PageNames.SITES_CATEGORIES:
                self.click_on_sidebar_menu(SidebarLocators.sites_categories_data_qa)
            elif page_name == PageNames.SITES_DOMAIN_BLACKLIST:
                self.click_on_sidebar_menu(SidebarLocators.sites_domain_blacklist_data_qa)
            elif page_name == PageNames.SITES_SUBDOMAIN_MAP:
                self.click_on_sidebar_menu(SidebarLocators.sites_subdomain_map_data_qa)
            elif page_name == PageNames.USERS:
                self.click_on_sidebar_menu(SidebarLocators.users_data_qa)
        elif category == PageCategories.TOOLS:
            is_expand = self.get_attribute_value(
                SidebarLocators.sidebar_menu_locator.format(SidebarLocators.tool_menu_data_qa), "aria-expanded",
                locator_initialization=True)
            if is_expand == 'false':
                self.click_on_sidebar_menu(SidebarLocators.tool_menu_data_qa)
            if page_name == PageNames.ALL_CAMPAIGNS:
                self.click_on_sidebar_menu(SidebarLocators.all_campaign_data_qa)
            elif page_name == PageNames.AUDIENCES:
                self.click_on_sidebar_menu(SidebarLocators.audiences_data_qa)
            elif page_name == PageNames.KEYWORDS:
                self.click_on_sidebar_menu(SidebarLocators.keywords_data_qa)
            elif page_name == PageNames.CHANGELOG:
                self.click_on_sidebar_menu(SidebarLocators.changelog_data_qa)
            elif page_name == PageNames.ADVANCED_CHANGELOG:
                self.click_on_sidebar_menu(SidebarLocators.advanced_changelog_data_qa)
            elif page_name == PageNames.OPTIMISATION:
                self.click_on_sidebar_menu(SidebarLocators.optimisation_data_qa)
            elif page_name == PageNames.PARTNER_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.partner_report_data_qa)
            elif page_name == PageNames.PACKAGES:
                self.click_on_sidebar_menu(SidebarLocators.packages_data_qa)
            elif page_name == PageNames.PRIVATE_MARKETPLACE:
                self.click_on_sidebar_menu(SidebarLocators.private_marketplace_data_qa)
            elif page_name == PageNames.TRAFFIC_DISCOVERY:
                self.click_on_sidebar_menu(SidebarLocators.traffic_discovery_data_qa)
        elif category == PageCategories.CAMPAIGNS:
            is_expand = self.get_attribute_value(
                SidebarLocators.sidebar_menu_locator.format(SidebarLocators.campaigns_menu_data_qa), "aria-expanded",
                locator_initialization=True)
            if is_expand == 'false':
                self.click_on_sidebar_menu(SidebarLocators.campaigns_menu_data_qa)
            if page_name == PageNames.CAMPAIGNS_LIST:
                self.click_on_element(SidebarLocators.campaigns_list_locator, locator_initialization=True)
            elif page_name == PageNames.CAMPAIGN_SETTINGS:
                self.click_on_element(SidebarLocators.campaign_settings_data_qa)
        elif category == PageCategories.SETTINGS:
            self.click_on_sidebar_menu(SidebarLocators.settings_menu_data_qa)
            if page_name == PageNames.PROFILE_INFO:
                self.click_on_element(SidebarLocators.profile_info_data_qa)
            elif page_name == PageNames.SETTINGS_BILLING:
                self.click_on_element(SidebarLocators.settings_billing_locator)
        elif category == PageCategories.BILLING:
            is_expand = self.get_attribute_value(SidebarLocators.billing_menu_locator, "aria-expanded")
            if is_expand == 'false':
                self.click_on_sidebar_menu(SidebarLocators.billing_menu_data_qa)
            if page_name == PageNames.CLIENTS:
                self.click_on_sidebar_menu(SidebarLocators.clients_data_qa)
            elif page_name == PageNames.COLLECTION_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.collection_report_data_qa)
            elif page_name == PageNames.CURRENCIES:
                self.click_on_sidebar_menu(SidebarLocators.currencies_data_qa)
            elif page_name == PageNames.FACTORING_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.factoring_report_data_qa)
            elif page_name == PageNames.FINANCE_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.finance_report_data_qa)
            elif page_name == PageNames.INCOME_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.income_report_data_qa)
            elif page_name == PageNames.INVOICE:
                self.click_on_sidebar_menu(SidebarLocators.invoice_data_qa)
            elif page_name == PageNames.INVOICE_TRACKER:
                self.click_on_sidebar_menu(SidebarLocators.invoice_tracker_data_qa)
            elif page_name == PageNames.IO:
                self.click_on_sidebar_menu(SidebarLocators.io_data_qa)
            elif page_name == PageNames.PROFORMA:
                self.click_on_sidebar_menu(SidebarLocators.proforma_data_qa)
            elif page_name == PageNames.BILLING_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.billing_report_data_qa)
            elif page_name == PageNames.REBATE_OVERVIEW:
                self.click_on_sidebar_menu(SidebarLocators.rebate_overview_data_qa)
            elif page_name == PageNames.SOA_REPORT:
                self.click_on_sidebar_menu(SidebarLocators.soa_report_data_qa)
        elif page_name == PageNames.OVERVIEW:
            self.click_on_sidebar_menu(SidebarLocators.overview_menu_data_qa)
        elif page_name == PageNames.CREATIVE_SETS:
            self.click_on_sidebar_menu(SidebarLocators.creative_sets_menu_data_qa)
        elif page_name == PageNames.REPORTS:
            self.click_on_sidebar_menu(SidebarLocators.reports_menu_data_qa)
        elif page_name == PageNames.TELCODASH:
            self.click_on_sidebar_menu(SidebarLocators.telcodash_menu_data_qa)
        else:
            raise ValueError(f"No navigation action defined for page: {page_name}")
