# Build Instructions

## Build Requirements
 * See `requirements.txt`

## Setup Python Environment
 * See `INSTALL.md` for details.

## Build Command Line

 * Make sure to activate the environment you created during INSTALL first, using:
   * `.venv\scripts\activate`

 * To build an executable, with the environment activated, call:
   * `python setup.py build_exe`

## Running

If you build the executable in the above steps, you will now have a `build\exe.win-amd64-3.11` directory. Run `trl_scu_main.exe` from there.

## Running without building

You can run the app directly from the command line.

 * Activate the environment you created during the `INSTALL` step:
   * `.venv\scripts\activate`
 * Run the app:
   * `python trl_scu_main.py`
