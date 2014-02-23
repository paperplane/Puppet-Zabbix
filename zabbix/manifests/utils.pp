class zabbix::utils{
    package{['zabbix-get','zabbix-sender']:
        ensure => "2.2.0-2",
        require => Class['zabbix::init']
    }
}
