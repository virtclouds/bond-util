BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root  
Name:		bond-util
Version:	1.1
Release:	1%{?dist}
Summary:	bond-util rpm package

Group:		Application
License:	GPL
URL:		http://www.virtclouds.com
Source0:	%{name}-%{version}.tar.gz


%description
This is a software for generating bond file for network configuration while deploying OpenStack.


%prep
%setup -q


%install
mkdir -p $RPM_BUILD_ROOT/etc/bond-util
install -m 644 conf/bond_admin.sample $RPM_BUILD_ROOT/etc/bond-util/bond_admin.sample
install -m 644 conf/bond_storage.sample $RPM_BUILD_ROOT/etc/bond-util/bond_storage.sample
install -m 644 conf/eth_interface.sample $RPM_BUILD_ROOT/etc/bond-util/eth_interface.sample
install -m 644 conf/input.csv.sample $RPM_BUILD_ROOT/etc/bond-util/input.csv.sample
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 src/generate_bond.py $RPM_BUILD_ROOT/usr/bin/generate-bond

%files
/etc/bond-util/bond_admin.sample
/etc/bond-util/bond_storage.sample
/etc/bond-util/eth_interface.sample
/etc/bond-util/input.csv.sample
/usr/bin/generate-bond


%changelog
* Wed Nov 22 2017 Zhaokun Fu <fuzk@inspur.com> - 1.0-1
- Add gatway for bond configuration.
