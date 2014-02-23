class zabbix::files{
    File{
        ensure => present,
        owner => root,
        group => root,
        mode => 0755,
    }
}
class zabbix::files::server inherits zabbix::files{
    file{"/etc/init.d/zabbix-server":
        source => "puppet:///ZabbixFile/zabbix-server",
    }
}

class zabbix::files::agentd inherits zabbix::files{
    file{"/etc/init.d/zabbix-agentd":
        source => "puppet:///ZabbixFile/zabbix-agentd",
    }
}
