class zabbix::agentd::install {
    package{"zabbix-agent":
        ensure => latest,
        require => Class["zabbix::init"],
    }
}

class zabbix::agentd::config inherits zabbix::params::agentd {
    file{"/usr/local/zabbix/etc/zabbix_agentd.conf":
        ensure => present,
        notify => Class["zabbix::agentd::service"],
        require => Class["zabbix::agentd::install"],
        content => template("zabbix/zabbix_agentd.conf.erb"),
    }
}

class zabbix::agentd::userdefine inherits zabbix::params::userdefine {
    file{"/usr/local/zabbix/etc/zabbix_agentd.userparams.conf":
        ensure => present,
        notify => Class["zabbix::agentd::service"],
        require => Class["zabbix::agentd::install"],
        content => template("zabbix/zabbix_agentd.userparams.conf.erb"),
    }
}

class zabbix::agentd::service {
    service{"zabbix-agentd":
        ensure => running,
        hasstatus => true,
        hasrestart => true,
        require => Class["zabbix::files::server"],
    }
}
