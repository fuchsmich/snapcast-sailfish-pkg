Name:           snapcast
Version:        0.13.0
Release:        1
Summary:        Synchronous multi-room audio player
License:        GPL
Group:          Multimedia/Audio Adaptation
Url:            https://github.com/badaix/snapcast
Source0:        %{name}-%{version}.tar.gz
#Source1:        externals.tar.gz
Source2:        snapclient.service
Source3:        snapserver.service
Source4:        snapserver.default
Source5:        snapclient-nofork.service
Source6:        snapserver-nofork.service
Source7:        snapclient-nofork-user.service
Source8:        pulse-xpolicy-snapclient.conf
Source9:        snapserver-nofork-user.service

BuildRequires: flac-devel
BuildRequires: libvorbis-devel
BuildRequires: alsa-utils
BuildRequires: avahi-devel
BuildRequires: alsa-lib-devel

BuildRequires: libstdc++-static
BuildRequires: libatomic-devel
Requires: avahi

%description
Snapcast is a multi-room client-server audio player, where all clients are time 
synchronized with the server to play perfectly synced audio. It's not a 
standalone player, but an extension that turns your existing audio player into 
a Sonos-like multi-room solution. The server's audio input is a named 
pipe /tmp/snapfifo. All data that is fed into this file will be send 
to the connected clients. One of the most generic ways to use Snapcast is in 
conjunction with the music player daemon (MPD) or Mopidy, which can be configured 
to use a named pipe as audio output.

%prep
%setup
#%setup -D -T -a1

%build
pwd
ls
cd snapcast
make

%install
install -Dm755 server/snapserver %{buildroot}%{_bindir}/snapserver
#install -Dm644 -g root -o root server/snapserver.1 ${pkgdir}/usr/share/man/man1/snapserver.1

install -Dm755 client/snapclient %{buildroot}%{_bindir}/snapclient
#install -Dm644 -g root -o root client/snapclient.1 ${pkgdir}/usr/share/man/man1/snapclient.1

#install -Dm644 server/debian/snapserver.service %{buildroot}%{_unitdir}/snapserver.service
install -Dm644 %{SOURCE3} %{buildroot}%{_unitdir}/snapserver.service
install -Dm644 %{SOURCE6} %{buildroot}%{_unitdir}/snapserver-nofork.service
install -Dm644 %{SOURCE9} %{buildroot}%{_userunitdir}/snapserver.service
#install -Dm644 server/debian/snapserver.default %{buildroot}%{_sysconfdir}/default/snapserver
install -Dm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/snapserver
install -Dm644 %{SOURCE2} %{buildroot}%{_unitdir}/snapclient.service
install -Dm644 %{SOURCE5} %{buildroot}%{_unitdir}/snapclient-nofork.service
install -Dm644 %{SOURCE7} %{buildroot}%{_userunitdir}/snapclient.service
install -Dm644 client/debian/snapclient.default %{buildroot}%{_sysconfdir}/default/snapclient
install -Dm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pulse/xpolicy.conf.d/snapclient.conf

%pre
#install
if [ "$1" -eq 1 ]; then
%{_sbindir}/useradd -r -s /bin/false -c "User for Snapserver" -d /run/snapserver -G inet -U snapserver 2> /dev/null || :
%{_sbindir}/useradd -r -s /bin/false -c "User for Snapclient" -d /run/snapclient -G audio,inet -U snapclient 2> /dev/null || :
fi
#upgrade
if [ "$1" -eq 2 ]; then
%{_sbindir}/usermod -G inet snapserver 2> /dev/null || :
%{_sbindir}/usermod -g snapclient -G audio,inet snapclient 2> /dev/null || :
fi

%post
systemctl daemon-reload 

%preun
if [ "$1" -eq 0 ]; then
systemctl stop snapserver.service snapclient.service >/dev/null 2>&1
fi


%postun
systemctl daemon-reload >/dev/null 2>&1

%files
%doc LICENSE README.md
%{_bindir}/snapserver
%{_bindir}/snapclient
%{_unitdir}/snapserver.service
%{_unitdir}/snapclient.service
%{_unitdir}/snapserver-nofork.service
%{_unitdir}/snapclient-nofork.service
%{_userunitdir}/snapclient.service
%{_userunitdir}/snapserver.service
%config %{_sysconfdir}/default/snapserver
%config %{_sysconfdir}/default/snapclient
%{_sysconfdir}/pulse/xpolicy.conf.d/snapclient.conf

%changelog
