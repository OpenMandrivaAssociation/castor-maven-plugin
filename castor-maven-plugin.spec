%{?_javapackages_macros:%_javapackages_macros}
Name:             castor-maven-plugin
Version:          2.1
Release:          2.0%{?dist}
Summary:          Maven plugin for Castor XML's code generator
License:          ASL 2.0

URL:              http://mojo.codehaus.org/%{name}

Source0:          http://repo2.maven.org/maven2/org/codehaus/mojo/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:          LICENSE-2.0.txt
Patch0:           converter-static-method.patch

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    mojo-parent
BuildRequires:    castor >= 1.3.2-9

%description
The Castor plugin is a Maven plugin that provides the functionality of Castor
XML's code generator for generating Java beans and associated descriptor
classes (required for marshaling to and unmarshaling from XML documents) from
XML Schema files.

%package javadoc
Summary:          Javadoc for %{name}


%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# Upstream doesn't ship a copy of the licence with the source
cp -p %{SOURCE1} .

# Remove any pre-built binaries
find -name "*.jar" -exec rm {} \;
find -name "*.class" -exec rm {} \;

# Patch due to a method in castor is no longer static
sed -i 's/\r/\n/g' src/main/java/org/codehaus/mojo/castor/ConvertDTD2XSDMojo.java
%patch0 -p0 -b.orig

# Missing dep on maven core
%pom_add_dep org.apache.maven:maven-core

%mvn_file :%{name} %{name}

%build
# A couple of tests are in error due to ComponentLookupException during test setup
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Aug 10 2013 Mat Booth <fedora@matbooth.co.uk> - 2.1-2
- Remove pre-built binaries in %%prep

* Fri Aug 09 2013 Mat Booth <fedora@matbooth.co.uk> - 2.1-1
- Initial version of the package

