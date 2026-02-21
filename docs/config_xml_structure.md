# OPNsense Configuration XML Structure

This document describes the structure of an OPNsense configuration backup XML file (`config.xml`). The file represents the complete state of an OPNsense firewall and can be exported via the `core/backup/download` API endpoint.

## Root Element

```xml
<?xml version="1.0"?>
<opnsense>
  <!-- All configuration sections live here -->
</opnsense>
```

Every element that represents a collection entry uses a `uuid` attribute for unique identification:
```xml
<item uuid="396a3425-a209-466d-a002-28f106cccd6c">
```

Boolean values are stored as `"1"` (true) or `"0"` (false), or empty string (false/unset).

---

## Top-Level Sections

| Section | Description |
|---------|-------------|
| `<theme>` | UI theme name (e.g., `opnsense`) |
| `<sysctl>` | FreeBSD kernel tunables |
| `<system>` | Hostname, users, groups, webgui, SSH, firmware settings |
| `<interfaces>` | Legacy interface assignments (wan, lan, optN) |
| `<dhcpd>` | Legacy ISC DHCP server configuration |
| `<snmpd>` | SNMP daemon settings |
| `<filter>` | Legacy packet filter rules (pre-MVC) |
| `<nat>` | Legacy NAT rules (DNAT outbound) |
| `<rrd>` | Round-Robin Database statistics settings |
| `<ntpd>` | NTP daemon settings |
| `<revision>` | Config revision metadata (time, description, username) |
| `<OPNsense>` | **Main configuration hub** -- all MVC-based plugin/module configs |
| `<hasync>` | High-availability sync configuration |
| `<vlans>` | VLAN definitions |
| `<staticroutes>` | Static route definitions |
| `<bridges>` | Bridge interface definitions |
| `<gifs>` | GIF tunnel definitions |
| `<gres>` | GRE tunnel definitions |
| `<laggs>` | LAGG (link aggregation) definitions |
| `<ppps>` | PPP connection definitions |
| `<wireless>` | Wireless interface definitions |
| `<ca>` | Certificate Authority entries (repeating element) |
| `<cert>` | Certificate entries (repeating element) |
| `<dnsmasq>` | Dnsmasq DNS/DHCP forwarder settings |

---

## `<system>` -- System Configuration

```xml
<system>
  <optimization>normal</optimization>
  <hostname>firewall</hostname>
  <domain>example.lan</domain>
  <dnsallowoverride>1</dnsallowoverride>

  <group uuid="...">
    <gid>1999</gid>
    <name>admins</name>
    <description>System Administrators</description>
    <scope>system</scope>
    <priv>page-all</priv>
    <member>0</member>
  </group>

  <user uuid="...">
    <uid>0</uid>
    <name>root</name>
    <descr>System Administrator</descr>
    <scope>system</scope>
    <password>$2y$...</password>          <!-- bcrypt hash -->
    <apikeys>
      <item>
        <key>base64-encoded-api-key</key>
        <secret>base64-encoded-api-secret</secret>
      </item>
    </apikeys>
    <shell>/usr/local/sbin/opnsense-shell</shell>
    <authorizedkeys/>                     <!-- SSH public keys, base64 -->
  </user>

  <nextuid>2000</nextuid>
  <nextgid>2000</nextgid>
  <timezone>Etc/UTC</timezone>
  <timeservers>0.opnsense.pool.ntp.org 1.opnsense.pool.ntp.org</timeservers>

  <webgui>
    <protocol>HTTPS</protocol>
    <port>443</port>
    <ssl-certref>ref-id-of-cert</ssl-certref>
    <compression/>
  </webgui>

  <ssh>
    <enabled>enabled</enabled>
    <group>admins</group>
    <noauto>1</noauto>
    <interfaces/>                         <!-- empty = all interfaces -->
  </ssh>

  <firmware>
    <plugins>os-acme-client,os-haproxy</plugins>
    <mirror/>
    <flavour/>
  </firmware>

  <language>en_US</language>
  <dns1addr/>                             <!-- manual DNS server 1 -->
  <dns2addr/>                             <!-- manual DNS server 2 -->
  <serialspeed>115200</serialspeed>
  <primaryconsole>video</primaryconsole>
</system>
```

---

## `<sysctl>` -- Kernel Tunables

```xml
<sysctl version="1.0.2" description="System Tunables">
  <item uuid="...">
    <tunable>net.inet.ip.portrange.first</tunable>
    <value/>                              <!-- empty = system default -->
    <descr>Set the ephemeral port range to be lower.</descr>
  </item>
  <!-- Common tunables:
    vfs.read_max, net.inet.tcp.blackhole, net.inet.udp.blackhole,
    net.inet.ip.random_id, net.inet.ip.sourceroute,
    net.inet.icmp.log_redirect, net.inet.tcp.drop_synfin,
    net.inet6.ip6.redirect, net.inet.tcp.syncookies,
    net.inet.tcp.recvspace, net.inet.tcp.sendspace,
    net.inet.tcp.delayed_ack, net.inet.udp.maxdgram,
    net.link.bridge.pfil_onlyip, net.link.bridge.pfil_member,
    net.link.tap.user_open, kern.randompid,
    hw.syscons.kbd_reboot, net.inet.tcp.tso,
    net.inet.udp.checksum, kern.ipc.maxsockbuf,
    vm.pmap.pti, hw.ibrs_disable,
    security.bsd.see_other_gids, security.bsd.see_other_uids
  -->
</sysctl>
```

---

## `<interfaces>` -- Interface Assignments

Each child element name is the interface identifier (`wan`, `lan`, `lo0`, `opt1`..`optN`).

```xml
<interfaces>
  <lo0>
    <internal_dynamic>1</internal_dynamic>
    <descr>Loopback</descr>
    <enable>1</enable>
    <if>lo0</if>                          <!-- OS device name -->
    <ipaddr>127.0.0.1</ipaddr>
    <ipaddrv6>::1</ipaddrv6>
    <subnet>8</subnet>
    <subnetv6>128</subnetv6>
    <type>none</type>
    <virtual>1</virtual>
  </lo0>

  <wan>
    <descr>WAN</descr>
    <enable>1</enable>
    <if>vmx0</if>
    <ipaddr>dhcp</ipaddr>                 <!-- "dhcp" | static IP -->
    <ipaddrv6>dhcp6</ipaddrv6>
    <subnet/>                             <!-- CIDR prefix length for static -->
    <blockbogons>1</blockbogons>
    <dhcphostname/>
    <spoofmac/>
  </wan>

  <lan>
    <descr>LAN</descr>
    <enable>1</enable>
    <if>vmx1</if>
    <ipaddr>192.168.1.1</ipaddr>
    <subnet>24</subnet>
    <ipaddrv6>track6</ipaddrv6>           <!-- track6 | static IPv6 | dhcp6 -->
    <track6-interface>wan</track6-interface>
    <track6-prefix-id>0</track6-prefix-id>
    <subnetv6>64</subnetv6>
  </lan>

  <opt1>
    <descr>VLAN10_Office</descr>
    <enable>1</enable>
    <if>vmx1_vlan10</if>                  <!-- VLAN sub-interface device name -->
    <ipaddr>10.10.10.1</ipaddr>
    <subnet>24</subnet>
  </opt1>
  <!-- opt2, opt3, ... optN for additional interfaces -->
</interfaces>
```

