# bond-util
bond-util使用指南

使用前提
	系统经过PXE部署完毕，并收集完毕PXE的IP。
使用流程
	部署节点的/etc/bond-util目录下有网卡配置的模板、bond配置模板以及输入物料清单的模板样例，可供参考。

1.	准备input.csv文件
可从部署节点/etc/bond-util/input.csv.sample下载，另存为input.csv文件 
文件中包含ADMIN，PUBLIC，PRIVATE，STORAGE四种openstack网络的定义及配置。各字段含义如下：
SERIAL_NUMBER: 主机序列号
PXE_IP：该主机PXE时自动获取的IP地址
HOSTNAME: 主机名

ADMIN_NAME: 管理网bond名字（如需建立vlan子接口，直接将该网卡名命名为vlan子接口名字样式即可，例如bond0.30，即为bond0上建立一个vlan30的子接口）。
ADMIN_IP：admin网络需要设置的ip地址
ADMIN_INTERFACE: 为admin网络分配的网卡名字，网卡之间用英文逗号隔开。

PUBLIC、PRIVATE、STORAGE的网络设置类似ADMIN的设置，如果无需设置IP，IP一栏不填即可。

2.	Bond配置文件
Bond的配置文件位于/etc/bond-util/目录下，一般情况下根据网络规划，如需要为那个网络设置bond类型、子网掩码、默认网关等特殊信息，就为那个网络单独配置。
例如要为admin网络指明bond类型、子网掩码及默认网关：
 

3.	生成网卡配置信息
配置好网卡的各网络的bond模板信息后，将编辑好的csv物料清单上传到部署节点上。执行generate-bond指令。如：
generate-bond ./input.csv
会在/tmp目录下生成已pxe的ip命名的文件夹，文件夹内即为各类型网络的配置信息，然后通过scp指令将网卡及bond的配置文件考到各目标主机，重启网络即可。
