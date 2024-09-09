from selenium.webdriver.common.by import By


class SidebarLocators:
    # [Start] data-qa attribute values
    overview_menu_data_qa = 'Overview'
    creative_sets_menu_data_qa = 'Creative sets'
    campaigns_menu_data_qa = 'Campaigns'
    campaign_settings_data_qa = 'Campaign settings'
    reports_menu_data_qa = 'Reports'
    telcodash_menu_data_qa = 'Telcodash'
    tool_menu_data_qa = 'Tools'
    all_campaign_data_qa = 'All campaigns'
    audiences_data_qa = 'Audiences'
    keywords_data_qa = 'Keywords'
    changelog_data_qa = 'Changelog'
    advanced_changelog_data_qa = "Advanced changelog"
    optimisation_data_qa = 'Optimisation'
    partner_report_data_qa = "Partner report"
    packages_data_qa = 'Packages'
    private_marketplace_data_qa = 'Private marketplace'
    traffic_discovery_data_qa = 'Traffic discovery'
    adops_tools_menu_data_qa = 'AdOps tools'
    branding_data_qa = 'Branding'
    campaigns_emails_data_qa = 'Campaigns emails'
    clients_companies_data_qa = 'Clients companies'
    global_audiences_data_qa = 'Global audiences'
    global_packages_data_qa = 'Global packages'
    admin_tools_menu_data_qa = 'Admin tools'
    ad_exchanges_data_qa = "Ad exchanges"
    bidder_settings_data_qa = "Bidder settings"
    blacklist_data_qa = "Blacklists"
    collection_target_data_qa = "Collection target"
    companies_groups_data_qa = "Companies groups"
    country_settings_data_qa = 'Country settings'
    devices_data_qa = "Devices"
    devices_missing_data_qa = "Devices missing"
    dmp_profiles_data_qa = "DMP profiles"
    eskimi_billing_entities_data_qa = 'Eskimi billing entities'
    operators_data_qa = "Operators"
    payment_settings_data_qa = "Payment settings"
    platforms_stats_data_qa = "Platforms stats"
    predictive_data_qa = "Predictive"
    screenshots_data_qa = "Screenshots"
    sidebar_layouts_data_qa = "Sidebar layouts"
    sites_categories_data_qa = "Sites categories"
    sites_domain_blacklist_data_qa = "Sites domain blacklist"
    sites_subdomain_map_data_qa = "Sites subdomain map"
    users_data_qa = 'Users'
    billing_menu_data_qa = 'Billing'
    budget_data_qa = 'Budget'
    clients_data_qa = 'Clients'
    collection_report_data_qa = 'Collection report'
    currencies_data_qa = 'Currencies'
    factoring_report_data_qa = "Factoring report"
    finance_report_data_qa = "Finance report"
    income_report_data_qa = "Income report"
    invoice_data_qa = 'Invoice'
    invoice_tracker_data_qa = "Invoice tracker"
    io_data_qa = 'IO'
    proforma_data_qa = 'Proforma'
    billing_report_data_qa = 'Billing'
    rebate_overview_data_qa = "Rebate overview"
    soa_report_data_qa = 'SOA report'
    settings_menu_data_qa = 'Settings'
    profile_info_data_qa = 'Profile Info'
    # [END] data-qa attribute values

    # [Start] Locators
    billing_menu_locator = (
        By.XPATH, "//span[text()='Billing']/../../../a")
    settings_billing_locator = (By.XPATH, "//i[@class='fas fa-money-bill-alt']/../span[contains(text(), 'Billing')]")
    campaigns_list_locator = "//ul[@class='sub-menu list-unstyled show']//dfn[@data-qa='Campaigns']"
    # [End] Locators

    # [Start] Attribute values
    sidebar_menu_locator = '//dfn[@data-qa="{}"]/..'
    # [End] Attribute values