**`ipaddr` values**: `dhcp`, `pppoe`, `pptp`, `l2tp`, or a static IPv4 address.

**`ipaddrv6` values**: `dhcp6`, `track6`, `slaac`, `6to4`, `6rd`, or a static IPv6 address.

---

## `<vlans>` -- VLAN Definitions

```xml
<vlans version="1.0.0">
  <vlan uuid="...">
    <if>vmx1</if>                         <!-- parent interface device -->
    <tag>10</tag>                         <!-- VLAN ID: 1-4094 -->
    <pcp>0</pcp>                          <!-- Priority Code Point: 0-7 -->
    <proto>802.1q</proto>                 <!-- "802.1q" | "802.1ad" (QinQ) -->
    <descr>Office VLAN</descr>
    <vlanif>vmx1_vlan10</vlanif>          <!-- resulting device name -->
  </vlan>
</vlans>
```

---

## `<ca>` and `<cert>` -- Certificates

Certificate Authority and certificate entries are **repeating elements at the root level** (multiple `<ca>` and `<cert>` elements).

```xml
<ca uuid="...">
  <refid>65a1b2c3d4e5f</refid>           <!-- unique reference ID -->
  <descr>Internal CA</descr>
  <crt>base64-encoded-certificate</crt>
  <prv>base64-encoded-private-key</prv>
  <serial>3</serial>                      <!-- next serial number -->
</ca>

<cert uuid="...">
  <refid>65f1a2b3c4d5e</refid>
  <descr>Web Server Certificate</descr>
  <caref>65a1b2c3d4e5f</caref>           <!-- reference to signing CA -->
  <crt>base64-encoded-certificate</crt>
  <prv>base64-encoded-private-key</prv>
  <csr>base64-encoded-csr</csr>           <!-- optional CSR -->
</cert>
```

---

## `<staticroutes>` -- Static Routes

```xml
<staticroutes>
  <route uuid="...">
    <network>10.0.0.0/8</network>
    <gateway>GW_WAN</gateway>             <!-- gateway name reference -->
    <descr>Route to internal network</descr>
    <disabled>0</disabled>
  </route>
</staticroutes>
```

---

## `<nat>` -- Legacy NAT (DNAT / Outbound)

```xml
<nat>
  <outbound>
    <mode>automatic</mode>                <!-- "automatic" | "hybrid" | "advanced" | "disabled" -->
    <!-- <rule> elements for manual outbound NAT when mode is hybrid/advanced -->
  </outbound>

  <rule uuid="...">
    <!-- Legacy DNAT / port-forward rules (see OPNsense/Firewall/Filter for MVC version) -->
    <sequence>1</sequence>
    <disabled>0</disabled>
    <interface>wan</interface>
    <ipprotocol>inet</ipprotocol>
    <protocol>tcp</protocol>
    <source>
      <network>any</network>
      <port/>
      <not>0</not>
    </source>
    <destination>
      <network>wanip</network>
      <port>443</port>
      <not>0</not>
    </destination>
    <target>192.168.1.100</target>
    <local-port>443</local-port>
    <descr>HTTPS to webserver</descr>
    <natreflection/>                      <!-- "" (system default) | "purenat" | "disable" -->
    <pass/>                               <!-- "" (manual) | "rule" | "pass" -->
    <log>0</log>
    <tag/>
    <tagged/>
    <nosync>0</nosync>
    <nordr>0</nordr>
    <poolopts/>
    <category/>
    <associated-rule-id/>
    <created>
      <username>root@10.0.0.1</username>
      <time>1700000000.00</time>
      <description>/api/firewall/nat/...</description>
    </created>
    <updated>
      <username>root@10.0.0.1</username>
      <time>1700000000.00</time>
      <description>/api/firewall/nat/...</description>
    </updated>
  </rule>
</nat>
```

---

## `<OPNsense>` -- Main Configuration Hub

This is the primary section containing all MVC-based module configurations. Each child is a plugin or core module.

```xml
<OPNsense>
  <wireguard>...</wireguard>
  <IPsec>...</IPsec>
  <Swanctl>...</Swanctl>
  <OpenVPNExport>...</OpenVPNExport>
  <OpenVPN>...</OpenVPN>
  <captiveportal>...</captiveportal>
  <cron>...</cron>
  <DHCRelay>...</DHCRelay>
  <Firewall>...</Firewall>
  <Netflow>...</Netflow>
  <IDS>...</IDS>
  <Interfaces>...</Interfaces>
  <Kea>...</Kea>
  <monit>...</monit>
  <Gateways>...</Gateways>
  <Syslog>...</Syslog>
  <TrafficShaper>...</TrafficShaper>
  <trust>...</trust>
  <unboundplus>...</unboundplus>
  <AcmeClient>...</AcmeClient>
  <HAProxy>...</HAProxy>
  <Hostwatch>...</Hostwatch>
  <radvd>...</radvd>
</OPNsense>
```

---

## `<OPNsense><Firewall>` -- Firewall Configuration

### Aliases

```xml
<Firewall>
  <Alias version="1.0.1">
    <geoip>
      <url/>
    </geoip>
    <aliases>
      <alias uuid="...">
        <enabled>1</enabled>
        <name>my_servers</name>
        <type>host</type>
        <!-- type values:
          "host"         - Single hosts (IP addresses or hostnames)
          "network"      - Network ranges (CIDR notation)
          "port"         - Port numbers or ranges
          "url"          - URL containing IP list (fetched once)
          "urltable"     - URL table (fetched periodically)
          "urljson"      - URL with JSON content
          "geoip"        - GeoIP country-based
          "networkgroup" - Group of other aliases
          "mac"          - MAC addresses
          "asn"          - Autonomous System Numbers
          "dynipv6host"  - Dynamic IPv6 host
          "authgroup"    - Authentication group
          "internal"     - Internal alias
          "external"     - External (pfTable) alias
        -->
        <proto/>
        <!-- proto values (comma-separated for multi):
          "IPv4", "IPv6"
        -->
        <interface/>
        <counters>0</counters>
        <updatefreq/>                     <!-- update frequency in days (for URL types) -->
        <content>10.0.0.1
10.0.0.2
10.0.0.3</content>                       <!-- newline-separated values -->
        <password/>
        <username/>
        <authtype/>                       <!-- "Basic" | "Bearer" | "Header" -->
        <expire/>                         <!-- expiry in seconds -->
        <categories/>                     <!-- comma-separated category UUIDs -->
        <description>My server list</description>
      </alias>
    </aliases>
  </Alias>
```

### Categories

```xml
  <Category version="1.0.0">
    <categories>
      <category uuid="...">
        <name>Web Services</name>
        <auto>0</auto>
        <color/>                          <!-- CSS color or empty -->
      </category>
    </categories>
  </Category>
```

### Filter Rules (Firewall Rules)

