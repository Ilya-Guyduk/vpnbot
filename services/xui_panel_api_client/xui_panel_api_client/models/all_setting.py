from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AllSetting")


@_attrs_define
class AllSetting:
    """AllSetting contains all configuration settings for the 3x-ui panel including web server, Telegram bot, and
    subscription settings.

        Attributes:
            datepicker (str): Date picker format
            expire_diff (int): Expiration warning threshold in days
            external_traffic_inform_enable (bool): Enable external traffic reporting
            external_traffic_inform_uri (str): URI for external traffic reporting
            ldap_auto_create (bool):
            ldap_auto_delete (bool):
            ldap_base_dn (str):
            ldap_bind_dn (str):
            ldap_default_expiry_days (int):
            ldap_default_limit_ip (int):
            ldap_default_total_gb (int):
            ldap_enable (bool): LDAP settings
            ldap_flag_field (str): Generic flag configuration
            ldap_host (str):
            ldap_inbound_tags (str):
            ldap_invert_flag (bool):
            ldap_password (str):
            ldap_port (int):
            ldap_sync_cron (str):
            ldap_truthy_values (str):
            ldap_use_tls (bool):
            ldap_user_attr (str): e.g., mail or uid
            ldap_user_filter (str):
            ldap_vless_field (str):
            page_size (int): UI settings
                Number of items per page in lists (0 disables pagination)
            panel_outbound (str): Xray outbound tag for the panel's own outbound HTTP (update checks/downloads, Telegram,
                geo updates, outbound-subscription fetches)
            remark_template (str): Subscription remark template ({{VAR}} tokens) rendered per client
            restart_xray_on_client_disable (bool): Restart Xray when clients are auto-disabled by expiry/traffic limit
            session_max_age (int): Session maximum age in minutes (cap at one year)
            smtp_cpu (int): CPU threshold for email notifications
            smtp_enable (bool): Email (SMTP) notification settings
                Enable email notifications
            smtp_enabled_events (str): Comma-separated event types to send via email
            smtp_encryption_type (str): SMTP encryption: none, starttls, tls
            smtp_host (str): SMTP server host
            smtp_memory (int): Memory threshold for email notifications
            smtp_password (str): SMTP password
            smtp_port (int): SMTP server port
            smtp_to (str): Comma-separated recipient emails
            smtp_username (str): SMTP username
            sub_announce (str): Subscription announce
            sub_cert_file (str): SSL certificate file for subscription server
            sub_clash_enable (bool): Enable Clash/Mihomo subscription endpoint
            sub_clash_enable_routing (bool): Enable global routing rules for Clash/Mihomo
            sub_clash_path (str): Path for Clash/Mihomo subscription endpoint
            sub_clash_rules (str): Clash/Mihomo global routing rules
            sub_clash_uri (str): Clash/Mihomo subscription server URI
            sub_domain (str): Domain for subscription server validation
            sub_enable (bool): Subscription server settings
                Enable subscription server
            sub_enable_routing (bool): Enable routing for subscription
            sub_encrypt (bool): Encrypt subscription responses
            sub_hide_settings (bool): Hide server settings in happ subscription (Only for Happ)
            sub_incy_enable_routing (bool): Enable routing injection for the Incy client
            sub_incy_routing_rules (str): Incy routing deep-link injected into the subscription body (Only for Incy)
            sub_json_enable (bool): Enable JSON subscription endpoint
            sub_json_final_mask (str): JSON subscription global finalmask (tcp/udp masks + quicParams)
            sub_json_mux (str): JSON subscription mux configuration
            sub_json_path (str): Path for JSON subscription endpoint
            sub_json_rules (str):
            sub_json_uri (str): JSON subscription server URI
            sub_key_file (str): SSL private key file for subscription server
            sub_listen (str): Subscription server listen IP
            sub_path (str): Base path for subscription URLs
            sub_port (int): Subscription server port
            sub_profile_url (str): Subscription profile URL
            sub_routing_rules (str): Subscription global routing rules (Only for Happ)
            sub_support_url (str): Subscription support URL
            sub_theme_dir (str): Absolute path to a folder containing a custom subscription page template
            sub_title (str): Subscription title
            sub_uri (str): Subscription server URI
            sub_updates (int): Subscription update interval in minutes
            tg_bot_api_server (str): Custom API server for Telegram bot
            tg_bot_backup (bool): Enable database backup via Telegram
            tg_bot_chat_id (str): Telegram chat ID for notifications
            tg_bot_enable (bool): Telegram bot settings
                Enable Telegram bot notifications
            tg_bot_proxy (str): Proxy URL for Telegram bot
            tg_bot_token (str): Telegram bot token
            tg_cpu (int): CPU usage threshold for alerts (percent)
            tg_enabled_events (str): Comma-separated event types to send via Telegram
            tg_lang (str): Telegram bot language
            tg_memory (int): Memory usage threshold for alerts (percent)
            tg_run_time (str): Cron schedule for Telegram notifications
            time_location (str): Security settings
                Time zone location
            traffic_diff (int): Traffic warning threshold percentage
            trusted_proxy_cid_rs (str): Trusted reverse proxy IPs/CIDRs for forwarded headers
            two_factor_enable (bool): Enable two-factor authentication
            two_factor_token (str): Two-factor authentication token
            warp_update_interval (int): WARP
            web_base_path (str): Base path for web panel URLs
            web_cert_file (str): Path to SSL certificate file for web server
            web_domain (str): Web server domain for domain validation
            web_key_file (str): Path to SSL private key file for web server
            web_listen (str): Web server settings
                Web server listen IP address
            web_port (int): Web server port number
    """

    datepicker: str
    expire_diff: int
    external_traffic_inform_enable: bool
    external_traffic_inform_uri: str
    ldap_auto_create: bool
    ldap_auto_delete: bool
    ldap_base_dn: str
    ldap_bind_dn: str
    ldap_default_expiry_days: int
    ldap_default_limit_ip: int
    ldap_default_total_gb: int
    ldap_enable: bool
    ldap_flag_field: str
    ldap_host: str
    ldap_inbound_tags: str
    ldap_invert_flag: bool
    ldap_password: str
    ldap_port: int
    ldap_sync_cron: str
    ldap_truthy_values: str
    ldap_use_tls: bool
    ldap_user_attr: str
    ldap_user_filter: str
    ldap_vless_field: str
    page_size: int
    panel_outbound: str
    remark_template: str
    restart_xray_on_client_disable: bool
    session_max_age: int
    smtp_cpu: int
    smtp_enable: bool
    smtp_enabled_events: str
    smtp_encryption_type: str
    smtp_host: str
    smtp_memory: int
    smtp_password: str
    smtp_port: int
    smtp_to: str
    smtp_username: str
    sub_announce: str
    sub_cert_file: str
    sub_clash_enable: bool
    sub_clash_enable_routing: bool
    sub_clash_path: str
    sub_clash_rules: str
    sub_clash_uri: str
    sub_domain: str
    sub_enable: bool
    sub_enable_routing: bool
    sub_encrypt: bool
    sub_hide_settings: bool
    sub_incy_enable_routing: bool
    sub_incy_routing_rules: str
    sub_json_enable: bool
    sub_json_final_mask: str
    sub_json_mux: str
    sub_json_path: str
    sub_json_rules: str
    sub_json_uri: str
    sub_key_file: str
    sub_listen: str
    sub_path: str
    sub_port: int
    sub_profile_url: str
    sub_routing_rules: str
    sub_support_url: str
    sub_theme_dir: str
    sub_title: str
    sub_uri: str
    sub_updates: int
    tg_bot_api_server: str
    tg_bot_backup: bool
    tg_bot_chat_id: str
    tg_bot_enable: bool
    tg_bot_proxy: str
    tg_bot_token: str
    tg_cpu: int
    tg_enabled_events: str
    tg_lang: str
    tg_memory: int
    tg_run_time: str
    time_location: str
    traffic_diff: int
    trusted_proxy_cid_rs: str
    two_factor_enable: bool
    two_factor_token: str
    warp_update_interval: int
    web_base_path: str
    web_cert_file: str
    web_domain: str
    web_key_file: str
    web_listen: str
    web_port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        datepicker = self.datepicker

        expire_diff = self.expire_diff

        external_traffic_inform_enable = self.external_traffic_inform_enable

        external_traffic_inform_uri = self.external_traffic_inform_uri

        ldap_auto_create = self.ldap_auto_create

        ldap_auto_delete = self.ldap_auto_delete

        ldap_base_dn = self.ldap_base_dn

        ldap_bind_dn = self.ldap_bind_dn

        ldap_default_expiry_days = self.ldap_default_expiry_days

        ldap_default_limit_ip = self.ldap_default_limit_ip

        ldap_default_total_gb = self.ldap_default_total_gb

        ldap_enable = self.ldap_enable

        ldap_flag_field = self.ldap_flag_field

        ldap_host = self.ldap_host

        ldap_inbound_tags = self.ldap_inbound_tags

        ldap_invert_flag = self.ldap_invert_flag

        ldap_password = self.ldap_password

        ldap_port = self.ldap_port

        ldap_sync_cron = self.ldap_sync_cron

        ldap_truthy_values = self.ldap_truthy_values

        ldap_use_tls = self.ldap_use_tls

        ldap_user_attr = self.ldap_user_attr

        ldap_user_filter = self.ldap_user_filter

        ldap_vless_field = self.ldap_vless_field

        page_size = self.page_size

        panel_outbound = self.panel_outbound

        remark_template = self.remark_template

        restart_xray_on_client_disable = self.restart_xray_on_client_disable

        session_max_age = self.session_max_age

        smtp_cpu = self.smtp_cpu

        smtp_enable = self.smtp_enable

        smtp_enabled_events = self.smtp_enabled_events

        smtp_encryption_type = self.smtp_encryption_type

        smtp_host = self.smtp_host

        smtp_memory = self.smtp_memory

        smtp_password = self.smtp_password

        smtp_port = self.smtp_port

        smtp_to = self.smtp_to

        smtp_username = self.smtp_username

        sub_announce = self.sub_announce

        sub_cert_file = self.sub_cert_file

        sub_clash_enable = self.sub_clash_enable

        sub_clash_enable_routing = self.sub_clash_enable_routing

        sub_clash_path = self.sub_clash_path

        sub_clash_rules = self.sub_clash_rules

        sub_clash_uri = self.sub_clash_uri

        sub_domain = self.sub_domain

        sub_enable = self.sub_enable

        sub_enable_routing = self.sub_enable_routing

        sub_encrypt = self.sub_encrypt

        sub_hide_settings = self.sub_hide_settings

        sub_incy_enable_routing = self.sub_incy_enable_routing

        sub_incy_routing_rules = self.sub_incy_routing_rules

        sub_json_enable = self.sub_json_enable

        sub_json_final_mask = self.sub_json_final_mask

        sub_json_mux = self.sub_json_mux

        sub_json_path = self.sub_json_path

        sub_json_rules = self.sub_json_rules

        sub_json_uri = self.sub_json_uri

        sub_key_file = self.sub_key_file

        sub_listen = self.sub_listen

        sub_path = self.sub_path

        sub_port = self.sub_port

        sub_profile_url = self.sub_profile_url

        sub_routing_rules = self.sub_routing_rules

        sub_support_url = self.sub_support_url

        sub_theme_dir = self.sub_theme_dir

        sub_title = self.sub_title

        sub_uri = self.sub_uri

        sub_updates = self.sub_updates

        tg_bot_api_server = self.tg_bot_api_server

        tg_bot_backup = self.tg_bot_backup

        tg_bot_chat_id = self.tg_bot_chat_id

        tg_bot_enable = self.tg_bot_enable

        tg_bot_proxy = self.tg_bot_proxy

        tg_bot_token = self.tg_bot_token

        tg_cpu = self.tg_cpu

        tg_enabled_events = self.tg_enabled_events

        tg_lang = self.tg_lang

        tg_memory = self.tg_memory

        tg_run_time = self.tg_run_time

        time_location = self.time_location

        traffic_diff = self.traffic_diff

        trusted_proxy_cid_rs = self.trusted_proxy_cid_rs

        two_factor_enable = self.two_factor_enable

        two_factor_token = self.two_factor_token

        warp_update_interval = self.warp_update_interval

        web_base_path = self.web_base_path

        web_cert_file = self.web_cert_file

        web_domain = self.web_domain

        web_key_file = self.web_key_file

        web_listen = self.web_listen

        web_port = self.web_port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datepicker": datepicker,
                "expireDiff": expire_diff,
                "externalTrafficInformEnable": external_traffic_inform_enable,
                "externalTrafficInformURI": external_traffic_inform_uri,
                "ldapAutoCreate": ldap_auto_create,
                "ldapAutoDelete": ldap_auto_delete,
                "ldapBaseDN": ldap_base_dn,
                "ldapBindDN": ldap_bind_dn,
                "ldapDefaultExpiryDays": ldap_default_expiry_days,
                "ldapDefaultLimitIP": ldap_default_limit_ip,
                "ldapDefaultTotalGB": ldap_default_total_gb,
                "ldapEnable": ldap_enable,
                "ldapFlagField": ldap_flag_field,
                "ldapHost": ldap_host,
                "ldapInboundTags": ldap_inbound_tags,
                "ldapInvertFlag": ldap_invert_flag,
                "ldapPassword": ldap_password,
                "ldapPort": ldap_port,
                "ldapSyncCron": ldap_sync_cron,
                "ldapTruthyValues": ldap_truthy_values,
                "ldapUseTLS": ldap_use_tls,
                "ldapUserAttr": ldap_user_attr,
                "ldapUserFilter": ldap_user_filter,
                "ldapVlessField": ldap_vless_field,
                "pageSize": page_size,
                "panelOutbound": panel_outbound,
                "remarkTemplate": remark_template,
                "restartXrayOnClientDisable": restart_xray_on_client_disable,
                "sessionMaxAge": session_max_age,
                "smtpCpu": smtp_cpu,
                "smtpEnable": smtp_enable,
                "smtpEnabledEvents": smtp_enabled_events,
                "smtpEncryptionType": smtp_encryption_type,
                "smtpHost": smtp_host,
                "smtpMemory": smtp_memory,
                "smtpPassword": smtp_password,
                "smtpPort": smtp_port,
                "smtpTo": smtp_to,
                "smtpUsername": smtp_username,
                "subAnnounce": sub_announce,
                "subCertFile": sub_cert_file,
                "subClashEnable": sub_clash_enable,
                "subClashEnableRouting": sub_clash_enable_routing,
                "subClashPath": sub_clash_path,
                "subClashRules": sub_clash_rules,
                "subClashURI": sub_clash_uri,
                "subDomain": sub_domain,
                "subEnable": sub_enable,
                "subEnableRouting": sub_enable_routing,
                "subEncrypt": sub_encrypt,
                "subHideSettings": sub_hide_settings,
                "subIncyEnableRouting": sub_incy_enable_routing,
                "subIncyRoutingRules": sub_incy_routing_rules,
                "subJsonEnable": sub_json_enable,
                "subJsonFinalMask": sub_json_final_mask,
                "subJsonMux": sub_json_mux,
                "subJsonPath": sub_json_path,
                "subJsonRules": sub_json_rules,
                "subJsonURI": sub_json_uri,
                "subKeyFile": sub_key_file,
                "subListen": sub_listen,
                "subPath": sub_path,
                "subPort": sub_port,
                "subProfileUrl": sub_profile_url,
                "subRoutingRules": sub_routing_rules,
                "subSupportUrl": sub_support_url,
                "subThemeDir": sub_theme_dir,
                "subTitle": sub_title,
                "subURI": sub_uri,
                "subUpdates": sub_updates,
                "tgBotAPIServer": tg_bot_api_server,
                "tgBotBackup": tg_bot_backup,
                "tgBotChatId": tg_bot_chat_id,
                "tgBotEnable": tg_bot_enable,
                "tgBotProxy": tg_bot_proxy,
                "tgBotToken": tg_bot_token,
                "tgCpu": tg_cpu,
                "tgEnabledEvents": tg_enabled_events,
                "tgLang": tg_lang,
                "tgMemory": tg_memory,
                "tgRunTime": tg_run_time,
                "timeLocation": time_location,
                "trafficDiff": traffic_diff,
                "trustedProxyCIDRs": trusted_proxy_cid_rs,
                "twoFactorEnable": two_factor_enable,
                "twoFactorToken": two_factor_token,
                "warpUpdateInterval": warp_update_interval,
                "webBasePath": web_base_path,
                "webCertFile": web_cert_file,
                "webDomain": web_domain,
                "webKeyFile": web_key_file,
                "webListen": web_listen,
                "webPort": web_port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        datepicker = d.pop("datepicker")

        expire_diff = d.pop("expireDiff")

        external_traffic_inform_enable = d.pop("externalTrafficInformEnable")

        external_traffic_inform_uri = d.pop("externalTrafficInformURI")

        ldap_auto_create = d.pop("ldapAutoCreate")

        ldap_auto_delete = d.pop("ldapAutoDelete")

        ldap_base_dn = d.pop("ldapBaseDN")

        ldap_bind_dn = d.pop("ldapBindDN")

        ldap_default_expiry_days = d.pop("ldapDefaultExpiryDays")

        ldap_default_limit_ip = d.pop("ldapDefaultLimitIP")

        ldap_default_total_gb = d.pop("ldapDefaultTotalGB")

        ldap_enable = d.pop("ldapEnable")

        ldap_flag_field = d.pop("ldapFlagField")

        ldap_host = d.pop("ldapHost")

        ldap_inbound_tags = d.pop("ldapInboundTags")

        ldap_invert_flag = d.pop("ldapInvertFlag")

        ldap_password = d.pop("ldapPassword")

        ldap_port = d.pop("ldapPort")

        ldap_sync_cron = d.pop("ldapSyncCron")

        ldap_truthy_values = d.pop("ldapTruthyValues")

        ldap_use_tls = d.pop("ldapUseTLS")

        ldap_user_attr = d.pop("ldapUserAttr")

        ldap_user_filter = d.pop("ldapUserFilter")

        ldap_vless_field = d.pop("ldapVlessField")

        page_size = d.pop("pageSize")

        panel_outbound = d.pop("panelOutbound")

        remark_template = d.pop("remarkTemplate")

        restart_xray_on_client_disable = d.pop("restartXrayOnClientDisable")

        session_max_age = d.pop("sessionMaxAge")

        smtp_cpu = d.pop("smtpCpu")

        smtp_enable = d.pop("smtpEnable")

        smtp_enabled_events = d.pop("smtpEnabledEvents")

        smtp_encryption_type = d.pop("smtpEncryptionType")

        smtp_host = d.pop("smtpHost")

        smtp_memory = d.pop("smtpMemory")

        smtp_password = d.pop("smtpPassword")

        smtp_port = d.pop("smtpPort")

        smtp_to = d.pop("smtpTo")

        smtp_username = d.pop("smtpUsername")

        sub_announce = d.pop("subAnnounce")

        sub_cert_file = d.pop("subCertFile")

        sub_clash_enable = d.pop("subClashEnable")

        sub_clash_enable_routing = d.pop("subClashEnableRouting")

        sub_clash_path = d.pop("subClashPath")

        sub_clash_rules = d.pop("subClashRules")

        sub_clash_uri = d.pop("subClashURI")

        sub_domain = d.pop("subDomain")

        sub_enable = d.pop("subEnable")

        sub_enable_routing = d.pop("subEnableRouting")

        sub_encrypt = d.pop("subEncrypt")

        sub_hide_settings = d.pop("subHideSettings")

        sub_incy_enable_routing = d.pop("subIncyEnableRouting")

        sub_incy_routing_rules = d.pop("subIncyRoutingRules")

        sub_json_enable = d.pop("subJsonEnable")

        sub_json_final_mask = d.pop("subJsonFinalMask")

        sub_json_mux = d.pop("subJsonMux")

        sub_json_path = d.pop("subJsonPath")

        sub_json_rules = d.pop("subJsonRules")

        sub_json_uri = d.pop("subJsonURI")

        sub_key_file = d.pop("subKeyFile")

        sub_listen = d.pop("subListen")

        sub_path = d.pop("subPath")

        sub_port = d.pop("subPort")

        sub_profile_url = d.pop("subProfileUrl")

        sub_routing_rules = d.pop("subRoutingRules")

        sub_support_url = d.pop("subSupportUrl")

        sub_theme_dir = d.pop("subThemeDir")

        sub_title = d.pop("subTitle")

        sub_uri = d.pop("subURI")

        sub_updates = d.pop("subUpdates")

        tg_bot_api_server = d.pop("tgBotAPIServer")

        tg_bot_backup = d.pop("tgBotBackup")

        tg_bot_chat_id = d.pop("tgBotChatId")

        tg_bot_enable = d.pop("tgBotEnable")

        tg_bot_proxy = d.pop("tgBotProxy")

        tg_bot_token = d.pop("tgBotToken")

        tg_cpu = d.pop("tgCpu")

        tg_enabled_events = d.pop("tgEnabledEvents")

        tg_lang = d.pop("tgLang")

        tg_memory = d.pop("tgMemory")

        tg_run_time = d.pop("tgRunTime")

        time_location = d.pop("timeLocation")

        traffic_diff = d.pop("trafficDiff")

        trusted_proxy_cid_rs = d.pop("trustedProxyCIDRs")

        two_factor_enable = d.pop("twoFactorEnable")

        two_factor_token = d.pop("twoFactorToken")

        warp_update_interval = d.pop("warpUpdateInterval")

        web_base_path = d.pop("webBasePath")

        web_cert_file = d.pop("webCertFile")

        web_domain = d.pop("webDomain")

        web_key_file = d.pop("webKeyFile")

        web_listen = d.pop("webListen")

        web_port = d.pop("webPort")

        all_setting = cls(
            datepicker=datepicker,
            expire_diff=expire_diff,
            external_traffic_inform_enable=external_traffic_inform_enable,
            external_traffic_inform_uri=external_traffic_inform_uri,
            ldap_auto_create=ldap_auto_create,
            ldap_auto_delete=ldap_auto_delete,
            ldap_base_dn=ldap_base_dn,
            ldap_bind_dn=ldap_bind_dn,
            ldap_default_expiry_days=ldap_default_expiry_days,
            ldap_default_limit_ip=ldap_default_limit_ip,
            ldap_default_total_gb=ldap_default_total_gb,
            ldap_enable=ldap_enable,
            ldap_flag_field=ldap_flag_field,
            ldap_host=ldap_host,
            ldap_inbound_tags=ldap_inbound_tags,
            ldap_invert_flag=ldap_invert_flag,
            ldap_password=ldap_password,
            ldap_port=ldap_port,
            ldap_sync_cron=ldap_sync_cron,
            ldap_truthy_values=ldap_truthy_values,
            ldap_use_tls=ldap_use_tls,
            ldap_user_attr=ldap_user_attr,
            ldap_user_filter=ldap_user_filter,
            ldap_vless_field=ldap_vless_field,
            page_size=page_size,
            panel_outbound=panel_outbound,
            remark_template=remark_template,
            restart_xray_on_client_disable=restart_xray_on_client_disable,
            session_max_age=session_max_age,
            smtp_cpu=smtp_cpu,
            smtp_enable=smtp_enable,
            smtp_enabled_events=smtp_enabled_events,
            smtp_encryption_type=smtp_encryption_type,
            smtp_host=smtp_host,
            smtp_memory=smtp_memory,
            smtp_password=smtp_password,
            smtp_port=smtp_port,
            smtp_to=smtp_to,
            smtp_username=smtp_username,
            sub_announce=sub_announce,
            sub_cert_file=sub_cert_file,
            sub_clash_enable=sub_clash_enable,
            sub_clash_enable_routing=sub_clash_enable_routing,
            sub_clash_path=sub_clash_path,
            sub_clash_rules=sub_clash_rules,
            sub_clash_uri=sub_clash_uri,
            sub_domain=sub_domain,
            sub_enable=sub_enable,
            sub_enable_routing=sub_enable_routing,
            sub_encrypt=sub_encrypt,
            sub_hide_settings=sub_hide_settings,
            sub_incy_enable_routing=sub_incy_enable_routing,
            sub_incy_routing_rules=sub_incy_routing_rules,
            sub_json_enable=sub_json_enable,
            sub_json_final_mask=sub_json_final_mask,
            sub_json_mux=sub_json_mux,
            sub_json_path=sub_json_path,
            sub_json_rules=sub_json_rules,
            sub_json_uri=sub_json_uri,
            sub_key_file=sub_key_file,
            sub_listen=sub_listen,
            sub_path=sub_path,
            sub_port=sub_port,
            sub_profile_url=sub_profile_url,
            sub_routing_rules=sub_routing_rules,
            sub_support_url=sub_support_url,
            sub_theme_dir=sub_theme_dir,
            sub_title=sub_title,
            sub_uri=sub_uri,
            sub_updates=sub_updates,
            tg_bot_api_server=tg_bot_api_server,
            tg_bot_backup=tg_bot_backup,
            tg_bot_chat_id=tg_bot_chat_id,
            tg_bot_enable=tg_bot_enable,
            tg_bot_proxy=tg_bot_proxy,
            tg_bot_token=tg_bot_token,
            tg_cpu=tg_cpu,
            tg_enabled_events=tg_enabled_events,
            tg_lang=tg_lang,
            tg_memory=tg_memory,
            tg_run_time=tg_run_time,
            time_location=time_location,
            traffic_diff=traffic_diff,
            trusted_proxy_cid_rs=trusted_proxy_cid_rs,
            two_factor_enable=two_factor_enable,
            two_factor_token=two_factor_token,
            warp_update_interval=warp_update_interval,
            web_base_path=web_base_path,
            web_cert_file=web_cert_file,
            web_domain=web_domain,
            web_key_file=web_key_file,
            web_listen=web_listen,
            web_port=web_port,
        )

        all_setting.additional_properties = d
        return all_setting

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
