import os


def is_dqm_gui_running():
    from l1t_cli.commands.dqm.gui.setup import DQM_GUI_PATH
    pid_file = os.path.join(DQM_GUI_PATH, 'state/dqmgui/dev/pid')
    if not os.path.exists(pid_file):
        return False
    with open(pid_file) as f:
        pid = int(f.readline())

    import psutil
    dqm_is_running = psutil.pid_exists(pid)
    return dqm_is_running