```xml
  <Filter version="1.0.10">
    <rules>
      <rule uuid="...">
        <enabled>1</enabled>
        <statetype>keep</statetype>
        <!-- statetype values: "keep", "sloppy", "modulate", "synproxy", "none" -->
        <state-policy/>
        <!-- state-policy values: "if-bound", "floating" -->
        <sequence>1</sequence>            <!-- 1-999999, determines rule order -->
        <action>pass</action>
        <!-- action values: "pass", "block", "reject" -->
        <quick>1</quick>                  <!-- 1 = stop processing on match -->
        <interfacenot>0</interfacenot>    <!-- 1 = negate interface match -->
        <interface>lan,opt1</interface>    <!-- comma-separated interface IDs -->
        <direction>in</direction>
        <!-- direction values: "in", "out" -->
        <ipprotocol>inet</ipprotocol>
        <!-- ipprotocol values: "inet" (IPv4), "inet6" (IPv6), "inet46" (both) -->
        <protocol>TCP</protocol>
        <!-- protocol values: "any", "TCP", "UDP", "TCP/UDP", "ICMP", "IGMP",
             "GRE", "ESP", "AH", "CARP", "PFSYNC", "OSPF", or protocol number -->
        <icmptype/>
        <!-- icmptype values (comma-separated):
          "echoreq", "echorep", "unreach", "squench", "redir", "althost",
          "routeradv", "routersol", "timex", "paramprob", "timereq", "timerep",
          "inforeq", "inforep", "maskreq", "maskrep"
        -->
        <icmp6type/>
        <source_net>any</source_net>
        <!-- source_net/destination_net values:
          "any"            - Any address
          "wanip"          - WAN interface address
          "lanip"          - LAN interface address
          "lan"            - LAN network
          "(self)"         - This firewall
          "10.0.0.0/24"   - CIDR network
          "10.0.0.1"      - Single host
          "alias_name"     - Reference to alias by name
          Comma-separated for multiple values.
        -->
        <source_not>0</source_not>        <!-- 1 = negate source match -->
        <source_port/>                    <!-- port number, range (80-443), or alias -->
        <destination_net>any</destination_net>
        <destination_not>0</destination_not>
        <destination_port>80,443</destination_port>
        <gateway/>                        <!-- gateway name or empty for default -->
        <replyto/>                        <!-- reply-to interface -->
        <disablereplyto>0</disablereplyto>
        <log>0</log>
        <allowopts>0</allowopts>          <!-- allow IP options -->
        <nosync>0</nosync>               <!-- exclude from XMLRPC sync -->
        <nopfsync>0</nopfsync>           <!-- no pfsync -->
        <statetimeout/>                   <!-- state timeout in seconds (1-2147483647) -->
        <udp_first/>                      <!-- UDP first timeout -->
        <udp_multiple/>                   <!-- UDP multiple timeout -->
        <udp_single/>                     <!-- UDP single timeout -->
        <max_src_nodes/>                  <!-- max source nodes -->
        <max_src_states/>                 <!-- max states per source -->
        <max_src_conn/>                   <!-- max connections per source -->
        <max/>                            <!-- max states total -->
        <max_src_conn_rate/>              <!-- connections per second -->
        <max_src_conn_rates/>             <!-- rate period in seconds -->
        <overload/>                       <!-- alias name for overload table -->
        <adaptivestart/>                  <!-- adaptive scaling start -->
        <adaptiveend/>                    <!-- adaptive scaling end -->
        <prio/>
        <!-- prio values: "0"-"7" (VLAN PCP priority) -->
        <set-prio/>
        <set-prio-low/>
        <tag/>                            <!-- pf tag (alphanumeric, max 512) -->
        <tagged/>                         <!-- match pf tag -->
        <tcpflags1/>
        <!-- tcpflags values (comma-separated):
          "syn", "ack", "fin", "rst", "psh", "urg", "ece", "cwr"
        -->
        <tcpflags2/>
        <categories/>                     <!-- comma-separated category UUIDs -->
        <sched/>                          <!-- schedule reference -->
        <tos/>                            <!-- Type of Service -->
        <shaper1/>                        <!-- traffic shaper pipe -->
        <shaper2/>                        <!-- traffic shaper queue -->
        <description>Allow web traffic</description>
      </rule>
    </rules>
```

### Source NAT (SNAT) Rules

```xml
    <snatrules>
      <rule uuid="...">
        <enabled>1</enabled>
        <nonat>0</nonat>                  <!-- 1 = exclude from NAT (no-nat rule) -->
        <sequence>1</sequence>
        <interface>wan</interface>         <!-- single interface identifier -->
        <ipprotocol>inet</ipprotocol>
        <!-- ipprotocol values: "inet", "inet6" -->
        <protocol>any</protocol>
        <source_net>10.0.0.0/24</source_net>
        <source_not>0</source_not>
        <source_port/>
        <destination_net>any</destination_net>
        <destination_not>0</destination_not>
        <destination_port/>
        <target>wanip</target>
        <!-- target values: "wanip", "lanip", specific IP, alias name, interface address -->
        <target_port/>                    <!-- redirect target port -->
        <log>0</log>
        <categories/>
        <tagged/>
        <description>Outbound NAT for LAN</description>
      </rule>
    </snatrules>
```

### 1:1 NAT (Binat) Rules

```xml
    <onetoone>
      <rule uuid="...">
        <enabled>1</enabled>
        <log>0</log>
        <sequence>1</sequence>
        <interface>wan</interface>
        <type>binat</type>
        <!-- type values: "binat" (bidirectional), "nat" (unidirectional) -->
        <source_net>10.0.0.100</source_net>
        <source_not>0</source_not>
        <destination_net>any</destination_net>
        <destination_not>0</destination_not>
        <external>203.0.113.100</external> <!-- external (public) IP address -->
        <natreflection/>
        <!-- natreflection values: "" (system default), "enable", "disable" -->
        <categories/>
        <description>1:1 NAT for web server</description>
      </rule>
    </onetoone>
```

### NPT (Network Prefix Translation)

```xml
    <npt>
      <!-- IPv6 prefix translation rules -->
      <rule uuid="...">
        <enabled>1</enabled>
        <interface>wan</interface>
        <source_net>fd00::/48</source_net>
        <destination_net>2001:db8::/48</destination_net>
        <description>IPv6 prefix mapping</description>
      </rule>
    </npt>
  </Filter>
</Firewall>
```

---

## `<OPNsense><unboundplus>` -- Unbound DNS Resolver

