SYS_REQ_DIR:=system_requirements

WHICH_REQS?=
_install_reqs:
	for pk in $$(cat ${WHICH_REQS}); do sudo apt-get install -yq "$$pk"; done

sys_reqs: WHICH_REQS=$(SYS_REQ_DIR)/base.txt
sys_reqs: _install_reqs

mysql_reqs: WHICH_REQS=$(SYS_REQ_DIR)/mysql.txt
mysql_reqs: _install_reqs

.PHONY: sys_reqs mysql_reqs
