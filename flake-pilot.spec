Name:           flake-pilot
Version:        3.1.53
Release:        1%{?dist}
Summary:        Launcher for execution of applications inside containers and VMs

License:        MIT
URL:            https://github.com/OSInside/flake-pilot
Source0:        %{url}/archive/refs/heads/main.tar.gz#/flake-pilot-main.tar.gz
Source1:        flake-pilot-vendor.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  glibc-static

Recommends:     podman
Suggests:       firecracker

%description
Flake Pilot provides an application launcher and registration utility for
applications executed inside isolated runtime environments such as OCI
containers or Firecracker MicroVMs.

%prep
%autosetup -n flake-pilot-main -a1
%cargo_prep -v vendor
test -f README.md || touch README.md

%build
%cargo_build
%cargo_vendor_manifest

%install
# Manual binary installation required for Cargo virtual workspaces
install -D -p -m 0755 target/rpm/flake-ctl %{buildroot}%{_bindir}/flake-ctl
install -D -p -m 0755 target/rpm/podman-pilot %{buildroot}%{_bindir}/podman-pilot
install -D -p -m 0755 target/rpm/firecracker-pilot %{buildroot}%{_bindir}/firecracker-pilot
install -D -p -m 0755 target/rpm/sci %{buildroot}%{_bindir}/sci

# System configuration and data directories
install -d -m 0755 %{buildroot}%{_sysconfdir}/flakes
install -d -m 0755 %{buildroot}%{_datadir}/flakes

# Install configuration templates required by flake-ctl
install -p -m 0644 flake-ctl/template/*.yaml %{buildroot}%{_sysconfdir}/flakes/

%check
%cargo_test -- -- --skip integration

%files
%license LICENSE cargo-vendor.txt
%doc README*
%dir %{_sysconfdir}/flakes
%config(noreplace) %{_sysconfdir}/flakes/*.yaml
%dir %{_datadir}/flakes
%{_bindir}/flake-ctl
%{_bindir}/podman-pilot
%{_bindir}/firecracker-pilot
%{_bindir}/sci

%changelog
%autochangelog