```xml
<unboundplus version="1.0.8">
  <general>
    <enabled>1</enabled>
    <port>53</port>
    <stats>0</stats>
    <dnssec>0</dnssec>
    <dns64>0</dns64>
    <dns64prefix/>
    <noarecords>0</noarecords>
    <regdhcp>0</regdhcp>                  <!-- register DHCP leases in DNS -->
    <regdhcpdomain/>
    <regdhcpstatic>0</regdhcpstatic>
    <noreglladdr6>0</noreglladdr6>
    <noregrecords/>
    <txtsupport>0</txtsupport>
    <cacheflush>0</cacheflush>
    <safesearch/>
    <local_zone_type>transparent</local_zone_type>
    <!-- local_zone_type values:
      "transparent", "always_nxdomain", "always_refuse", "always_transparent",
      "deny", "inform", "inform_deny", "nodefault", "refuse", "static",
      "typetransparent"
    -->
    <enable_wpad/>
  </general>

  <advanced>
    <hideidentity>0</hideidentity>
    <hideversion>0</hideversion>
    <prefetch>0</prefetch>
    <prefetchkey>0</prefetchkey>
    <dnssecstripped>0</dnssecstripped>
    <aggressivensec>1</aggressivensec>
    <serveexpired>0</serveexpired>
    <serveexpiredreplyttl/>
    <serveexpiredttl/>
    <serveexpiredttlreset>0</serveexpiredttlreset>
    <serveexpiredclienttimeout/>
    <qnameminstrict>0</qnameminstrict>
    <extendedstatistics>0</extendedstatistics>
    <logqueries>0</logqueries>
    <logreplies>0</logreplies>
    <logtagqueryreply>0</logtagqueryreply>
    <logservfail>0</logservfail>
    <loglocalactions>0</loglocalactions>
    <logverbosity>1</logverbosity>
    <!-- logverbosity values: "0"-"5" -->
    <valloglevel>0</valloglevel>
    <!-- valloglevel values: "0"-"2" -->
    <privatedomain/>
    <privateaddress/>                     <!-- comma-separated -->
    <insecuredomain/>
    <msgcachesize/>
    <rrsetcachesize/>
    <outgoingnumtcp/>
    <incomingnumtcp/>
    <numqueriesperthread/>
    <outgoingrange/>
    <jostletimeout/>
    <discardtimeout/>
    <cachemaxttl/>
    <cachemaxnegativettl/>
    <cacheminttl/>
    <infrahostttl/>
    <infrakeepprobing>0</infrakeepprobing>
    <infracachenumhosts/>
    <unwantedreplythreshold/>
  </advanced>

  <acls>
    <default_action>allow</default_action>
    <!-- default_action values: "allow", "deny", "refuse" -->
  </acls>

  <dnsbl>
    <!-- DNS Blocklist configuration -->
    <enabled>0</enabled>
    <type/>
    <!-- type values (comma-separated):
      "atf", "ag" (AdGuard), "el" (EasyList), "ep" (EasyPrivacy),
      "hgz001"-"hgz021" (various threat lists),
      "oisd0"-"oisd2" (OISD lists), "sb" (Steven Black), "yy"
    -->
    <lists/>
    <allowlists/>
    <blocklists/>
    <wildcards/>
    <source_nets/>
    <address/>
    <nxdomain/>
    <cache_ttl>72000</cache_ttl>
    <description/>
  </dnsbl>

  <forwarding>
    <enabled>0</enabled>
  </forwarding>

  <dots>
    <!-- DNS-over-TLS / forwarding entries -->
    <dot uuid="...">
      <enabled>1</enabled>
      <type>dot</type>
      <!-- type values: "dot" (DNS-over-TLS), "forward" (plain forwarding) -->
      <domain/>                           <!-- domain to forward (empty = all) -->
      <server>1.1.1.1</server>
      <port>853</port>
      <verify>cloudflare-dns.com</verify>
      <forward_tcp_upstream>0</forward_tcp_upstream>
      <forward_first>0</forward_first>
      <description>Cloudflare DoT</description>
    </dot>
  </dots>

  <hosts>
    <!-- Host overrides (local DNS records) -->
    <host uuid="...">
      <enabled>1</enabled>
      <hostname>server1</hostname>
      <domain>example.lan</domain>
      <rr>A</rr>
      <!-- rr values: "A" (IPv4), "AAAA" (IPv6), "MX" (mail), "TXT" (text) -->
      <mxprio/>                           <!-- MX priority (for rr=MX) -->
      <mx/>                               <!-- MX target (for rr=MX) -->
      <ttl/>
      <server>192.168.1.100</server>      <!-- IP address for A/AAAA records -->
      <txtdata/>                          <!-- TXT record data -->
      <aliascount>0</aliascount>
      <description/>
    </host>
  </hosts>

  <aliases>
    <!-- Host aliases (CNAME-like overrides) -->
    <alias uuid="...">
      <enabled>1</enabled>
      <host>uuid-of-parent-host</host>    <!-- references a host entry -->
      <hostname>alias1</hostname>
      <domain>example.lan</domain>
      <description/>
    </alias>
  </aliases>
</unboundplus>
```

---

## `<OPNsense><Kea>` -- Kea DHCP Server

```xml
<Kea>
  <ctrl_agent>
    <enabled>0</enabled>
    <http_host>127.0.0.1</http_host>
    <http_port>8000</http_port>
  </ctrl_agent>

  <dhcp4>
    <general>
      <enabled>0</enabled>
      <manual_config>0</manual_config>
      <interfaces/>                       <!-- comma-separated interface IDs -->
      <valid_lifetime>4000</valid_lifetime>
      <fwrules>1</fwrules>               <!-- auto-create firewall rules -->
      <dhcp_socket_type>raw</dhcp_socket_type>
      <!-- dhcp_socket_type values: "raw", "udp" -->
    </general>

    <subnets>
      <subnet4 uuid="...">
        <subnet>192.168.1.0/24</subnet>
        <next_server/>                    <!-- TFTP/PXE boot server -->
        <option_data_autocollect>1</option_data_autocollect>
        <match_client_id>1</match_client_id>
        <pools>192.168.1.100-192.168.1.200</pools>
        <option_data>
          <!-- DHCP options -->
          <domain_name_servers>192.168.1.1</domain_name_servers>
          <routers>192.168.1.1</routers>
          <domain_name>example.lan</domain_name>
          <ntp_servers/>
          <tftp_server_name/>
          <boot_file_name/>
          <domain_search/>
          <static_routes/>
        </option_data>
        <description>LAN subnet</description>
      </subnet4>
    </subnets>

    <reservations>
      <reservation uuid="...">
        <subnet>uuid-of-subnet</subnet>   <!-- references a subnet4 entry -->
        <ip_address>192.168.1.50</ip_address>
        <hw_address>aa:bb:cc:dd:ee:ff</hw_address>
        <hostname>server1</hostname>
        <description>Reserved for server</description>
      </reservation>
    </reservations>

    <ha_peers>
      <peer uuid="...">
        <name>primary</name>
        <role>primary</role>
        <!-- role values: "primary", "standby" -->
        <url>http://peer-ip:8000/</url>
      </peer>
    </ha_peers>
  </dhcp4>

  <dhcp6>
    <general>
      <enabled>0</enabled>
      <!-- similar structure to dhcp4 -->
    </general>
  </dhcp6>
</Kea>
```

---

## `<OPNsense><HAProxy>` -- HAProxy Load Balancer

### General Settings

```xml
<HAProxy>
  <general>
    <enabled>1</enabled>
    <gracefulStop>1</gracefulStop>
    <maxConnections>500</maxConnections>
    <nbthread/>                           <!-- number of threads -->
    <hard_stop_after>60s</hard_stop_after>
    <stickytablePeers>
      <peer uuid="...">
        <name>peer1</name>
        <enabled>1</enabled>
        <address>10.0.0.2</address>
        <port>10000</port>
      </peer>
    </stickytablePeers>
    <tuning>
      <maxRewrite/>
      <bufferSize/>
      <lua_maxmem/>
      <lua_session_timeout/>
      <lua_task_timeout/>
      <lua_service_timeout/>
      <ssl_maxrecord/>
      <spread_checks/>
      <max_ssl_connections/>
      <max_zlib_memory/>
      <comp_maxlevel/>
      <running_process/>
      <nbproc/>
    </tuning>
    <defaultsSection>
      <maxConnections/>
      <timeoutClient/>
      <timeoutConnect/>
      <timeoutCheck/>
      <timeoutServer/>
      <retries/>
      <noredispatch>1</noredispatch>
    </defaultsSection>
    <logging>
      <dontlog_normal>0</dontlog_normal>
      <send_hostname/>
      <send_hostname_field/>
    </logging>
    <stats>
      <enabled>0</enabled>
      <listen_address/>
      <listen_port/>
    </stats>
    <cache>
      <enabled>0</enabled>
      <total_max_size/>
      <max_object_size/>
      <max_age/>
      <process_vary/>
    </cache>
  </general>
```

