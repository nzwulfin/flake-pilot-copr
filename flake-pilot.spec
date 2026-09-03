Name:           flake-pilot
Version:        0.1.0
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

%check
%cargo_test -- -- --skip integration

%files
%license LICENSE cargo-vendor.txt
%doc README.md
%dir %{_sysconfdir}/flakes
%dir %{_datadir}/flakes
%{_bindir}/flake-ctl
%{_bindir}/podman-pilot
%{_bindir}/firecracker-pilot
%{_bindir}/sci

%changelog
* Thu Sep 03 2026 COPR Package Maintainer <user@fedoraproject.org> - 0.1.0-1
- Initial COPR package build for flake-pilot
