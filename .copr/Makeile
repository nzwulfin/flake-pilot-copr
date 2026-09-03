# COPR executes: make -f .copr/Makefile srpm outdir="$(outdir)" spec="$(spec)"

srpm:
	# 1. Install missing tools into COPR's minimal build environment
	dnf install -y cargo rust rpm-build rpmdevtools git tar

	# 2. Download the upstream source tarball (Source0) listed in the spec file
	spectool -g -C . $(spec)

	# 3. Fetch dependencies and generate the vendor directory
	rm -rf source vendor
	git clone https://github.com/OSInside/flake-pilot source
	cd source && cargo vendor ../vendor

	# 4. Archive the vendor folder into Source1 expected by the spec
	tar -czf flake-pilot-vendor.tar.gz vendor
	rm -rf source vendor

	# 5. Build the SRPM and output it directly to $(outdir)
	rpmbuild -bs \
		--define "_sourcedir ." \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