### Frontends

```xml
  <frontends>
    <frontend uuid="...">
      <enabled>1</enabled>
      <name>frontend-https</name>
      <description>HTTPS Frontend</description>
      <bind>10.0.0.1:443</bind>          <!-- listen address:port -->
      <bindOptions/>                      <!-- extra bind options -->
      <mode>http</mode>
      <!-- mode values: "http", "ssl" (TCP+SSL passthrough), "tcp" -->
      <defaultBackend>uuid-of-backend</defaultBackend>
      <ssl_enabled>1</ssl_enabled>
      <ssl_certificates>uuid1,uuid2</ssl_certificates>  <!-- comma-separated cert UUIDs -->
      <ssl_default_certificate>uuid</ssl_default_certificate>
      <ssl_customOptions/>
      <ssl_advancedEnabled>0</ssl_advancedEnabled>
      <ssl_bindOptions>no-sslv3,no-tlsv10,no-tlsv11</ssl_bindOptions>
      <!-- ssl_bindOptions values (comma-separated):
        "no-sslv3", "no-tlsv10", "no-tlsv11", "no-tlsv12", "no-tlsv13",
        "no-tls-tickets", "force-sslv3", "force-tlsv10", "force-tlsv11",
        "force-tlsv12", "force-tlsv13", "prefer-client-ciphers", "strict-sni"
      -->
      <ssl_minVersion/>
      <!-- ssl version values: "SSLv3", "TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3" -->
      <ssl_maxVersion/>
      <ssl_cipherList/>
      <ssl_cipherSuites/>
      <ssl_hstsEnabled>1</ssl_hstsEnabled>
      <ssl_hstsIncludeSubDomains>0</ssl_hstsIncludeSubDomains>
      <ssl_hstsPreload>0</ssl_hstsPreload>
      <ssl_hstsMaxAge>15768000</ssl_hstsMaxAge>
      <ssl_clientAuthEnabled>0</ssl_clientAuthEnabled>
      <ssl_clientAuthVerify>none</ssl_clientAuthVerify>
      <!-- ssl_clientAuthVerify values: "none", "optional", "required" -->
      <ssl_clientAuthCAs/>
      <ssl_clientAuthCRLs/>
      <basicAuthEnabled>0</basicAuthEnabled>
      <basicAuthUsers/>
      <basicAuthGroups/>
      <tuning_maxConnections/>
      <tuning_timeoutClient/>
      <tuning_timeoutHttpReq/>
      <tuning_timeoutHttpKeepAlive/>
      <linkedCpuAffinityRules/>
      <tuning_shards/>
      <logging_dontLogNull>0</logging_dontLogNull>
      <logging_dontLogNormal>0</logging_dontLogNormal>
      <logging_logSeparateErrors>0</logging_logSeparateErrors>
      <logging_detailedLog>0</logging_detailedLog>
      <logging_socketStats>0</logging_socketStats>
      <stickiness_pattern/>
      <!-- stickiness_pattern values: "ipv4", "ipv6", "integer", "string", "binary" -->
      <stickiness_dataTypes/>
      <!-- stickiness_dataTypes values (comma-separated):
        "conn_cnt", "conn_cur", "conn_rate", "sess_cnt", "sess_rate",
        "http_req_cnt", "http_req_rate", "http_err_cnt", "http_err_rate",
        "bytes_in_cnt", "bytes_in_rate", "bytes_out_cnt", "bytes_out_rate"
      -->
      <stickiness_expire/>
      <stickiness_size/>
      <stickiness_counter/>
      <stickiness_counter_key/>
      <stickiness_length/>
      <stickiness_connRatePeriod/>
      <stickiness_sessRatePeriod/>
      <stickiness_httpReqRatePeriod/>
      <stickiness_httpErrRatePeriod/>
      <stickiness_bytesInRatePeriod/>
      <stickiness_bytesOutRatePeriod/>
      <http2Enabled>1</http2Enabled>
      <http2Enabled_nontls>0</http2Enabled_nontls>
      <advertised_protocols>h2,http/1.1</advertised_protocols>
      <!-- advertised_protocols values: "h2", "http/1.1", "http/1.0" -->
      <prometheus_enabled>0</prometheus_enabled>
      <prometheus_path/>
      <connectionBehaviour>http-keep-alive</connectionBehaviour>
      <!-- connectionBehaviour values:
        "http-keep-alive", "httpclose", "http-server-close"
      -->
      <customOptions/>
      <linkedActions>uuid1,uuid2</linkedActions>   <!-- comma-separated action UUIDs -->
      <linkedErrorfiles/>
    </frontend>
  </frontends>
```

### Backends

```xml
  <backends>
    <backend uuid="...">
      <enabled>1</enabled>
      <name>backend-webservers</name>
      <description>Web server pool</description>
      <mode>http</mode>
      <!-- mode values: "http", "tcp" -->
      <algorithm>roundrobin</algorithm>
      <!-- algorithm values:
        "source", "roundrobin", "static-rr", "leastconn", "uri", "random"
      -->
      <random_draws>2</random_draws>
      <proxyProtocol/>
      <!-- proxyProtocol values: "v1", "v2" -->
      <linkedServers>uuid1,uuid2</linkedServers>
      <linkedFcgi/>
      <linkedResolver/>
      <resolverOpts/>
      <!-- resolverOpts values: "allow-dup-ip", "ignore-weight", "prevent-dup-ip" -->
      <resolvePrefer/>
      <!-- resolvePrefer values: "ipv4", "ipv6" -->
      <source/>
      <healthCheckEnabled>0</healthCheckEnabled>
      <healthCheck/>
      <healthCheckLogStatus>0</healthCheckLogStatus>
      <checkInterval/>
      <checkDownInterval/>
      <healthCheckFall/>
      <healthCheckRise/>
      <linkedMailer/>
      <http2Enabled>0</http2Enabled>
      <http2Enabled_nontls>0</http2Enabled_nontls>
      <ba_advertised_protocols/>
      <forwardFor>1</forwardFor>
      <forwardedHeader/>
      <forwardedHeaderParameters/>
      <!-- forwardedHeaderParameters values (comma-separated):
        "proto", "host", "by", "by-port", "for", "for-port"
      -->
      <persistence/>
      <!-- persistence values: "sticktable", "cookie" -->
      <persistence_cookiemode>piggyback</persistence_cookiemode>
      <!-- persistence_cookiemode values: "piggyback", "new" -->
      <persistence_cookiename/>
      <persistence_stripquotes>0</persistence_stripquotes>
      <stickiness_pattern/>
      <!-- stickiness_pattern values:
        "sourceipv4", "sourceipv6", "cookievalue", "rdpcookie"
      -->
      <stickiness_dataTypes/>
      <stickiness_expire/>
      <stickiness_size/>
      <stickiness_cookiename/>
      <stickiness_cookielength/>
      <stickiness_connRatePeriod/>
      <stickiness_sessRatePeriod/>
      <stickiness_httpReqRatePeriod/>
      <stickiness_httpErrRatePeriod/>
      <stickiness_bytesInRatePeriod/>
      <stickiness_bytesOutRatePeriod/>
      <basicAuthEnabled>0</basicAuthEnabled>
      <basicAuthUsers/>
      <basicAuthGroups/>
      <tuning_timeoutConnect/>
      <tuning_timeoutCheck/>
      <tuning_timeoutServer/>
      <tuning_retries/>
      <customOptions/>
      <tuning_defaultserver/>
      <tuning_noport>0</tuning_noport>
      <tuning_httpreuse>safe</tuning_httpreuse>
      <!-- tuning_httpreuse values: "never", "safe", "aggressive", "always" -->
      <tuning_caching>0</tuning_caching>
      <linkedActions/>
      <linkedErrorfiles/>
    </backend>
  </backends>
```

