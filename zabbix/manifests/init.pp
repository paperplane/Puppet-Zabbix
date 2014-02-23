class zabbix::init {
    user{"zabbix":
        ensure => present,
        comment => "Zabbix User",
        gid => "zabbix",
        require => Group["zabbix"],
    }

    group{"zabbix":
        ensure => present,
    }

    package{"zabbix":
        ensure => installed,
        require => User["zabbix"],
    }
}

class zabbix::server{
    include zabbix::server::install,zabbix::server::config,zabbix::server::service
    include zabbix::files::server,zabbix::params::server
}

class zabbix::agentd{
    include zabbix::agentd::install,zabbix::agentd::config,zabbix::agentd::service
    include zabbix::files::agentd,zabbix::params::agentd,zabbix::params::userdefine 
}

class zabbix{
    include zabbix::init
    include zabbix::server
    include zabbix::agentd
    include zabbix::utils
}
