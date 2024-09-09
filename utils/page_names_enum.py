from enum import Enum


class PageNames(Enum):
    OVERVIEW = "Overview"
    CREATIVE_SETS = "Creative sets"
    CAMPAIGNS_LIST = "Campaigns list"
    CAMPAIGN_SETTINGS = "Campaign settings"
    REPORTS = "Reports"
    TELCODASH = "Telcodash"
    ALL_CAMPAIGNS = "All campaigns"
    AUDIENCES = "Audiences"
    KEYWORDS = "Keywords"
    CHANGELOG = "Changelog"
    ADVANCED_CHANGELOG = "Advanced changelog"
    OPTIMISATION = "Optimisation"
    PARTNER_REPORT = "Partner report"
    PACKAGES = "Packages"
    PRIVATE_MARKETPLACE = "Private marketplace"
    TRAFFIC_DISCOVERY = "Traffic discovery"
    BRANDING = "Branding"
    CAMPAIGNS_EMAILS = "Campaigns emails"
    CLIENTS_COMPANIES = "Clients companies"
    GLOBAL_AUDIENCES = "Global audiences"
    GLOBAL_PACKAGES = "Global packages"
    AD_EXCHANGES = "Ad exchanges"
    BIDDER_SETTINGS = "Bidder settings"
    BLACKLISTS = "Blacklists"
    COLLECTION_TARGET = "Collection target"
    COMPANIES_GROUPS = "Companies groups"
    COUNTRY_SETTINGS = "Country settings"
    DEVICES = "Devices"
    DEVICES_MISSING = "Devices missing"
    DMP_PROFILES = "DMP profiles"
    ESKIMI_BILLING_ENTITIES = "Eskimi billing entities"
    OPERATORS = "Operators"
    PAYMENT_SETTINGS = "Payment settings"
    PLATFORMS_STATS = "Platforms stats"
    PREDICTIVE = "Predictive"
    SCREENSHOTS = "Screenshots"
    SIDEBAR_LAYOUTS = "Sidebar layouts"
    SITES_CATEGORIES = "Sites categories"
    SITES_DOMAIN_BLACKLIST = "Sites domain blacklist"
    SITES_SUBDOMAIN_MAP = "Sites subdomain map"
    USERS = "Users"
    BUDGET = "Budget"
    CLIENTS = "Clients"
    COLLECTION_REPORT = "Collection report"
    CURRENCIES = "Currencies"
    FACTORING_REPORT = "Factoring report"
    FINANCE_REPORT = "Finance report"
    INCOME_REPORT = "Income report"
    INVOICE = "Invoice"
    INVOICE_TRACKER = "Invoice tracker"
    IO = "IO"
    PROFORMA = "Proforma"
    BILLING_REPORT = "Billing report"
    REBATE_OVERVIEW = "Rebate overview"
    SOA_REPORT = "SOA report"
    PROFILE_INFO = "Profile info"
    SETTINGS_BILLING = "Settings Billing"


class PageCategories(Enum):
    ADOPS_TOOLS = {
        PageNames.BRANDING,
        PageNames.CAMPAIGNS_EMAILS,
        PageNames.CLIENTS_COMPANIES,
        PageNames.GLOBAL_AUDIENCES,
        PageNames.GLOBAL_PACKAGES
    }
    ADMIN_TOOLS = {
        PageNames.AD_EXCHANGES,
        PageNames.BIDDER_SETTINGS,
        PageNames.BLACKLISTS,
        PageNames.COLLECTION_TARGET,
        PageNames.COMPANIES_GROUPS,
        PageNames.COUNTRY_SETTINGS,
        PageNames.DEVICES,
        PageNames.DEVICES_MISSING,
        PageNames.DMP_PROFILES,
        PageNames.ESKIMI_BILLING_ENTITIES,
        PageNames.OPERATORS,
        PageNames.PAYMENT_SETTINGS,
        PageNames.PLATFORMS_STATS,
        PageNames.PREDICTIVE,
        PageNames.SCREENSHOTS,
        PageNames.SIDEBAR_LAYOUTS,
        PageNames.SITES_CATEGORIES,
        PageNames.SITES_DOMAIN_BLACKLIST,
        PageNames.SITES_SUBDOMAIN_MAP,
        PageNames.USERS
    }
    TOOLS = {
        PageNames.ALL_CAMPAIGNS,
        PageNames.AUDIENCES,
        PageNames.KEYWORDS,
        PageNames.CHANGELOG,
        PageNames.ADVANCED_CHANGELOG,
        PageNames.OPTIMISATION,
        PageNames.PARTNER_REPORT,
        PageNames.PACKAGES,
        PageNames.PRIVATE_MARKETPLACE,
        PageNames.TRAFFIC_DISCOVERY
    }
    CAMPAIGNS = {
        PageNames.CAMPAIGNS_LIST,
        PageNames.CAMPAIGN_SETTINGS
    }
    SETTINGS = {
        PageNames.PROFILE_INFO,
        PageNames.SETTINGS_BILLING
    }
    BILLING = {
        PageNames.CLIENTS,
        PageNames.COLLECTION_REPORT,
        PageNames.CURRENCIES,
        PageNames.FACTORING_REPORT,
        PageNames.FINANCE_REPORT,
        PageNames.INCOME_REPORT,
        PageNames.INVOICE,
        PageNames.INVOICE_TRACKER,
        PageNames.IO,
        PageNames.PROFORMA,
        PageNames.BILLING_REPORT,
        PageNames.REBATE_OVERVIEW,
        PageNames.SOA_REPORT
    }