### Servers

```xml
  <servers>
    <server uuid="...">
      <enabled>1</enabled>
      <name>webserver1</name>
      <description/>
      <address>192.168.1.100</address>
      <port>80</port>
      <checkport/>
      <mode>active</mode>
      <!-- mode values: "active", "backup", "disabled" -->
      <multiplexer_protocol/>
      <!-- multiplexer_protocol values: "", "fcgi", "h2", "h1" -->
      <type>static</type>
      <!-- type values: "static", "template", "unix" -->
      <serviceName/>                      <!-- for DNS SRV template resolution -->
      <number/>                           <!-- for template type -->
      <linkedResolver/>
      <resolverOpts/>
      <resolvePrefer/>
      <ssl>0</ssl>
      <sslSNI/>
      <sslVerify>0</sslVerify>
      <sslCA/>
      <sslCRL/>
      <sslClientCertificate/>
      <maxConnections/>
      <weight/>
      <checkInterval/>
      <checkDownInterval/>
      <source/>
      <advanced/>
      <unix_socket/>                      <!-- for unix socket type -->
    </server>
  </servers>
```

### ACLs (Conditions)

```xml
  <acls>
    <acl uuid="...">
      <name>is_example_com</name>
      <description>Match example.com requests</description>
      <expression>ssl_sni</expression>
      <!-- expression values:
        Match types:
          "http_auth"        - HTTP authentication
          "hdr_beg"          - Header begins with
          "hdr_end"          - Header ends with
          "hdr"              - Header exact match
          "hdr_reg"          - Header regex match
          "hdr_sub"          - Header substring
          "path_beg"         - Path begins with
          "path_end"         - Path ends with
          "path"             - Path exact match
          "path_reg"         - Path regex match
          "path_dir"         - Path directory match
          "path_sub"         - Path substring
          "url_param"        - URL parameter match
          "cust_hdr_beg/end/reg/sub" - Custom header matches
        SSL:
          "ssl_c_verify"     - Client cert verification
          "ssl_c_verify_code"- Specific verify code
          "ssl_c_ca_commonname" - Client CA common name
          "ssl_hello_type"   - SSL hello type (0=not SSL, 1=SSLv2, 2=TLS)
          "ssl_fc"           - Connection is SSL
          "ssl_fc_sni"       - SNI exact match
          "ssl_sni"          - SNI match (deprecated alias)
          "ssl_sni_sub/beg/end/reg" - SNI sub/begin/end/regex
        Source:
          "src"              - Source IP/network match
          "src_is_local"     - Source is local
          "src_port"         - Source port
          "src_bytes_in_rate/out_rate" - Byte rates
          "src_conn_cnt/cur/rate"      - Connection counters
          "src_http_err_cnt/rate"      - HTTP error counters
          "src_http_req_cnt/rate"      - HTTP request counters
          "src_kbytes_in/out"          - Kilobyte counters
          "src_sess_cnt/rate"          - Session counters
        Other:
          "traffic_is_http"  - Traffic is HTTP
          "traffic_is_ssl"   - Traffic is SSL
          "nbsrv"            - Number of available servers in backend
          "custom_acl"       - Custom ACL expression
      -->
      <negate>0</negate>
      <caseSensitive>0</caseSensitive>
      <!-- Match fields (populated based on expression type): -->
      <ssl_sni>example.com</ssl_sni>
      <!-- ... other expression-specific fields ... -->
    </acl>
  </acls>
```

### Actions (Rules)

```xml
  <actions>
    <action uuid="...">
      <name>redirect_to_https</name>
      <description>Redirect HTTP to HTTPS</description>
      <testType>IF</testType>
      <!-- testType values: "IF", "UNLESS" -->
      <linkedAcls>uuid1,uuid2</linkedAcls>
      <operator>AND</operator>
      <!-- operator values: "AND", "OR" -->
      <type>http_request_redirect</type>
      <!-- type values:
        Backend routing:
          "use_backend", "use_server", "map_use_backend"
        FastCGI:
          "fcgi_pass_header", "fcgi_set_param"
        HTTP request actions:
          "http_request_allow", "http_request_deny", "http_request_tarpit",
          "http_request_auth", "http_request_redirect", "http_request_lua",
          "http_request_use_service",
          "http_request_add_header", "http_request_set_header",
          "http_request_del_header", "http_request_replace_header",
          "http_request_replace_value",
          "http_request_set_path", "http_request_set_var"
        HTTP response actions:
          "http_response_allow", "http_response_deny", "http_response_lua",
          "http_response_add_header", "http_response_set_header",
          "http_response_del_header", "http_response_replace_header",
          "http_response_replace_value",
          "http_response_set_status", "http_response_set_var"
        Monitoring:
          "monitor_fail"
        TCP request:
          "tcp_request_connection_accept", "tcp_request_connection_reject",
          "tcp_request_content_accept", "tcp_request_content_reject",
          "tcp_request_content_lua", "tcp_request_content_use_service",
          "tcp_request_inspect_delay"
        TCP response:
          "tcp_response_content_accept", "tcp_response_content_close",
          "tcp_response_content_reject", "tcp_response_content_lua",
          "tcp_response_inspect_delay"
        Custom:
          "custom"
      -->
      <!-- Type-specific fields: -->
      <http_request_redirect>https://%[hdr(host)]%[path]</http_request_redirect>
      <use_backend>uuid-of-backend</use_backend>
      <use_server>uuid-of-server</use_server>
      <http_request_set_var_scope>txn</http_request_set_var_scope>
      <!-- var scope values: "proc", "sess", "txn", "req", "res" -->
      <http_request_set_var_name/>
      <http_request_set_var_expr/>
      <!-- ... many other type-specific fields ... -->
    </action>
  </actions>
```

### Lua Scripts

```xml
  <luas>
    <lua uuid="...">
      <enabled>1</enabled>
      <name>json</name>
      <description>JSON library for Lua</description>
      <content>base64-encoded-lua-script</content>
    </lua>
  </luas>
```

### Other HAProxy Subsections

