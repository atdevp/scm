import os

MYSQL = {
    "HOST": "127.0.0.1",
    "PORT": 3306,
    "USER": "root",
    "PASSWORD": "",
    "DATABASE": "scm"
}

CI_WORKSPACE = "/tmp/scm_data"
CICD_CFG = {
    "SRC_CODE_PATH": os.path.join(CI_WORKSPACE, "src_code"),
    "ONLINE_PACKAGE": os.path.join(CI_WORKSPACE, "online_package"),
    "DEVELOP_PACKAGE": os.path.join(CI_WORKSPACE, "develop_package"),
    "STATING_PACKAGE": os.path.join(CI_WORKSPACE, "stating_package")
}
