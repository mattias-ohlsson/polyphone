Name:           polyphone
Version:        2.2.0
Release:        1%{?dist}
Summary:        A soundfont editor

License:        GPLv3+
URL:            https://www.polyphone-soundfonts.com/
Source0:        https://github.com/davy7125/polyphone/archive/%{version}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  portaudio-devel
BuildRequires:  zlib-devel
BuildRequires:  libogg-devel
BuildRequires:  flac-devel
BuildRequires:  libvorbis-devel
BuildRequires:  glib2-devel
BuildRequires:  openssl-devel
BuildRequires:  rtmidi-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  stk-devel
BuildRequires:  desktop-file-utils

%description
Polyphone is an open-source soundfont editor for creating musical instruments.

%prep
%autosetup

# Enable debug
sed -i '1 i CONFIG += debug' sources/polyphone.pro

# Use local qcustomplot
sed -i 's|#DEFINES += USE_LOCAL_QCUSTOMPLOT|DEFINES += USE_LOCAL_QCUSTOMPLOT|' sources/polyphone.pro

# https://github.com/davy7125/polyphone/issues/96
sed -i 's|jack.h|jack/jack.h|' sources/context/audiodevice.cpp
sed -i 's|Chorus.h|stk/Chorus.h|' sources/sound_engine/voice.h
sed -i 's|FreeVerb|stk/FreeVerb|' sources/sound_engine/voice.h

%build
cd sources
qmake-qt5
%make_build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_bindir}
install -m 755 sources/bin/polyphone %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/pixmaps
cp logo.png %{buildroot}%{_datadir}/pixmaps/polyphone.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications \
 sources/contrib/polyphone.desktop

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/polyphone
%{_datadir}/applications/polyphone.desktop
%{_datadir}/pixmaps/polyphone.png

%changelog
* Sat Jun 20 2020 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 2.2.0-1
- Initial build