```xml
  <healthchecks>
    <healthcheck uuid="...">
      <name>http-check</name>
      <type>http</type>
      <!-- type values: "http", "tcp", "mysql", "pgsql", "redis", "smtp", "esmtp", "ssl", "ldap", "agent" -->
      <interval/>
      <path>/health</path>
      <httpVersion>HTTP/1.1</httpVersion>
      <checkExpect/>
    </healthcheck>
  </healthchecks>

  <fcgis/>           <!-- FastCGI application definitions -->
  <errorfiles/>      <!-- Custom error page files -->
  <mapfiles/>        <!-- HAProxy map files -->
  <groups/>          <!-- HAProxy user groups (for basic auth) -->
  <users/>           <!-- HAProxy users (for basic auth) -->
  <cpus/>            <!-- CPU affinity rules -->
  <resolvers/>       <!-- DNS resolver definitions for server discovery -->
  <mailers/>         <!-- Email alerting configuration -->

  <maintenance>
    <maintenanceEnabled>0</maintenanceEnabled>
  </maintenance>
</HAProxy>
```

---

## `<OPNsense><AcmeClient>` -- ACME / Let's Encrypt

```xml
<AcmeClient>
  <settings>
    <enabled>1</enabled>
    <environment/>                        <!-- "" (production) or "staging" -->
    <logLevel/>
    <autoRenewal>1</autoRenewal>
    <renewInterval>60</renewInterval>     <!-- days before expiry to renew -->
    <haproxyIntegration>1</haproxyIntegration>
    <challengePort>43580</challengePort>
    <tlsChallengePort/>
  </settings>

  <accounts>
    <account uuid="...">
      <enabled>1</enabled>
      <name>My CA Account</name>
      <description/>
      <email>admin@example.com</email>
      <ca>custom_url</ca>
      <!-- ca values: "letsencrypt", "buypass", "zerossl", "google", "ssl_com",
           "custom_url" (for private CA like OpenBao/Vault) -->
      <customCaUrl>http://ca.example.lan:8200/v1/pki/acme/directory</customCaUrl>
      <customCaEABKeyId/>
      <customCaEABKey/>
      <statusCode/>
      <statusLastUpdate/>
    </account>
  </accounts>

  <certificates>
    <certificate uuid="...">
      <enabled>1</enabled>
      <name>example.com</name>
      <description/>
      <altNames>www.example.com,mail.example.com</altNames>  <!-- comma-separated SANs -->
      <account>uuid-of-account</account>
      <validationMethod>uuid-of-validation</validationMethod>
      <keyLength>4096</keyLength>
      <!-- keyLength values: "2048", "3072", "4096", "ec-256", "ec-384" -->
      <ocsp>0</ocsp>
      <autoRenewal>1</autoRenewal>
      <renewInterval/>
      <lastUpdate/>
      <statusCode/>
      <statusLastUpdate/>
    </certificate>
  </certificates>

  <validations>
    <validation uuid="...">
      <enabled>1</enabled>
      <name>HTTP-01 via HAProxy</name>
      <description/>
      <method>http01</method>
      <!-- method values: "http01", "dns01", "tlsalpn01" -->
      <dns_service/>
      <!-- dns_service values (for dns01):
        "cloudflare", "route53", "digitalocean", "godaddy", "namecheap",
        "nsone", "ovh", "powerdns", "gcloud", "azure", "hetzner",
        "duckdns", "desec", "acmedns", "inwx", "lexicon", ... many more
      -->
      <dns_environment/>                  <!-- provider-specific env vars -->
      <http_service>opnsense</http_service>
      <!-- http_service values: "opnsense" (built-in challenge server) -->
      <http_opn_autodiscovery>haproxy</http_opn_autodiscovery>
      <!-- http_opn_autodiscovery values: "" (disabled), "haproxy" (auto-inject) -->
    </validation>
  </validations>

  <actions>
    <!-- Post-issuance automation actions -->
    <action uuid="...">
      <enabled>1</enabled>
      <name>Restart HAProxy</name>
      <type>configd</type>
      <configd>haproxy restart</configd>
    </action>
  </actions>
</AcmeClient>
```

---

## `<OPNsense><Interfaces>` -- MVC Interface Settings

```xml
<Interfaces>
  <loopbacks/>                            <!-- additional loopback interfaces -->
  <neighbors/>                            <!-- ARP/NDP static entries -->
  <vxlans/>                               <!-- VXLAN tunnel interfaces -->
  <settings>
    <offloading>
      <hardware_crc>1</hardware_crc>
      <hardware_tso>1</hardware_tso>
      <hardware_lro>1</hardware_lro>
    </offloading>
  </settings>
</Interfaces>
```

---

## `<OPNsense><IDS>` -- Intrusion Detection System (Suricata)

```xml
<IDS>
  <general>
    <enabled>0</enabled>
    <ips>0</ips>                          <!-- 1 = IPS mode (inline blocking) -->
    <promisc>0</promisc>
    <interfaces/>
    <homenet>192.168.0.0/16,10.0.0.0/8,172.16.0.0/12</homenet>
    <defaultPacketSize/>
    <UpdateCron/>
    <AlertLogrotate>W0D23</AlertLogrotate>
    <AlertSaveLogs>4</AlertSaveLogs>
    <MPMAlgo>ac</MPMAlgo>
    <!-- MPMAlgo values: "ac" (Aho-Corasick), "hs" (Hyperscan), "ac-bs", "ac-ks" -->
    <syslog>0</syslog>
    <syslog_eve>0</syslog_eve>
    <LogPayload>0</LogPayload>
  </general>
  <rules/>
  <policies/>
  <userDefinedRules/>
</IDS>
```

---

## `<OPNsense><wireguard>` -- WireGuard VPN

```xml
<wireguard>
  <client>
    <clients/>                            <!-- WireGuard peer definitions -->
  </client>
  <general>
    <enabled>0</enabled>
  </general>
  <server>
    <servers/>                            <!-- WireGuard interface/tunnel definitions -->
  </server>
</wireguard>
```

---

## `<OPNsense><Syslog>` -- Remote Syslog

```xml
<Syslog>
  <general>
    <enabled>1</enabled>
    <loglocal>1</loglocal>
    <maxpreserve>31</maxpreserve>
    <maxfilesize/>
  </general>
  <destinations>
    <destination uuid="...">
      <enabled>1</enabled>
      <transport>udp4</transport>
      <!-- transport values: "udp4", "udp6", "tcp4", "tcp6", "tls4", "tls6" -->
      <hostname>syslog.example.com</hostname>
      <port>514</port>
      <program/>
      <level/>
      <facility/>
      <certificate/>
      <rfc5424>0</rfc5424>
      <description/>
    </destination>
  </destinations>
</Syslog>
```

---

## `<OPNsense><TrafficShaper>` -- Traffic Shaping (ALTQ)

```xml
<TrafficShaper>
  <pipes>
    <pipe uuid="...">
      <enabled>1</enabled>
      <number>1</number>
      <bandwidth>100</bandwidth>
      <bandwidthMetric>Mbit</bandwidthMetric>
      <!-- bandwidthMetric values: "Kbit", "Mbit", "Gbit" -->
      <queue/>
      <mask>none</mask>
      <!-- mask values: "none", "src-ip", "dst-ip" -->
      <buckets/>
      <scheduler/>
      <codel_enable>0</codel_enable>
      <codel_target/>
      <codel_interval/>
      <fqcodel_quantum/>
      <fqcodel_limit/>
      <fqcodel_flows/>
      <pie_enable>0</pie_enable>
      <description/>
    </pipe>
  </pipes>
  <queues/>
  <rules/>
</TrafficShaper>
```

