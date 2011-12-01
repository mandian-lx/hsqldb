# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global cvs_version 1_8_1_3

Name:       hsqldb
Version:    1.8.1.3
Release:    5
Epoch:	    1
Summary:    HyperSQL Database Engine
License:    BSD
URL:        http://hsqldb.sourceforge.net/
Source0:    http://downloads.sourceforge.net/hsqldb/%{name}_%{cvs_version}.zip
Source1:    %{name}-1.8.0-standard.cfg
Source2:    %{name}-1.8.0-standard-server.properties
Source3:    %{name}-1.8.0-standard-webserver.properties
Source4:    %{name}-1.8.0-standard-sqltool.rc
Source5:    http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.8.0.10/%{name}-1.8.0.10.pom
Patch0:     %{name}-1.8.0-scripts.patch
Patch1:     hsqldb-tmp.patch
Patch2:     %{name}-1.8.0-specify-su-shell.patch
Requires:   servlet25
Requires(post):   coreutils
Requires(preun):  coreutils
Requires(preun): initscripts
Requires(pre):  shadow-utils
Requires(post): jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  servlet25
Group:      Databases
BuildArch:  noarch

%description
HSQLdb is a relational database engine written in JavaTM , with a JDBC
driver, supporting a subset of ANSI-92 SQL. It offers a small (about
100k), fast database engine which offers both in memory and disk based
tables. Embedded and server modes are available. Additionally, it
includes tools such as a minimal web server, in-memory query and
management tools (can be run as applets or servlets, too) and a number
of demonstration examples.
Downloaded code should be regarded as being of production quality. The
product is currently being used as a database and persistence engine in
many Open Source Software projects and even in commercial projects and
products! In it's current version it is extremely stable and reliable.
It is best known for its small size, ability to execute completely in
memory and its speed. Yet it is a completely functional relational
database management system that is completely free under the Modified
BSD License. Yes, that's right, completely free of cost or restrictions!

%package manual
Summary:    Manual for %{name}
Group:      Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   jpackage-utils

%description javadoc
Javadoc for %{name}.

%package demo
Summary:    Demo for %{name}
Group:      Development/Java
Requires:   %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -T -c -n %{name}
(cd ..
unzip -q %{SOURCE0} 
)
# set right permissions
find . -name "*.sh" -exec chmod 755 \{\} \;
# remove all _notes directories
for dir in `find . -name _notes`; do rm -rf $dir; done
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
find . -name "*.war" -exec rm -f {} \;
# correct silly permissions
chmod -R go=u-w *

%patch0
%patch1 -p1
%patch2

cp %{SOURCE5} ./pom.xml

%build
export CLASSPATH=$(build-classpath \
servlet \
junit)
pushd build
ant jar javadoc
popd

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 lib/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar
# bin
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 bin/runUtil.sh %{buildroot}%{_bindir}/%{name}RunUtil
# sysv init
install -d -m 755 %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 bin/%{name} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
# config
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
# serverconfig
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 644 %{SOURCE2} %{buildroot}%{_localstatedir}/lib/%{name}/server.properties
install -m 644 %{SOURCE3} %{buildroot}%{_localstatedir}/lib/%{name}/webserver.properties
install -m 600 %{SOURCE4} %{buildroot}%{_localstatedir}/lib/%{name}/sqltool.rc
# lib
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/lib
install -m 644 lib/functions %{buildroot}%{_localstatedir}/lib/%{name}/lib
# data
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/data
# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/demo
install -m 755 demo/*.sh %{buildroot}%{_datadir}/%{name}/demo
install -m 644 demo/*.html %{buildroot}%{_datadir}/%{name}/demo
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -r doc/src/* %{buildroot}%{_javadocdir}/%{name}
rm -rf doc/src
# manual
install -d -m 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -r doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp index.html %{buildroot}%{_docdir}/%{name}-%{version}

# Maven metadata
install -pD -T -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

pushd %{buildroot}%{_localstatedir}/lib/%{name}/lib
    ln -s $(build-classpath hsqldb) hsqldb.jar
    ln -s $(build-classpath servlet) servlet.jar
popd

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%pre
# Add the "hsqldb" user and group
# we need a shell to be able to use su - later
%{_sbindir}/groupadd -g 96 -f -r %{name} 2> /dev/null || :
%{_sbindir}/useradd -u 96 -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name} -r %{name} 2> /dev/null || :

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}

%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%doc doc/hsqldb_lic.txt
%{_javadir}/*
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0700,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/data
%{_localstatedir}/lib/%{name}/lib
%{_localstatedir}/lib/%{name}/server.properties
%{_localstatedir}/lib/%{name}/webserver.properties
%attr(0600,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/sqltool.rc
%dir %{_localstatedir}/lib/%{name}
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%doc doc/hsqldb_lic.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc doc/hsqldb_lic.txt

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}

