Name:           perl-XML-LibXML
# NOTE: also update perl-XML-LibXSLT to the same version, see
# https://bugzilla.redhat.com/show_bug.cgi?id=469480
Version:        1.70
Release:        5%{?dist}
# Epoch set when version went from 1.62001 to 1.65
Epoch:          1
Summary:        Perl interface to the libxml2 library

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-LibXML/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       %(perl -MConfig -le 'if (defined $Config{useithreads}) { print "perl(:WITH_ITHREADS)" } else { print "perl(:WITHOUT_ITHREADS)" }')
Requires:       %(perl -MConfig -le 'if (defined $Config{usethreads}) { print "perl(:WITH_THREADS)" } else { print "perl(:WITHOUT_THREADS)" }')
Requires:       %(perl -MConfig -le 'if (defined $Config{uselargefiles}) { print "perl(:WITH_LARGEFILES)" } else { print "perl(:WITHOUT_LARGEFILES)" }')
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0:        http://www.cpan.org/authors/id/P/PA/PAJAS/XML-LibXML-%{version}.tar.gz
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::SAX)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires:  libxml2-devel
Provides:       perl-XML-LibXML-Common = %{version}
Obsoletes:      perl-XML-LibXML-Common <= 0.13

%description
This module implements a Perl interface to the GNOME libxml2 library
which provides interfaces for parsing and manipulating XML files. This
module allows Perl programmers to make use of the highly capable
validating XML parser and the high performance DOM implementation.

%prep
%setup -q -n XML-LibXML-%{version}

%build
%{__perl} Makefile.PL SKIP_SAX_INSTALL=1 INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for i in Changes; do
  /usr/bin/iconv -f iso8859-1 -t utf-8 $i > $i.conv && /bin/mv -f $i.conv $i
done

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- perl-XML-SAX
for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
  perl -MXML::SAX -e "XML::SAX->add_parser(q($p))->save_parsers()" \
    2>/dev/null || :
done

%preun
if [ $1 -eq 0 ] ; then
  for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
    perl -MXML::SAX -e "XML::SAX->remove_parser(q($p))->save_parsers()" \
      2>/dev/null || :
  done
fi

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorarch}/auto/XML
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

%changelog
* Fri Jan  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-5
- remove BR XML::LibXML::Common
- Resolves: rhbz#543948

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:1.70-4
- rebuild against perl 5.10.1

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-3
- corrected version of obsoletes

* Thu Nov 26 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-2
- 541605 this package now contains XML::LibXML::Common

* Fri Nov 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.70-1
- update to fix 539102

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.69-1
- update to 1.69

* Fri Aug 01 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:1.66-2
- Supress warning about nonexistent file in perl-XML-SAX install trigger

* Mon Jun 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:1.66-1
- upgrade to 1.66

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.65-5
- Rebuild for perl 5.10 (again)

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-4
- Build for new perl

* Mon Feb 11 2008 Robin Norwood <rnorwood@redhat.com> - 1:1.65-3
- Resolves: bz#432442
- Use epoch to permit upgrade from 1.62001 -> 1.65

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-2
- disable hacks, build normally

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.65-1.1
- rebuild for new perl, first pass, temporarily disable BR: XML::Sax, tests

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.65-1
- Update to latest CPAN release: 1.65
- patch0 no longer needed
- various spec file cleanups

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.3
- fix stupid test

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.2
- add BR: perl(Test::More)

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.62001-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Dec 07 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001-2
- Rebuild

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.62001
- Build latest version from CPAN: 1.62001

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.58-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.58-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Mar 19 2005 Joe Orton <jorton@redhat.com> 1.58-2
- rebuild

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 1.58-1
- #121168
- Update to 1.58.
- Require perl(:MODULE_COMPAT_*).
- Handle ParserDetails.ini parser registration.
- BuildRequires libxml2-devel.
- Own installed directories.

* Fri Feb 27 2004 Chip Turner <cturner@redhat.com> - 1.56-1
- Specfile autogenerated.