---

## `<OPNsense><monit>` -- Monit Monitoring

```xml
<monit>
  <general>
    <enabled>0</enabled>
    <interval>120</interval>
    <startdelay>120</startdelay>
    <mailserver/>
    <port/>
    <username/>
    <password/>
    <ssl>0</ssl>
    <sslversion>auto</sslversion>
    <sslverify>1</sslverify>
    <logfile>syslog facility log_daemon</logfile>
    <statefile/>
    <eventqueuePath/>
    <eventqueueSlots/>
    <httpdEnabled>0</httpdEnabled>
    <httpdPort>2812</httpdPort>
    <httpdAllow/>
    <mmonitUrl/>
    <mmonitTimeout/>
    <mmonitRegisterCredentials/>
  </general>
  <alert/>
  <service>
    <!-- Monitored services -->
    <service uuid="...">
      <enabled>1</enabled>
      <name>system</name>
      <type>3</type>
      <!-- type values: "0" (filesystem), "1" (directory), "2" (file),
           "3" (process), "4" (host), "5" (system), "6" (fifo), "7" (custom),
           "8" (network) -->
      <pidfile/>
      <match/>
      <path/>
      <timeout>300</timeout>
      <starttimeout>30</starttimeout>
      <address/>
      <interface/>
      <start/>
      <stop/>
      <tests>uuid1,uuid2</tests>
      <depends/>
      <polltime/>
      <description/>
    </service>
  </service>
  <test>
    <test uuid="...">
      <name>Memory</name>
      <type>SystemResource</type>
      <!-- type values: "NetworkPing", "NetworkPort", "SystemResource",
           "ProcessResource", "FileChecksum", "FilesystemMountFlags",
           "SpaceUsage", "FileTimestamp", "FileContentMatch", "ProgramStatus",
           "ConnectionFailed", "Custom" -->
      <condition>memory usage is greater than 75%</condition>
      <action>alert</action>
      <!-- action values: "alert", "restart", "start", "stop", "exec", "unmonitor" -->
      <path/>
    </test>
  </test>
</monit>
```

---

## `<OPNsense><cron>` -- Scheduled Tasks

```xml
<cron>
  <jobs>
    <job uuid="...">
      <enabled>1</enabled>
      <minutes>0</minutes>                <!-- cron minute field -->
      <hours>0</hours>                    <!-- cron hour field -->
      <days>*</days>                      <!-- cron day-of-month field -->
      <months>*</months>                  <!-- cron month field -->
      <weekdays>*</weekdays>              <!-- cron day-of-week field -->
      <who>root</who>
      <command>firmware auto-update</command>
      <parameters/>
      <description>Firmware update check</description>
      <origin>cron</origin>
    </job>
  </jobs>
</cron>
```

---

## `<OPNsense><trust>` -- Trust / Certificate Store Settings

```xml
<trust>
  <general>
    <minCertDays>30</minCertDays>         <!-- minimum days before cert expiry warning -->
    <castore>0</castore>
    <crlstore>0</crlstore>
    <autoserial>1</autoserial>
    <serialBits>32</serialBits>
    <defaultDays>365</defaultDays>
    <defaultDigest>sha256</defaultDigest>
    <!-- defaultDigest values: "sha1", "sha256", "sha384", "sha512" -->
    <defaultKeySize>2048</defaultKeySize>
    <!-- defaultKeySize values: "1024", "2048", "3072", "4096", "8192" -->
    <defaultEcCurve>prime256v1</defaultEcCurve>
    <!-- defaultEcCurve values: "prime256v1", "secp384r1", "secp521r1" -->
    <defaultKeyType>RSA</defaultKeyType>
    <!-- defaultKeyType values: "RSA", "Elliptic Curve" -->
    <defaultCountry/>
    <defaultState/>
    <defaultCity/>
    <defaultOrganization/>
  </general>
</trust>
```

---

## `<OPNsense><IPsec>` -- IPsec VPN

```xml
<IPsec>
  <general>
    <enabled>0</enabled>
  </general>
  <charon>
    <threads>16</threads>
    <ikesa_table_size/>
    <ikesa_table_segments/>
    <init_limit_half_open/>
    <install_routes>0</install_routes>
    <close_ike_on_child_failure>0</close_ike_on_child_failure>
  </charon>
  <keyPairs/>
  <preSharedKeys/>
</IPsec>
```

---

## `<OPNsense><Swanctl>` -- strongSwan VPN Configuration

```xml
<Swanctl>
  <Connections>
    <Connection uuid="...">
      <enabled>0</enabled>
      <version>2</version>               <!-- IKE version: "1", "2", "0" (any) -->
      <local_addrs/>
      <remote_addrs/>
      <proposals>default</proposals>
      <!-- proposals: "default" or explicit like "aes256-sha256-modp2048" -->
      <rekey_time/>
      <over_time/>
      <dpd_delay>60s</dpd_delay>
    </Connection>
  </Connections>
  <locals/>                               <!-- local authentication rules -->
  <remotes/>                              <!-- remote authentication rules -->
  <children/>                             <!-- child SA (IPSEC policy) definitions -->
  <Pools/>                                <!-- virtual IP pools -->
  <VTIs/>                                 <!-- VTI interfaces -->
  <SPDs/>                                 <!-- Security Policy Database entries -->
</Swanctl>
```

---

## `<hasync>` -- High Availability Sync

```xml
<hasync>
  <pfsyncenabled/>
  <pfsyncinterface/>
  <pfsyncpeerip/>
  <synchronizetoip/>
  <username/>
  <password/>
  <services/>                             <!-- comma-separated service names to sync -->
  <disablepreempt/>
  <disconnectppps/>
  <synchronizeinterfacesonly/>
</hasync>
```

---

## `<revision>` -- Configuration Revision Metadata

```xml
<revision>
  <time>1700000000.00</time>
  <description>API change description</description>
  <username>root@10.0.0.1</username>
  <encoding>base64</encoding>
</revision>
```

This section is automatically updated on every config change and records who made the change and when.

---

## Data Format Conventions

| Convention | Example | Description |
|-----------|---------|-------------|
| Booleans | `<enabled>1</enabled>` | `"1"` = true, `"0"` or `""` = false |
| UUIDs | `uuid="a1b2c3d4-..."` | XML attribute on collection items |
| References | `<account>uuid-value</account>` | UUID string referencing another element |
| Multi-value | `<interface>wan,lan,opt1</interface>` | Comma-separated within single element |
| Empty/unset | `<field/>` | Self-closing tag = unset/default |
| Newline lists | `<content>10.0.0.1\n10.0.0.2</content>` | Newline-separated (alias content) |
| Timestamps | `<time>1700000000.00</time>` | Unix epoch with fractional seconds |
| Base64 blobs | `<crt>LS0tLS1CRUdJ...</crt>` | Certificates, keys, Lua scripts |
| Versioned sections | `version="1.0.10"` | Attribute on section root for schema migration |
