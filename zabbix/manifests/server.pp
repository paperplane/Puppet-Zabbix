class zabbix::server::install {
    package{"zabbix-server":
        ensure => "2.2.0-2",
        require => Class["zabbix::init"],
    }
}

class zabbix::server::config inherits zabbix::params::server {
    file{"/usr/local/zabbix/etc/zabbix_server.conf":
        ensure => present,
        notify => Class["zabbix::server::service"],
        require => Class["zabbix::server::install"],
        content => template("zabbix/zabbix_server.conf.erb"),
    }
}

class zabbix::server::service {
    service{"zabbix-server":
        ensure => running,
        hasstatus => true,
        hasrestart => true,
        require => Class["zabbix::files::server"],
    }
}
